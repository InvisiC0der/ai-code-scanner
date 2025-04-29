# app.py
import os
import zipfile
import openai
import json
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from llm_helper import explain_issues, explain_with_fixes, extract_fixed_code
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound

def detect_language_from_code(code):
    try:
        lexer = guess_lexer(code)
        return lexer.name
    except ClassNotFound:
        return "Unknown"

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORT_FOLDER'] = 'reports'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)

SUPPORTED_EXTENSIONS = ('.py', '.java', '.c', '.cpp', '.js', '.html', '.php')

RISKY_PATTERNS = {
    "Command Injection (Python)": ["os.system(", "subprocess.Popen(", "shell=True"],
    "Deserialization (Python)": ["pickle.load", "yaml.load"],
    "Eval/Exec (Python)": ["eval(", "exec("],
    "Buffer Overflow (C/C++)": ["gets(", "strcpy(", "scanf(", "sprintf("],
    "Command Execution (C/C++)": ["system("],
    "Command Execution (Java)": ["Runtime.getRuntime().exec("],
    "Deserialization (Java)": ["ObjectInputStream", "readObject("],
    "DOM Injection (JS/HTML)": ["innerHTML", "document.write(", "eval(", "setTimeout("],
    "Insecure JS Functions": ["Function(", "new Function("],
    "Insecure PHP Code": ["eval(", "include(", "require(", "$_GET", "$_POST"],
}

def analyze_with_ai(code_line, language="Unknown"):
    try:
        prompt = f"Analyze this {language} code for security issues:\n\n{code_line}\n\n" \
                 f"Give output using:\n[Risk] <severity>\n[Why] <why it's risky>\n[Fix] <suggested fix>"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.4,
        )
        content = response['choices'][0]['message']['content']
        lines = content.strip().split("\n")
        output = {"severity": "Unknown", "why": "", "fix": ""}
        for line in lines:
            if line.startswith("[Risk]"):
                output["severity"] = line.replace("[Risk]", "").strip()
            elif line.startswith("[Why]"):
                output["why"] = line.replace("[Why]", "").strip()
            elif line.startswith("[Fix]"):
                output["fix"] = line.replace("[Fix]", "").strip()
        return output
    except Exception as e:
        return {"severity": "Unknown", "why": "Error reaching AI", "fix": str(e)}

def detect_language(file_name):
    ext = file_name.split('.')[-1]
    return {
        'py': 'Python',
        'java': 'Java',
        'c': 'C',
        'cpp': 'C++',
        'js': 'JavaScript',
        'html': 'HTML',
        'php': 'PHP'
    }.get(ext, 'Unknown')

def calculate_score(issues):
    score = 100
    for issue in issues:
        sev = issue.get("severity", "").lower()
        if sev == "high":
            score -= 10
        elif sev == "medium":
            score -= 5
        elif sev == "low":
            score -= 2
    return max(score, 0)

def get_issue_data(issues):
    categories = list(RISKY_PATTERNS.keys())
    counts = [sum(1 for issue in issues if issue['category'] == cat) for cat in categories]
    return {'labels': categories, 'counts': counts}

