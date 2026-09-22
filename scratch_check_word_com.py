import win32com.client
import os

word = None
try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc_path = os.path.abspath(r"c:\Users\Chaha\Downloads\NeuralFlow_Group9_Final_Fixed.docx")
    doc = word.Documents.Open(doc_path, ReadOnly=True)
    print("Opened document successfully in Word!")
    print(f"Total paragraphs in Word COM: {doc.Paragraphs.Count}")
    
    # Check paragraphs around Table I and Fig 2
    for i in range(1, min(doc.Paragraphs.Count + 1, 120)):
        p = doc.Paragraphs(i)
        t = p.Range.Text.strip()
        ls = p.Range.ListFormat.ListString
        if ls or any(k in t for k in ["TABLE", "Fig", "INTRODUCTION"]):
            print(f"Word P{i}: ListString={repr(ls)} | Text={repr(t[:80])}")
            
    doc.Close(False)
except Exception as e:
    print("Error with Word COM:", e)
finally:
    if word:
        word.Quit()
