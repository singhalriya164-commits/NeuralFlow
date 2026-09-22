import docx
from report_builder_core import load_template_doc
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = load_template_doc(r"c:\Users\Chaha\Downloads\Project-template-a4.docx")

print("Original sections:", len(doc.sections))
for i, s in enumerate(doc.sections):
    cols = s._sectPr.xpath('./w:cols')
    num = cols[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num', 'default(1)') if cols else 'none'
    space = cols[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}space', 'none') if cols else 'none'
    print(f"  Section {i}: num={num}, space={space}")

# Remove placeholder paragraphs from index 10 onwards
p_elements = [p._p for p in doc.paragraphs[10:]]
for p_elem in p_elements:
    p_elem.getparent().remove(p_elem)

for t in doc.tables:
    t._tbl.getparent().remove(t._tbl)

# Now check sections after removal
print("\nSections after removing p[10:]:")
print(f"Total sections: {len(doc.sections)}")
for i, s in enumerate(doc.sections):
    cols = s._sectPr.xpath('./w:cols')
    num = cols[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num', 'default(1)') if cols else 'none'
    space = cols[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}space', 'none') if cols else 'none'
    print(f"  Section {i}: num={num}, space={space}")

# Fix the last section's sectPr to 2 columns
last_sec = doc.sections[-1]
sectPr = last_sec._sectPr
for c in sectPr.xpath('./w:cols'):
    sectPr.remove(c)
cols = parse_xml(f'<w:cols {nsdecls("w")} w:num="2" w:space="360"/>')
sectPr.append(cols)

print("\nSections after setting w:num=2 on last section:")
for i, s in enumerate(doc.sections):
    cols = s._sectPr.xpath('./w:cols')
    num = cols[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num', 'default(1)') if cols else 'none'
    space = cols[0].get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}space', 'none') if cols else 'none'
    print(f"  Section {i}: num={num}, space={space}")
