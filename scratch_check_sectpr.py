import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile(r"c:\Users\Chaha\Downloads\Project-template-a4.docx", "r") as z:
    xml = z.read("word/document.xml").decode("utf-8")
    root = ET.fromstring(xml)
    
    # find all sectPr
    sectPrs = []
    p_idx = 0
    for p in root.iter():
        if p.tag.endswith('}p'):
            p_idx += 1
            for child in p:
                if child.tag.endswith('}pPr'):
                    for sub in child:
                        if sub.tag.endswith('}sectPr'):
                            sectPrs.append((p_idx, ET.tostring(sub, encoding='utf-8').decode('utf-8')))
        elif p.tag.endswith('}body'):
            for child in p:
                if child.tag.endswith('}sectPr'):
                    sectPrs.append(('body_end', ET.tostring(child, encoding='utf-8').decode('utf-8')))

    for loc, s_xml in sectPrs:
        print(f"Location: {loc}")
        print(s_xml)
        print("-" * 40)