def save_report(filepath, issues, summary=None, fixes=None, fixed_code=None):
    with open(filepath, 'w', encoding='utf-8') as f:
        for issue in issues:
            f.write(f"{issue['file']} — line {issue['line_number']}: {issue['code']}\n")
            f.write(f"  Category: {issue.get('category', 'N/A')}\n")
            f.write(f"  Risk: {issue.get('severity', 'N/A')}\n")
            f.write(f"  Why: {issue.get('why', 'N/A')}\n")
            f.write(f"  Fix: {issue.get('fix', 'N/A')}\n")
            f.write("-" * 40 + "\n")

        if summary:
            f.write("\n\n=== AI Summary ===\n")
            f.write(summary.strip() + "\n")

        if fixes:
            f.write("\n\n=== AI Fix Suggestions ===\n")
            f.write(fixes.strip() + "\n")

        if fixed_code:
            f.write("\n\n=== Cleaned Fixed Code ===\n")
            f.write(fixed_code.strip() + "\n")

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('zip_file')
        if not file or not file.filename.endswith('.zip'):
            flash('Please upload a valid .zip file.', 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        extract_folder = os.path.join(app.config['UPLOAD_FOLDER'], filename[:-4])
        os.makedirs(extract_folder, exist_ok=True)

        with zipfile.ZipFile(upload_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        all_code = ""
        issues = []
        for root, dirs, files in os.walk(extract_folder):
            for file in files:
                if file.endswith(SUPPORTED_EXTENSIONS):
                    language = detect_language(file)
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        all_code += ''.join(lines)
                        for i, line in enumerate(lines, start=1):
                            for category, patterns in RISKY_PATTERNS.items():
                                for pattern in patterns:
                                    if pattern in line:
                                        result = analyze_with_ai(line.strip(), language)
                                        highlighted_code = line.strip()
                                        for p in patterns:
                                            if p in highlighted_code:
                                                highlighted_code = highlighted_code.replace(
                                                    p,
                                                    f'<span class="highlight-risk-pattern">{p}</span>'
                                                )
                                                break
                                        issues.append({
                                            'file': file,
                                            'line_number': i,
                                            'code': highlighted_code,
                                            'category': category,
                                            'severity': result['severity'],
                                            'why': result['why'],
                                            'fix': result['fix']
                                        })

        score = calculate_score(issues)
        summary = explain_issues(all_code)
        fix_suggestions = explain_with_fixes(all_code)
        fixed_code = extract_fixed_code(fix_suggestions)
        issue_data = get_issue_data(issues)
        report_path = os.path.join(app.config['REPORT_FOLDER'], filename[:-4] + '.txt')
        save_report(report_path, issues, summary, fix_suggestions, fixed_code)

        fixed_file_path = os.path.join(app.config['REPORT_FOLDER'], f"fixed_{filename}.txt")
        with open(fixed_file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_code)

        flash("✅ ZIP scan complete! Report generated below.", "success")
        return render_template("report.html", issues=issues, filename=filename, issue_data=issue_data, score=score, summary=summary, fix_suggestions=fix_suggestions, fixed_code=fixed_code)

    return render_template("upload.html")

@app.route("/paste_scan", methods=["GET", "POST"])
def paste_scan():
    if request.method == "POST":
        pasted_code = request.form.get("code")
        if not pasted_code.strip():
            flash("Please paste code before scanning.", "danger")
            return redirect(url_for("paste_scan"))

        language = detect_language_from_code(pasted_code)

        issues = []
        lines = pasted_code.split('\n')
        for i, line in enumerate(lines, start=1):
            for category, patterns in RISKY_PATTERNS.items():
                for pattern in patterns:
                    if pattern in line:
                        result = analyze_with_ai(line.strip(), language)
                        highlighted_code = line.strip()
                        for p in patterns:
                            if p in highlighted_code:
                                highlighted_code = highlighted_code.replace(
                                    p,
                                    f'<span class="highlight-risk-pattern">{p}</span>'
                                )
                                break
                        issues.append({
                            'file': 'Pasted Code',
                            'line_number': i,
                            'code': highlighted_code,
                            'category': category,
                            'severity': result['severity'],
                            'why': result['why'],
                            'fix': result['fix']
                        })

        score = calculate_score(issues)
        all_code = "\n".join([issue['code'] for issue in issues])
        summary = explain_issues(all_code)
        fix_suggestions = explain_with_fixes(all_code)
        fixed_code = extract_fixed_code(fix_suggestions)
        issue_data = get_issue_data(issues)
        filename = 'pasted_code'

        report_path = os.path.join(app.config['REPORT_FOLDER'], f"{filename}.txt")
        save_report(report_path, issues, summary, fix_suggestions, fixed_code)

        fixed_file_path = os.path.join(app.config['REPORT_FOLDER'], f"fixed_{filename}.txt")
        with open(fixed_file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_code)

        flash("✅ Code scan complete! Report generated below.", "success")
        return render_template("report.html", issues=issues, filename=filename, issue_data=issue_data, score=score, summary=summary, fix_suggestions=fix_suggestions, fixed_code=fixed_code)

    return render_template("paste_scan.html")

@app.route('/download_report/<filename>')
def download_report(filename):
    filename = filename.replace('.zip', '').replace('.py', '') + '.txt'
    path = os.path.join(app.config['REPORT_FOLDER'], filename)
    if os.path.exists(path):
        return send_from_directory(app.config['REPORT_FOLDER'], filename, as_attachment=True)
    else:
        flash("Report not found.", "danger")
        return redirect(url_for('home'))

@app.route('/bug_bounty', methods=['POST'])
def bug_bounty():
    issues_json = request.form.get('issues')
    score = int(request.form.get('score', 100))
    issues = json.loads(issues_json)
    high = sum(1 for i in issues if i['severity'].lower() == 'high')
    medium = sum(1 for i in issues if i['severity'].lower() == 'medium')
    low = sum(1 for i in issues if i['severity'].lower() == 'low')

    reward = "$0"
    if high >= 1:
        reward = "$300"
    elif medium >= 1:
        reward = "$150"
    elif low >= 1:
        reward = "$50"

    return render_template("bug_bounty.html", score=score, issues=issues, high=high, medium=medium, low=low, reward=reward)

@app.route('/report')
def report():
    flash("📄 No new scan, this is just a placeholder report.", "info")
    return render_template('report.html', issues=[], filename="placeholder", issue_data={}, score=100, summary="No summary", fix_suggestions="No fix suggestions", fixed_code="No fixed code")

@app.errorhandler(404)
def not_found_error(error):
    flash("⚠️ Page not found.", "warning")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
