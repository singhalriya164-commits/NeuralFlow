import win32com.client
import os

word = None
try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc_path = os.path.abspath(r"c:\Users\Chaha\Downloads\NeuralFlow_Group9_Final_Fixed.docx")
    doc = word.Documents.Open(doc_path, ReadOnly=True)
    
    # Check all styles that have numbering
    print("Checking paragraphs with ListString:")
    count = 0
    for i in range(1, doc.Paragraphs.Count + 1):
        p = doc.Paragraphs(i)
        ls = p.Range.ListFormat.ListString
        if ls:
            t = p.Range.Text.strip()[:60]
            print(f"P{i} [{p.Style.NameLocal}]: ListString={repr(ls)} | Text={repr(t)}")
            count += 1
            if count > 40:
                print("... and many more")
                break
                
    doc.Close(False)
except Exception as e:
    print("Error:", e)
finally:
    if word:
        word.Quit()
