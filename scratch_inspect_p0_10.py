import docx
from report_builder_core import load_template_doc

doc = load_template_doc(r"c:\Users\Chaha\Downloads\Project-template-a4.docx")

for i in range(11):
    p = doc.paragraphs[i]
    sect_in_p = p._p.xpath('./w:pPr/w:sectPr')
    s_info = f" [SECT_PR: {len(sect_in_p)}]" if sect_in_p else ""
    print(f"p{i:02d} [{p.style.name}]{s_info}: text={repr(p.text[:60])}")
