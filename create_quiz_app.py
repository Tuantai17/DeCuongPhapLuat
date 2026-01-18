
import os
import re
import json

def parse_markdown_file(filepath, level):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    parts = content.split('## ĐÁP ÁN')
    if len(parts) < 2:
        print(f"Warning: No Answer section found in {filepath}")
        return []
    
    q_section = parts[0]
    a_section = parts[1]

    answers = {}
    ans_matches = re.findall(r'(\d+)\.\s*([ABCD])', a_section)
    for num_str, char in ans_matches:
        answers[int(num_str)] = char

    questions = []
    lines = q_section.split('\n')
    
    current_q = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        q_match = re.match(r'\*\*Câu\s+(\d+)\.\*\*\s*(.*)', line)
        if q_match:
            if current_q:
                questions.append(current_q)
            
            q_num = int(q_match.group(1))
            q_text = q_match.group(2)
            current_q = {
                'id': q_num,
                'level': level,
                'question': q_text,
                'options': [],
                'correct_answer': answers.get(q_num, '?')
            }
            continue
        
        opt_match = re.match(r'^([ABCD])\.\s*(.*)', line)
        if opt_match and current_q:
            opt_char = opt_match.group(1)
            opt_text = opt_match.group(2)
            current_q['options'].append({'key': opt_char, 'text': opt_text})

    if current_q:
        questions.append(current_q)
        
    return questions

