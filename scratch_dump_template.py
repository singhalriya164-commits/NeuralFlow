import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile(r"c:\Users\Chaha\Downloads\Project-template-a4.docx", "r") as z:
    xml = z.read("word/document.xml").decode("utf-8")
    root = ET.fromstring(xml)
    
    with open("template_structure.txt", "w", encoding="utf-8") as out:
        p_idx = 0
        for elem in root.iter():
            if elem.tag.endswith('}p'):
                p_idx += 1
                pStyle = ""
                for child in elem.iter():
                    if child.tag.endswith('}pStyle'):
                        pStyle = child.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') or child.attrib.get('{http://purl.oclc.org/ooxml/wordprocessingml/main}val') or ""
                texts = [c.text for c in elem.iter() if c.tag.endswith('}t') and c.text]
                full_text = "".join(texts).strip()
                sect = [c for c in elem.iter() if c.tag.endswith('}sectPr')]
                sect_str = f" [SECT_PR: len={len(sect)}]" if sect else ""
                out.write(f"p{p_idx:02d} [{pStyle}]{sect_str}: {full_text}\n")
            elif elem.tag.endswith('}tbl'):
                out.write(f"--- TABLE FOUND ---\n")
            elif elem.tag.endswith('}sectPr') and not any(elem in p.iter() for p in root.iter() if p.tag.endswith('}p')):
                out.write(f"--- BODY SECT_PR FOUND ---\n")

print("Dump complete -> template_structure.txt")
