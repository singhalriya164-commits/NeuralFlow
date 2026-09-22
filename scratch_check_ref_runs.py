import docx

doc = docx.Document(r"c:\Users\Chaha\Downloads\NeuralFlow_Group9_Final_Fixed.docx")
for i, p in enumerate(doc.paragraphs):
    if p.style.name == "references":
        print(f"P{i}: {[r.text for r in p.runs[:3]]}")
