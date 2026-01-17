
import re

def parse_questions(filename, output_filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Level 5 section
    # Search for "5.CẤP ĐỘ 5"
    start_match = re.search(r'5\.CẤP ĐỘ 5', content)
    
    # End is tricky. It seems to end before "Từ viết tắt:" or "1: Chương 1" around line 2012
    # Let's search for "Từ viết tắt:" or just split by lines and look for footer
    
    if not start_match:
        print("Could not find start (Level 5) marker.")
        return

    # Slice from start to end of file
    section_text_raw = content[start_match.end():]
    
    # Try to find end marker
    end_match = re.search(r'(Từ viết tắt:|III\.\s*Đ\s*uất)', section_text_raw)
    if end_match:
         section_text = section_text_raw[:end_match.start()]
    else:
         section_text = section_text_raw
         
    lines = section_text.split('\n')
    print(f"Total lines in section: {len(lines)}")

    questions = []
    current_q = None
    
    line_idx = 0
    while line_idx < len(lines):
        line = lines[line_idx].strip()
        line_idx += 1
        
        if not line:
            continue
            
        # IGNORE standalone numbers (Chapter/Page numbers) or single chars that aren't answers
        if re.match(r'^\d+$', line):
            continue

        # Check for Question start
        start_q_match = re.search(r'^(\d+)\.\s*(.*)', line)
        embedded_q_match = re.search(r'\s+(\d+)\.\s+(.*)', line)
        
        is_new_q = False
        q_num = -1
        q_text = ""
        pre_text = ""
        
        if start_q_match:
             is_new_q = True
             q_num = int(start_q_match.group(1))
             q_text = start_q_match.group(2)
        elif embedded_q_match:
            found_num = int(embedded_q_match.group(1))
            # Heuristic: logical progression
            if current_q and (found_num == current_q['number'] + 1):
                match_start = embedded_q_match.start()
                pre_text = line[:match_start].strip()
                q_num = found_num
                q_text = embedded_q_match.group(2)
                is_new_q = True

        if is_new_q:
            if pre_text and current_q:
                 process_content_line(current_q, pre_text)
            
            if current_q:
                questions.append(current_q)
            
            current_q = {
                'number': q_num,
                'question': q_text,
                'options': [],
                'answer': None
            }
            # Check answer on same line (e.g. "Question? D 1")
            extract_answer_from_q_line(current_q)
            # Check embedded Option A on same line (e.g. "Question? A. Answer")
            check_embedded_start_option(current_q)
            continue
            
        if current_q:
            process_content_line(current_q, line)
    
    if current_q:
        questions.append(current_q)

    # Output generation
    write_output(questions, output_filename)

def check_embedded_start_option(q):
    match = re.search(r'\s+(A\.\s.*)$', q['question'])
    if match:
        opt_text = match.group(1).strip()
        q['options'].append(opt_text)
        q['question'] = q['question'][:match.start()].strip()

def extract_answer_from_q_line(q):
    # Pattern: [Text] [Space] [ABCD] [Space] [Number/Empty]
    ans_match = re.search(r'\s+([ABCD])\s*(\d+)?$', q['question'])
    if ans_match:
        found_ans = ans_match.group(1)
        q['answer'] = found_ans
        q['question'] = q['question'][:ans_match.start()].strip()

def process_content_line(q, line):
    # IGNORE standalone numbers
    if re.match(r'^\d+$', line):
        return

    # Check for Answer (at end)
    ans_match = re.search(r'\s+([ABCD])\s*(\d+)?$', line)
    line_content = line
    found_ans = None
    if ans_match:
         found_ans = ans_match.group(1)
         line_content = line[:ans_match.start()].strip()
    
    if found_ans:
        q['answer'] = found_ans
    
    # Parse Options from line_content
    # Matches: "^A. ", " B. ", " C. ", "D.Text" ...
    matches = list(re.finditer(r'(?:^|\s+)([ABCD])\.\s*', line_content))
    
    if not matches:
        # No formal options found. Append to previous context.
        # Check standard answer line "D" (Single char)
        standalone_ans = re.match(r'^([ABCD])\s*(\d+)?$', line_content)
        if standalone_ans:
             if not q['answer']: q['answer'] = standalone_ans.group(1)
        else:
            if line_content:
                if q['options']:
                    q['options'][-1] += " " + line_content
                else:
                    q['question'] += " " + line_content
        return

    # If matches found, process them
    prev_end = 0
    
    for i, m in enumerate(matches):
        # Text before this match (if i==0)
        if i == 0:
             preamble = line_content[:m.start()].strip()
             if preamble:
                if q['options']:
                    q['options'][-1] += " " + preamble
                else:
                    q['question'] += " " + preamble
        
        # Content of this option
        opt_char = m.group(1)
        start_text = m.end()
        end_text = len(line_content)
        if i + 1 < len(matches):
             end_text = matches[i+1].start()
        
        opt_text = line_content[start_text:end_text].strip()
        q['options'].append(f"{opt_char}. {opt_text}")

def write_output(questions, output_filename):
    output_lines = []
    output_lines.append("# CẤP ĐỘ 5 - NHÓM CÂU HỎI RẤT KHÓ")
    output_lines.append("")
    
    questions.sort(key=lambda x: x['number'])
    
    for q in questions:
        output_lines.append(f"**Câu {q['number']}.** {q['question']}")
        for opt in q['options']:
            output_lines.append(opt)
        output_lines.append("")
        
    output_lines.append("---")
    output_lines.append("## ĐÁP ÁN")
    
    ans_buffer = []
    start_num = questions[0]['number'] if questions else 1
    end_num = questions[-1]['number'] if questions else 0
    
    q_map = {q['number']: q.get('answer', '?') for q in questions}
    
    for i in range(start_num, end_num + 1):
        ans = q_map.get(i, "?")
        if not ans: ans = "?"
        ans_buffer.append(f"{i}.{ans}")
        
    chunk_size = 10
    for i in range(0, len(ans_buffer), chunk_size):
        output_lines.append(" ".join(ans_buffer[i:i+chunk_size]))
        output_lines.append("")

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
        
    print(f"Extracted {len(questions)} questions. Last: {end_num}")
    print(f"Saved to {output_filename}")

parse_questions(r'e:\DeCuongPhapLuat\DeCuongPhapLuat.md', r'e:\DeCuongPhapLuat\CauHoi_CapDo5.md')
