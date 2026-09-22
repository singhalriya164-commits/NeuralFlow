import zipfile
import xml.etree.ElementTree as ET

path = r'c:\Users\Chaha\Downloads\Project-template-a4.docx'
with zipfile.ZipFile(path) as z:
    root = ET.fromstring(z.read('word/styles.xml'))

ns = {'w': 'http://purl.oclc.org/ooxml/wordprocessingml/main'}

for style in root.findall('w:style', ns):
    s_id = style.get('{http://purl.oclc.org/ooxml/wordprocessingml/main}styleId')
    name_el = style.find('w:name', ns)
    name = name_el.get('{http://purl.oclc.org/ooxml/wordprocessingml/main}val') if name_el is not None else s_id
    
    rPr = style.find('w:rPr', ns)
    sz = rPr.find('w:sz', ns).get('{http://purl.oclc.org/ooxml/wordprocessingml/main}val') if (rPr is not None and rPr.find('w:sz', ns) is not None) else 'def'
    b = rPr.find('w:b', ns) is not None if rPr is not None else False
    i = rPr.find('w:i', ns) is not None if rPr is not None else False
    caps = rPr.find('w:caps', ns) is not None if rPr is not None else False
    smallCaps = rPr.find('w:smallCaps', ns) is not None if rPr is not None else False
    
    pPr = style.find('w:pPr', ns)
    jc = pPr.find('w:jc', ns).get('{http://purl.oclc.org/ooxml/wordprocessingml/main}val') if (pPr is not None and pPr.find('w:jc', ns) is not None) else 'def'
    sp = pPr.find('w:spacing', ns) if pPr is not None else None
    sp_before = sp.get('{http://purl.oclc.org/ooxml/wordprocessingml/main}before') if sp is not None else 'def'
    sp_after = sp.get('{http://purl.oclc.org/ooxml/wordprocessingml/main}after') if sp is not None else 'def'
    sp_line = sp.get('{http://purl.oclc.org/ooxml/wordprocessingml/main}line') if sp is not None else 'def'
    
    pt_val = f"{float(sz)/2}pt" if sz != 'def' else "default (10pt)"
    print(f"[{name}]: sz={pt_val}, bold={b}, italic={i}, smallCaps={smallCaps}, caps={caps}, align={jc}, before={sp_before}, after={sp_after}, line={sp_line}")
