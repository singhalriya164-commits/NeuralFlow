import docx

doc = docx.Document(r"c:\Users\Chaha\Downloads\NeuralFlow_Group9_Final_Fixed.docx")
for i, p in enumerate(doc.paragraphs):
    if p.style.name.startswith("Heading"):
        print(f"P{i} [{p.style.name}]: {repr(p.text[:60])}")