def generate_html(all_questions, output_file):
    json_data = json.dumps(all_questions, ensure_ascii=False)
    
    html_content = f'''<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="On Tap Phap Luat">
    <meta name="theme-color" content="#667eea">
    <title>On Tap Phap Luat Dai Cuong</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --primary-light: #818cf8;
            --success: #22c55e;
            --success-light: #dcfce7;
            --error: #ef4444;
            --error-light: #fee2e2;
            --warning: #f59e0b;
            --warning-light: #fef3c7;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --card-shadow: 0 20px 60px rgba(0,0,0,0.15);
            --text-dark: #1e293b;
            --text-medium: #475569;
            --text-light: #94a3b8;
            --border: #e2e8f0;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-gradient);
            min-height: 100vh;
            color: var(--text-dark);
            line-height: 1.6;
            padding: 20px;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            padding: 40px 20px;
            color: white;
        }}
        
        header h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 8px;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            letter-spacing: -0.5px;
        }}
        
        header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}

        .card {{
            background: white;
            border-radius: 24px;
            padding: 40px;
            box-shadow: var(--card-shadow);
            margin-bottom: 24px;
        }}
        
        .card-hidden {{
            display: none;
        }}

        /* Setup Screen */
        .setup-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-dark);
            text-align: center;
            margin-bottom: 32px;
        }}
        
        .select-wrapper {{
            margin-bottom: 32px;
        }}
        
        .select-label {{
            display: block;
            font-weight: 600;
            color: var(--text-medium);
            margin-bottom: 12px;
            font-size: 0.95rem;
        }}
        
        .custom-select {{
            width: 100%;
            padding: 16px 20px;
            font-size: 1rem;
            font-family: inherit;
            border: 2px solid var(--border);
            border-radius: 12px;
            background: white;
            color: var(--text-dark);
            cursor: pointer;
            transition: all 0.2s;
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 16px center;
            background-size: 20px;
        }}
        
        .custom-select:focus {{
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }}
        
        .custom-select:hover {{
            border-color: var(--primary-light);
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 14px 28px;
            font-size: 1rem;
            font-weight: 600;
            font-family: inherit;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .btn-primary {{
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
        }}
        
        .btn-primary:hover {{
            background: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }}
        
        .btn-secondary {{
            background: white;
            color: var(--primary);
            border: 2px solid var(--primary);
        }}
        
        .btn-secondary:hover {{
            background: rgba(99, 102, 241, 0.05);
        }}
        
        .btn-warning {{
            background: var(--warning);
            color: white;
            box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4);
        }}
        
        .btn-warning:hover {{
            background: #d97706;
            transform: translateY(-2px);
        }}
        
        .btn-block {{
            width: 100%;
        }}

        /* Stats Bar */
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 24px;
            padding: 16px 24px;
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            margin-bottom: 24px;
            color: white;
            font-weight: 600;
        }}
        
        .stat-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .stat-value {{
            font-size: 1.25rem;
            font-weight: 700;
        }}

        /* Question Card */
        .question-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            background: var(--bg-gradient);
            color: white;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .question-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }}
        
        .question-id {{
            color: var(--text-light);
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .question-text {{
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--text-dark);
            margin-bottom: 28px;
            line-height: 1.7;
        }}

        .options-list {{
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}
        
        .option-item {{
            display: flex;
            align-items: flex-start;
            gap: 16px;
            padding: 18px 20px;
            background: #f8fafc;
            border: 2px solid var(--border);
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        .option-item:hover {{
            border-color: var(--primary-light);
            background: #f1f5f9;
            transform: translateX(4px);
        }}
        
        .option-key {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            background: white;
            border: 2px solid var(--border);
            border-radius: 10px;
            font-weight: 700;
            color: var(--primary);
            flex-shrink: 0;
        }}
        
        .option-text {{
            flex: 1;
            padding-top: 6px;
            color: var(--text-medium);
        }}
        
        .option-item.correct {{
            background: var(--success-light);
            border-color: var(--success);
        }}
        
        .option-item.correct .option-key {{
            background: var(--success);
            border-color: var(--success);
            color: white;
        }}
        
        .option-item.correct .option-text {{
            color: #166534;
        }}
        
        .option-item.wrong {{
            background: var(--error-light);
            border-color: var(--error);
        }}
        
        .option-item.wrong .option-key {{
            background: var(--error);
            border-color: var(--error);
            color: white;
        }}
        
        .option-item.wrong .option-text {{
            color: #991b1b;
            text-decoration: line-through;
        }}

        /* Navigation */
        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            gap: 16px;
            margin-top: 32px;
            padding-top: 24px;
            border-top: 2px solid var(--border);
        }}

        /* Result Screen */
        .result-header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .result-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 16px;
        }}
        
        .result-score {{
            font-size: 4rem;
            font-weight: 800;
            background: var(--bg-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
        }}
        
        .result-subtitle {{
            color: var(--text-light);
            font-size: 1rem;
        }}
        
        .result-actions {{
            display: flex;
            justify-content: center;
            gap: 16px;
            margin-top: 32px;
        }}

        /* Question List */
        .question-list {{
            margin-top: 40px;
        }}
        
        .question-list-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-dark);
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--border);
        }}
        
        .q-item {{
            background: white;
            border: 2px solid var(--border);
            border-radius: 16px;
            margin-bottom: 16px;
            overflow: hidden;
        }}
        
        .q-item-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 20px;
            font-weight: 600;
        }}
        
        .q-item-header.correct {{
            background: var(--success-light);
            color: #166534;
        }}
        
        .q-item-header.wrong {{
            background: var(--error-light);
            color: #991b1b;
        }}
        
        .q-item-header.unanswered {{
            background: var(--warning-light);
            color: #92400e;
        }}
        
        .q-item-content {{
            padding: 20px;
        }}
        
        .q-item-question {{
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text-dark);
        }}
        
        .q-item-options {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .q-item-option {{
            padding: 12px 16px;
            border-radius: 10px;
            border: 1px solid var(--border);
            font-size: 0.95rem;
        }}
        
        .q-item-option.correct-answer {{
            background: var(--success-light);
            border-color: var(--success);
            color: #166534;
        }}
        
        .q-item-option.user-wrong {{
            background: var(--error-light);
            border-color: var(--error);
            color: #991b1b;
        }}
        
        .answer-summary {{
            margin-top: 12px;
            padding: 12px 16px;
            background: var(--warning-light);
            border-radius: 10px;
            font-size: 0.9rem;
            color: #92400e;
        }}

        @media (max-width: 640px) {{
            body {{
                padding: 10px;
            }}
            
            header {{
                padding: 20px 10px;
            }}
            
            header h1 {{
                font-size: 1.5rem;
            }}
            
            header p {{
                font-size: 0.95rem;
            }}
            
            .card {{
                padding: 20px;
                border-radius: 16px;
            }}
            
            .setup-title {{
                font-size: 1.2rem;
            }}
            
            .nav-buttons {{
                flex-direction: column;
            }}
            
            .btn {{
                width: 100%;
                padding: 16px 20px;
                font-size: 1rem;
            }}
            
            .stats-bar {{
                flex-direction: column;
                gap: 8px;
                text-align: center;
                padding: 12px 16px;
            }}
            
            .question-text {{
                font-size: 1.05rem;
            }}
            
            .option-item {{
                padding: 14px 16px;
            }}
            
            .result-score {{
                font-size: 3rem;
            }}
            
            .result-actions {{
                flex-direction: column;
                gap: 12px;
            }}
            
            .q-item-header {{
                flex-direction: column;
                gap: 8px;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>

<div class="container">
    <header>
        <h1> Ôn Tập Pháp Luật</h1>
        <p>Hệ thống trắc nghiệm ôn thi 5 Cấp độ</p>
    </header>

    <!-- Setup Screen -->
    <div id="setup-screen" class="card">
        <h2 class="setup-title">Chọn Chế Độ Ôn Tập</h2>
        <div class="select-wrapper">
            <label class="select-label">Cấp độ câu hỏi:</label>
            <select id="level-select" class="custom-select">
                <option value="all"> Tất cả (330 câu)</option>
                <optgroup label="CẤP ĐỘ 1 - DỄ">
                    <option value="1"> Đầy đủ Cấp độ 1 (78 câu)</option>
                    <option value="1-1">    ├ Phần 1: Câu 1 → 39</option>
                    <option value="1-2">    └ Phần 2: Câu 40 → 78</option>
                </optgroup>
                <optgroup label="CẤP ĐỘ 2 - TRUNG BÌNH">
                    <option value="2"> Đầy đủ Cấp độ 2 (109 câu)</option>
                    <option value="2-1">    ├ Phần 1: Câu 1 → 36</option>
                    <option value="2-2">    ├ Phần 2: Câu 37 → 72</option>
                    <option value="2-3">    └ Phần 3: Câu 73 → 109</option>
                </optgroup>
                <optgroup label="CẤP ĐỘ 3 - KHÁ">
                    <option value="3"> Đầy đủ Cấp độ 3 (70 câu)</option>
                    <option value="3-1">    ├ Phần 1: Câu 1 → 35</option>
                    <option value="3-2">    └ Phần 2: Câu 36 → 70</option>
                </optgroup>
                <optgroup label="CẤP ĐỘ 4 & 5 - NÂNG CAO">
                    <option value="4"> Cấp độ 4 - Khó (45 câu)</option>
                    <option value="5"> Cấp độ 5 - Rất khó (28 câu)</option>
                </optgroup>
            </select>
        </div>
        <div class="select-wrapper">
            <label class="select-label">Mật khẩu truy cập:</label>
            <input type="password" id="password-input" class="custom-select" placeholder="Nhập mật khẩu để bắt đầu..." style="padding-right: 20px;">
            <p id="password-error" style="color: #ef4444; font-size: 0.9rem; margin-top: 8px; display: none;">Mật khẩu không đúng!</p>
        </div>
        <button class="btn btn-primary btn-block" onclick="startQuiz()">
            Bắt Đầu Làm Bài
        </button>
        <button class="btn btn-secondary btn-block" onclick="startQuickReview()" style="margin-top: 12px;">
            Ôn Nhanh (Xem đáp án)
        </button>
    </div>

    <!-- Result Screen -->
    <div id="result-screen" class="card card-hidden">
        <div class="result-header">
            <h2 class="result-title">Kết Quả Ôn Tập</h2>
            <div class="result-score">
                <span id="final-score">0</span> / <span id="final-total">0</span>
            </div>
            <p class="result-subtitle">Số câu đã trả lời: <span id="final-answered">0</span></p>
        </div>
        
        <div class="result-actions">
            <button class="btn btn-secondary" onclick="resetQuiz()">
                Chọn cấp độ khác
            </button>
            <button id="redo-wrong-btn" class="btn btn-warning" onclick="redoWrongQuestions()" style="display: none;">
                Làm lại câu sai
            </button>
        </div>
        
        <div class="question-list">
            <h3 class="question-list-title">Chi tiet bai lam</h3>
            <div id="question-list"></div>
        </div>
        
        <div style="margin-top: 32px; padding-top: 24px; border-top: 2px solid var(--border); display: flex; flex-direction: column; gap: 12px;">
            <button id="redo-wrong-btn-bottom" class="btn btn-warning btn-block" onclick="redoWrongQuestions()" style="display: none;">
                Lam lai cau sai
            </button>
            <button class="btn btn-primary btn-block" onclick="resetQuiz()">Chon cap do khac</button>
        </div>
    </div>

    <!-- Quiz Screen -->
    <div id="quiz-screen" class="card-hidden">
        <div class="stats-bar">
            <div class="stat-item">
                <span>Câu</span>
                <span class="stat-value"><span id="current-q-num">1</span> / <span id="total-q-num">0</span></span>
            </div>
            <div class="stat-item">
                <span>Điểm</span>
                <span class="stat-value" id="score">0</span>
            </div>
        </div>
        
        <div class="card">
            <div id="question-container"></div>
            
            <div class="nav-buttons">
                <button id="prev-btn" class="btn btn-secondary" onclick="prevQuestion()" disabled>
                    Quay lại
                </button>
                <button id="submit-btn" class="btn btn-warning" onclick="finishQuiz()">
                    Nộp bài
                </button>
                <button id="next-btn" class="btn btn-primary" onclick="nextQuestion()">
                    Tiếp theo
                </button>
            </div>
        </div>
    </div>

    <!-- Quick Review Screen -->
    <div id="quick-review-screen" class="card card-hidden">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; flex-wrap: wrap; gap: 12px;">
            <h2 class="setup-title" style="margin: 0;">Che Do On Nhanh</h2>
            <button class="btn btn-secondary" onclick="resetQuiz()">Quay lai</button>
        </div>
        <p style="color: var(--text-medium); margin-bottom: 20px;">Xem tat ca cau hoi va dap an dung de on tap nhanh.</p>
        <div id="quick-review-list"></div>
        <div style="margin-top: 32px; padding-top: 24px; border-top: 2px solid var(--border); text-align: center;">
            <button class="btn btn-primary btn-block" onclick="resetQuiz()">Chon cap do khac</button>
        </div>
    </div>
</div>

<script>
    const allQuestions = {json_data};
    
    let currentQuestions = [];
    let currentIndex = 0;
    let score = 0;
    let userAnswers = {{}};
    let isReviewMode = false;
    let shuffledOptionsMap = {{}};

    function shuffleArray(array) {{
        const newArr = [...array];
        for (let i = newArr.length - 1; i > 0; i--) {{
            const j = Math.floor(Math.random() * (i + 1));
            [newArr[i], newArr[j]] = [newArr[j], newArr[i]];
        }}
        return newArr;
    }}

    function getFilteredQuestions(selection) {{
        let filtered = [];
        
        if (selection === 'all') {{
            filtered = [...allQuestions];
        }} else if (selection === '1') {{
            filtered = allQuestions.filter(q => q.level === 1);
        }} else if (selection === '2') {{
            filtered = allQuestions.filter(q => q.level === 2);
        }} else if (selection === '3') {{
            filtered = allQuestions.filter(q => q.level === 3);
        }} else if (selection === '4') {{
            filtered = allQuestions.filter(q => q.level === 4);
        }} else if (selection === '5') {{
            filtered = allQuestions.filter(q => q.level === 5);
        }} else if (selection === '1-1') {{
            filtered = allQuestions.filter(q => q.level === 1 && q.id >= 1 && q.id <= 39);
        }} else if (selection === '1-2') {{
            filtered = allQuestions.filter(q => q.level === 1 && q.id >= 40 && q.id <= 78);
        }} else if (selection === '2-1') {{
            filtered = allQuestions.filter(q => q.level === 2 && q.id >= 1 && q.id <= 36);
        }} else if (selection === '2-2') {{
            filtered = allQuestions.filter(q => q.level === 2 && q.id >= 37 && q.id <= 72);
        }} else if (selection === '2-3') {{
            filtered = allQuestions.filter(q => q.level === 2 && q.id >= 73 && q.id <= 109);
        }} else if (selection === '3-1') {{
            filtered = allQuestions.filter(q => q.level === 3 && q.id >= 1 && q.id <= 35);
        }} else if (selection === '3-2') {{
            filtered = allQuestions.filter(q => q.level === 3 && q.id >= 36 && q.id <= 70);
        }}
        
        return filtered;
    }}

    // Password configuration for each level
    const passwords = {{
        'all': '0107',
        '1': '0107',
        '1-1': '0107',
        '1-2': '0107',
        '2': '0107nger',
        '2-1': '0107nger',
        '2-2': '0107nger',
        '2-3': '0107nger',
        '3': '0107nger',
        '3-1': '0107nger',
        '3-2': '0107nger',
        '4': '0107nger',
        '5': '0107nger'
    }};

    function startQuiz() {{
        const levelSelect = document.getElementById('level-select').value;
        const passwordInput = document.getElementById('password-input').value;
        const passwordError = document.getElementById('password-error');
        
        // Validate password
        const correctPassword = passwords[levelSelect];
        if (passwordInput !== correctPassword) {{
            passwordError.style.display = 'block';
            document.getElementById('password-input').style.borderColor = '#ef4444';
            return;
        }}
        
        // Hide error if password is correct
        passwordError.style.display = 'none';
        document.getElementById('password-input').style.borderColor = '#e2e8f0';
        
        currentQuestions = getFilteredQuestions(levelSelect);
        
        if (currentQuestions.length === 0) {{
            alert("Không tìm thấy câu hỏi cho cấp độ này!");
            return;
        }}

        currentIndex = 0;
        score = 0;
        userAnswers = {{}};
        isReviewMode = false;
        shuffledOptionsMap = {{}};
        
        currentQuestions.forEach(q => {{
            const uniqueId = q.id + '_' + q.level;
            shuffledOptionsMap[uniqueId] = shuffleArray(q.options);
        }});
        
        document.getElementById('setup-screen').classList.add('card-hidden');
        document.getElementById('result-screen').classList.add('card-hidden');
        document.getElementById('quiz-screen').classList.remove('card-hidden');
        document.getElementById('submit-btn').style.display = 'inline-flex';
        
        updateStats();
        renderQuestion();
    }}
    
    function resetQuiz() {{
        document.getElementById('result-screen').classList.add('card-hidden');
        document.getElementById('quiz-screen').classList.add('card-hidden');
        document.getElementById('quick-review-screen').classList.add('card-hidden');
        document.getElementById('setup-screen').classList.remove('card-hidden');
    }}

    // Quick Review Mode - View all questions with answers
    function startQuickReview() {{
        const levelSelect = document.getElementById('level-select').value;
        const passwordInput = document.getElementById('password-input').value;
        const passwordError = document.getElementById('password-error');
        
        const correctPassword = passwords[levelSelect];
        if (passwordInput !== correctPassword) {{
            passwordError.style.display = 'block';
            document.getElementById('password-input').style.borderColor = '#ef4444';
            return;
        }}
        
        passwordError.style.display = 'none';
        document.getElementById('password-input').style.borderColor = '#e2e8f0';
        
        const questions = getFilteredQuestions(levelSelect);
        
        if (questions.length === 0) {{
            alert("Không tìm thấy câu hỏi cho cấp độ này!");
            return;
        }}

        document.getElementById('setup-screen').classList.add('card-hidden');
        document.getElementById('quick-review-screen').classList.remove('card-hidden');
        
        renderQuickReview(questions);
    }}

    function renderQuickReview(questions) {{
        const container = document.getElementById('quick-review-list');
        let html = '';
        
        questions.forEach((q, index) => {{
            html += '<div class="q-item">';
            html += '<div class="q-item-header correct">';
            html += '<span>Câu ' + q.id + ' (Cấp độ ' + q.level + ')</span>';
            html += '<span>Đáp án: ' + q.correct_answer + '</span>';
            html += '</div>';
            
            html += '<div class="q-item-content">';
            html += '<div class="q-item-question">' + q.question + '</div>';
            
            html += '<div class="q-item-options">';
            q.options.forEach(opt => {{
                let optClass = 'q-item-option';
                if (opt.key === q.correct_answer) {{
                    optClass += ' correct-answer';
                }}
                html += '<div class="' + optClass + '">';
                html += '<strong>' + opt.key + '.</strong> ' + opt.text;
                if (opt.key === q.correct_answer) {{
                    html += '';
                }}
                html += '</div>';
            }});
            html += '</div>';
            html += '</div>';
            html += '</div>';
        }});
        
        container.innerHTML = html;
    }}

    // Redo Wrong Questions
    function redoWrongQuestions() {{
        const wrongQuestions = currentQuestions.filter(q => {{
            const uniqueId = q.id + '_' + q.level;
            const userAns = userAnswers[uniqueId];
            return userAns && userAns !== q.correct_answer;
        }});
        
        if (wrongQuestions.length === 0) {{
            alert("Không có câu sai để làm lại!");
            return;
        }}
        
        currentQuestions = wrongQuestions;
        currentIndex = 0;
        score = 0;
        userAnswers = {{}};
        isReviewMode = false;
        shuffledOptionsMap = {{}};
        
        currentQuestions.forEach(q => {{
            const uniqueId = q.id + '_' + q.level;
            shuffledOptionsMap[uniqueId] = shuffleArray(q.options);
        }});
        
        document.getElementById('result-screen').classList.add('card-hidden');
        document.getElementById('quiz-screen').classList.remove('card-hidden');
        document.getElementById('submit-btn').style.display = 'inline-flex';
        
        updateStats();
        renderQuestion();
    }}
    
    function finishQuiz() {{
        const unanswered = currentQuestions.length - Object.keys(userAnswers).length;
        if (unanswered > 0) {{
            if (!confirm('Bạn còn ' + unanswered + ' câu chưa trả lời.\\nBạn có chắc chắn muốn nộp bài không?')) {{
                return;
            }}
        }}
        showResults();
    }}
    
    function showResults() {{
        document.getElementById('quiz-screen').classList.add('card-hidden');
        document.getElementById('result-screen').classList.remove('card-hidden');
        
        document.getElementById('final-score').innerText = score;
        document.getElementById('final-total').innerText = currentQuestions.length;
        document.getElementById('final-answered').innerText = Object.keys(userAnswers).length;
        
        // Count wrong answers and show/hide redo button
        const wrongCount = currentQuestions.filter(q => {{
            const uniqueId = q.id + '_' + q.level;
            const userAns = userAnswers[uniqueId];
            return userAns && userAns !== q.correct_answer;
        }}).length;
        
        const redoBtn = document.getElementById('redo-wrong-btn');
        const redoBtnBottom = document.getElementById('redo-wrong-btn-bottom');
        if (wrongCount > 0) {{
            redoBtn.style.display = 'inline-flex';
            redoBtn.innerText = 'Lam lai ' + wrongCount + ' cau sai';
            redoBtnBottom.style.display = 'inline-flex';
            redoBtnBottom.innerText = 'Lam lai ' + wrongCount + ' cau sai';
        }} else {{
            redoBtn.style.display = 'none';
            redoBtnBottom.style.display = 'none';
        }}
        
        renderQuestionList();
    }}
    
    function renderQuestionList() {{
        const container = document.getElementById('question-list');
        let html = '';
        
        currentQuestions.forEach((q, index) => {{
            const uniqueId = q.id + '_' + q.level;
            const userAns = userAnswers[uniqueId];
            
            let statusClass = 'unanswered';
            let statusText = 'Chưa trả lời';
            
            if (userAns) {{
                if (userAns === q.correct_answer) {{
                    statusClass = 'correct';
                    statusText = 'Đúng';
                }} else {{
                    statusClass = 'wrong';
                    statusText = 'Sai';
                }}
            }}
            
            html += '<div class="q-item">';
            html += '<div class="q-item-header ' + statusClass + '">';
            html += '<span>Câu ' + q.id + ' (Cấp độ ' + q.level + ')</span>';
            html += '<span>' + statusText + '</span>';
            html += '</div>';
            
            html += '<div class="q-item-content">';
            html += '<div class="q-item-question">' + q.question + '</div>';
            
            html += '<div class="q-item-options">';
            q.options.forEach(opt => {{
                let optClass = 'q-item-option';
                
                if (opt.key === q.correct_answer) {{
                    optClass += ' correct-answer';
                }} else if (userAns && opt.key === userAns && userAns !== q.correct_answer) {{
                    optClass += ' user-wrong';
                }}
                
                html += '<div class="' + optClass + '">';
                html += '<strong>' + opt.key + '.</strong> ' + opt.text;
                if (opt.key === q.correct_answer) {{
                    html += '';
                }}
                html += '</div>';
            }});
            html += '</div>';
            
            if (userAns && userAns !== q.correct_answer) {{
                html += '<div class="answer-summary">';
                html += '<strong>Bạn chọn:</strong> ' + userAns + ' → <strong>Đáp án đúng:</strong> ' + q.correct_answer;
                html += '</div>';
            }}
            
            html += '</div>';
            html += '</div>';
        }});
        
        container.innerHTML = html;
    }}

    function updateStats() {{
        document.getElementById('current-q-num').innerText = currentIndex + 1;
        document.getElementById('total-q-num').innerText = currentQuestions.length;
        document.getElementById('score').innerText = score;
    }}

    function renderQuestion() {{
        const container = document.getElementById('question-container');
        const q = currentQuestions[currentIndex];
        
        const uniqueId = q.id + '_' + q.level;
        const answeredKey = userAnswers[uniqueId];
        const isAnswered = !!answeredKey;
        
        const shuffledOptions = shuffledOptionsMap[uniqueId] || q.options;

        let optionsHtml = '<div class="options-list">';
        
        shuffledOptions.forEach(opt => {{
            let className = 'option-item';
            
            if (isAnswered) {{
                if (opt.key === q.correct_answer) {{
                    className += ' correct';
                }} else if (opt.key === answeredKey && opt.key !== q.correct_answer) {{
                    className += ' wrong';
                }}
            }}
            
            const canClick = !isAnswered && !isReviewMode;
            const onClickAttr = canClick ? ' onclick="selectAnswer(\\'' + opt.key + '\\')"' : '';
            const cursorStyle = canClick ? '' : ' style="cursor: default;"';
            
            optionsHtml += '<div class="' + className + '"' + cursorStyle + onClickAttr + '>';
            optionsHtml += '<div class="option-key">' + opt.key + '</div>';
            optionsHtml += '<div class="option-text">' + opt.text + '</div>';
            optionsHtml += '</div>';
        }});
        optionsHtml += '</div>';

        let html = '<div class="question-header">';
        html += '<span class="question-badge">Cấp độ ' + q.level + '</span>';
        html += '<span class="question-id">Câu ' + q.id + '</span>';
        html += '</div>';
        html += '<div class="question-text">' + q.question + '</div>';
        html += optionsHtml;
        
        container.innerHTML = html;
        
        document.getElementById('prev-btn').disabled = (currentIndex === 0);
        
        const isLast = (currentIndex === currentQuestions.length - 1);
        const nextBtn = document.getElementById('next-btn');
        nextBtn.innerText = isLast ? 'Hoàn thành →' : 'Tiếp theo →';
        
        if (isReviewMode) {{
            document.getElementById('submit-btn').style.display = 'none';
        }} else {{
            document.getElementById('submit-btn').style.display = 'inline-flex';
        }}
    }}

    function selectAnswer(key) {{
        if (isReviewMode) return;
        
        const q = currentQuestions[currentIndex];
        const uniqueId = q.id + '_' + q.level;
        
        if (userAnswers[uniqueId]) return;
        
        userAnswers[uniqueId] = key;
        
        if (key === q.correct_answer) {{
            score++;
        }}
        
        updateStats();
        renderQuestion();
    }}

    function nextQuestion() {{
        const isLast = (currentIndex === currentQuestions.length - 1);
        if (isLast) {{
            if (isReviewMode) {{
                resetQuiz();
            }} else {{
                finishQuiz();
            }}
        }} else {{
            currentIndex++;
            renderQuestion();
            updateStats();
        }}
    }}

    function prevQuestion() {{
        if (currentIndex > 0) {{
            currentIndex--;
            renderQuestion();
            updateStats();
        }}
    }}

</script>

</body>
</html>'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {output_file} with {len(all_questions)} questions.")

def main():
    base_path = r'e:\DeCuongPhapLuat'
    files = [
        (os.path.join(base_path, 'CauHoi_CapDo1.md'), 1),
        (os.path.join(base_path, 'CauHoi_CapDo2.md'), 2),
        (os.path.join(base_path, 'CauHoi_CapDo3.md'), 3),
        (os.path.join(base_path, 'CauHoi_CapDo4.md'), 4),
        (os.path.join(base_path, 'CauHoi_CapDo5.md'), 5),
    ]
    
    all_questions = []
    for fp, level in files:
        if os.path.exists(fp):
            print(f"Parsing {fp}...")
            qs = parse_markdown_file(fp, level)
            all_questions.extend(qs)
            print(f"  Found {len(qs)} questions.")
        else:
            print(f"File not found: {fp}")
            
    output_html = os.path.join(base_path, 'OnTapPhapLuat.html')
    generate_html(all_questions, output_html)

if __name__ == '__main__':
    main()
