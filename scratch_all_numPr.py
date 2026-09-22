import docx

doc = docx.Document(r"c:\Users\Chaha\Downloads\NeuralFlow_Group9_Final_Fixed.docx")
styles_el = doc.styles._element
numPrs = styles_el.xpath(".//*[local-name()='numPr']")
print(f"Total numPr elements in styles.xml: {len(numPrs)}")
for np in numPrs:
    parent = np.getparent()
    parent_parent = parent.getparent() if parent is not None else None
    style_id = parent_parent.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}styleId') if parent_parent is not None else None
    name_el = parent_parent.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}name') if parent_parent is not None else None
    name_val = name_el.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') if name_el is not None else None
    print(f"  Parent: {parent.tag}, StyleId: {style_id}, Name: {name_val}")
