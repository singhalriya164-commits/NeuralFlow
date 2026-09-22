import docx

doc = docx.Document(r"c:\Users\Chaha\Downloads\NeuralFlow_Group9_Final_Fixed.docx")
style_names = [
    'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4',
    'bullet list', 'figure caption', 'footnote', 'references',
    'table footnote', 'table head'
]

for s in doc.styles:
    if s.name in style_names or s.style_id in style_names:
        print(f"=== STYLE: {s.name} ({s.style_id}) ===")
        pPr = s.element.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr")
        if pPr is not None:
            print(pPr.xml)
        else:
            print("No pPr")
