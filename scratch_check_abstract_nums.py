import docx

doc = docx.Document(r"c:\Users\Chaha\Downloads\NeuralFlow_Group9_Final_Fixed.docx")
num_part = doc.part.numbering_part

from xml.etree import ElementTree as ET
import lxml.etree as etree

for ab_id in ['18', '14']:
    abs_matches = num_part._element.xpath(f'.//w:abstractNum[@w:abstractNumId="{ab_id}"]')
    if abs_matches:
        print(f"=== abstractNumId {ab_id} ===")
        for lvl in abs_matches[0].xpath(".//*[local-name()='lvl']"):
            print(etree.tostring(lvl, encoding='unicode'))
