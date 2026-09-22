import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile(r"c:\Users\Chaha\Downloads\Project-template-a4.docx", "r") as z:
    xml = z.read("word/styles.xml").decode("utf-8")
    root = ET.fromstring(xml)

for s in root.iter():
    if s.tag.endswith('}style') and s.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type', '') == 'paragraph' or s.attrib.get('{http://purl.oclc.org/ooxml/wordprocessingml/main}type', '') == 'paragraph':
        style_id = s.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}styleId') or s.attrib.get('{http://purl.oclc.org/ooxml/wordprocessingml/main}styleId')
        name = ""
        for c in s:
            if c.tag.endswith('}name'):
                name = c.attrib.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') or c.attrib.get('{http://purl.oclc.org/ooxml/wordprocessingml/main}val')
        print(f"ID: {style_id:<18} Name: {name:<20}")
        # print rPr
        rPr_info = []
        for c in s:
            if c.tag.endswith('}rPr'):
                for r in c:
                    tag = r.tag.split('}')[-1]
                    val = list(r.attrib.values())[0] if r.attrib else ""
                    rPr_info.append(f"{tag}={val}" if val else tag)
            if c.tag.endswith('}pPr'):
                for p in c:
                    tag = p.tag.split('}')[-1]
                    val = list(p.attrib.values())[0] if p.attrib else ""
                    rPr_info.append(f"pPr:{tag}={val}" if val else f"pPr:{tag}")
        print("   " + ", ".join(rPr_info))
