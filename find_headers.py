
import re

filename = r'e:\DeCuongPhapLuat\DeCuongPhapLuat.md'
with open(filename, 'r', encoding='utf-8') as f:
    headers = []
    for i, line in enumerate(f):
        if 'CẤP ĐỘ' in line:
            headers.append(f"{i+1}: {line.strip()}")

with open('headers.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(headers))
print("Headers saved to headers.txt")
