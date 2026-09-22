import docx
import shutil
import re
import os
import win32com.client

src = r"c:\Users\Chaha\Downloads\NeuralFlow_Group9_Final_Fixed.docx"
test_dst = r"c:\Users\Chaha\Downloads\NeuralFlow_Test_Fixed.docx"

doc = docx.Document(src)

# 1. Remove numPr from styles
styles_el = doc.styles._element
numPrs = styles_el.xpath(".//*[local-name()='numPr']")
print(f"Found {len(numPrs)} numPr in styles. Removing them...")
for np in numPrs:
    parent = np.getparent()
    parent.remove(np)

# In figure caption style, also remove w:tabs if present
for s in doc.styles:
    if s.name in ['figure caption', 'figurecaption']:
        tabs = s.element.xpath(".//*[local-name()='tabs']")
        for t in tabs:
            t.getparent().remove(t)

# 2. Update Figure in captions and body text
fig_caption_count = 0
for p in doc.paragraphs:
    if p.style.name in ['figure caption', 'figurecaption']:
        # Replace in runs
        for r in p.runs:
            if re.search(r'\bFig\.\s*(\d+)', r.text):
                r.text = re.sub(r'\bFig\.\s*(\d+)', r'Figure \1', r.text)
                fig_caption_count += 1
                print(f"Caption updated: {repr(r.text)}")

print(f"Total captions updated: {fig_caption_count}")

# 3. Update Fig. to Figure in body text
body_fig_count = 0
for i, p in enumerate(doc.paragraphs):
    if p.style.name not in ['figure caption', 'figurecaption']:
        for r in p.runs:
            if re.search(r'\bFig\.\s*(\d+)', r.text):
                old_text = r.text
                r.text = re.sub(r'\bFig\.\s*(\d+)', r'Figure \1', r.text)
                body_fig_count += 1
                print(f"P{i} body text updated: {repr(old_text)} -> {repr(r.text)}")

print(f"Total body text Fig. updated: {body_fig_count}")

doc.save(test_dst)
print("Saved to", test_dst)

# Now inspect with Word COM
print("\n--- INSPECTING WITH WORD COM ---")
word = None
try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    wdoc = word.Documents.Open(os.path.abspath(test_dst), ReadOnly=True)
    
    # Check paragraphs with ListString
    list_count = 0
    for i in range(1, wdoc.Paragraphs.Count + 1):
        p = wdoc.Paragraphs(i)
        ls = p.Range.ListFormat.ListString
        if ls:
            list_count += 1
            if list_count <= 20:
                print(f"Still has ListString: P{i} [{p.Style.NameLocal}]: {repr(ls)} | Text={repr(p.Range.Text.strip()[:60])}")
    print(f"Total paragraphs with ListString remaining: {list_count}")
    
    # Check specific paragraphs in Word
    # Check Headings, Table I, Figure 1, Figure 2
    for i in range(1, min(wdoc.Paragraphs.Count + 1, 350)):
        p = wdoc.Paragraphs(i)
        t = p.Range.Text.strip()
        if any(k in t for k in ["TABLE I.", "TABLE II.", "Figure 1.", "Figure 2.", "I. INTRODUCTION", "A. Historical"]):
            print(f"Word P{i} [{p.Style.NameLocal}]: ListString={repr(p.Range.ListFormat.ListString)} | Text={repr(t[:80])}")
            
    wdoc.Close(False)
except Exception as e:
    print("Word COM error:", e)
finally:
    if word:
        word.Quit()
