import docx

doc = docx.Document(r"c:\Users\Chaha\Downloads\NeuralFlow_Group9_Final_Fixed.docx")
num_part = doc.part.numbering_part

print("--- NUM DEFINITIONS ---")
for num in num_part._element.xpath(".//w:num"):
    numId = num.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numId")
    abId_elem = num.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}abstractNumId")
    if abId_elem is None:
        continue
    abId = abId_elem.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val")
    abs_matches = num_part._element.xpath(f'.//w:abstractNum[@w:abstractNumId="{abId}"]')
    if not abs_matches:
        continue
    ab = abs_matches[0]
    for lvl in ab.xpath(".//*[local-name()='lvl']"):
        ilvl = lvl.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ilvl")
        lvlText = lvl.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}lvlText")
        lt = lvlText.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val") if lvlText is not None else ""
        fmt = lvl.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numFmt")
        fv = fmt.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val") if fmt is not None else ""
        print(f"numId={numId} (ab={abId}, lvl={ilvl}): text={repr(lt)} fmt={fv}")

print("\n--- STYLES WITH numPr ---")
for s in doc.styles:
    nums = s.element.xpath(".//*[local-name()='numPr']")
    if nums:
        numId = nums[0].find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numId")
        nid = numId.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val") if numId is not None else None
        print(f"Style: '{s.name}' ({s.style_id}) -> numId={nid}")

print("\n--- PARAGRAPHS WITH DIRECT numPr ---")
direct_num = 0
for i, p in enumerate(doc.paragraphs):
    nums = p._p.xpath(".//*[local-name()='numPr']")
    if nums:
        direct_num += 1
        numId = nums[0].find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numId")
        nid = numId.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val") if numId is not None else None
        print(f"P{i} [{p.style.name}] -> numId={nid}: {repr(p.text[:60])}")
print(f"Total paragraphs with direct numPr: {direct_num}")
