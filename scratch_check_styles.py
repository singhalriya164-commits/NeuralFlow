import docx
from report_builder_core import load_template_doc

doc = load_template_doc(r"c:\Users\Chaha\Downloads\Project-template-a4.docx")
print("Number of styles in template:", len(doc.styles))
for s in doc.styles:
    if s.type == docx.enum.style.WD_STYLE_TYPE.PARAGRAPH:
        print(f"Style: '{s.name}' (id: {s.style_id})")
