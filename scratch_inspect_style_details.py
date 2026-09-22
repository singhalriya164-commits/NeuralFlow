import docx
from report_builder_core import load_template_doc

doc = load_template_doc(r"c:\Users\Chaha\Downloads\Project-template-a4.docx")

styles_to_check = [
    'paper title', 'paper subtitle', 'Author', 'Affiliation', 'Abstract', 'Keywords',
    'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4', 'Heading 5',
    'Body Text', 'bullet list', 'equation', 'figure caption',
    'table head', 'table col head', 'table col subhead', 'table copy', 'table footnote',
    'references'
]

print(f"{'Style Name':<20} {'Font':<18} {'Size':<8} {'Bold':<6} {'Italic':<8} {'Caps/SmallCaps':<16} {'Alignment':<12} {'SpaceBefore':<12} {'SpaceAfter':<12}")
print("-" * 110)

for name in styles_to_check:
    try:
        s = doc.styles[name]
        font = s.font.name or "Inherit"
        size = f"{s.font.size.pt}pt" if s.font.size else "Inherit"
        bold = str(s.font.bold) if s.font.bold is not None else "-"
        italic = str(s.font.italic) if s.font.italic is not None else "-"
        caps = ""
        if s.font.all_caps: caps = "All-Caps"
        elif s.font.small_caps: caps = "Small-Caps"
        else: caps = "-"
        
        align = str(s.paragraph_format.alignment) if s.paragraph_format.alignment is not None else "Inherit"
        sb = f"{s.paragraph_format.space_before.pt}pt" if s.paragraph_format.space_before else "-"
        sa = f"{s.paragraph_format.space_after.pt}pt" if s.paragraph_format.space_after else "-"
        
        print(f"{name:<20} {font:<18} {size:<8} {bold:<6} {italic:<8} {caps:<16} {align:<12} {sb:<12} {sa:<12}")
    except KeyError:
        print(f"MISSING STYLE: {name}")
