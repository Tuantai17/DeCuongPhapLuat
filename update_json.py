import json
import re

file_path = r"d:\DeCuongPhapLuat\OnTapPhapLuat.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract JSON
match = re.search(r'const allQuestions = (\[.*?\]);', content, re.DOTALL)
if not match:
    print("Could not find allQuestions JSON")
    exit(1)

json_str = match.group(1)
questions = json.loads(json_str)

# Update Questions
count = 0
for q in questions:
    if q['level'] == 2:
        if q['id'] == 54:
            # Update Options for Q54
            q['options'] = [
                {"key": "A", "text": "Tổ chức công đoàn"},
                {"key": "B", "text": "Thanh tra lao động, Toà án nhân dân"},
                {"key": "C", "text": "Người lao động"},
                {"key": "D", "text": "Người sử dụng lao động"}
            ]
            q['correct_answer'] = "B" # Confirming key
            print("Updated Q54 L2")
            count += 1
        
        elif q['id'] == 37:
            # Update Key for Q37
            q['correct_answer'] = "D"
            print("Updated Q37 L2 Key to D")
            count += 1
            
        elif q['id'] == 96:
            # Update Text for Q96 Option D
            for opt in q['options']:
                if opt['key'] == "D":
                    opt['text'] = "Cả hai nguyên nhân trên (lãnh đạo và phẩm chất) đều đúng."
            print("Updated Q96 L2 Option D text")
            count += 1

        elif q['id'] == 97:
             # Update Text for Q97 Option D
            for opt in q['options']:
                if opt['key'] == "D":
                     opt['text'] = "Cả hai nguyên nhân trên (lãnh đạo và phẩm chất) đều đúng."
            print("Updated Q97 L2 Option D text")
            count += 1

# Serialize back
new_json_str = json.dumps(questions, ensure_ascii=False)
new_content = content.replace(json_str, new_json_str)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Successfully updated {count} questions.")
