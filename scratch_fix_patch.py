with open('generate_full_25page_report.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '# Appendices extension for generate_full_25page_report.py'
end_marker = '    # Save to both workspace and Downloads template locations'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

with open('appendices_patch.py', 'r', encoding='utf-8') as pf:
    p_text = pf.read()

s_start = p_text.find("'''") + 3
s_end = p_text.rfind("'''")
inner_code = p_text[s_start:s_end]

new_content = content[:start_idx] + inner_code + '\n\n' + content[end_idx:]
with open('generate_full_25page_report.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Successfully cleaned up generate_full_25page_report.py!')
