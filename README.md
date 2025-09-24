# ai-code-scanner
ARKDOWN
# 🔐 AegisScan – AI-Powered Code Vulnerability Scanner

AegisScan is a Flask-based web application that uses **AI (OpenAI GPT)** and **regex-based scanning** to detect, explain, and fix security vulnerabilities in source code.

You can **upload ZIP files** or **paste code directly**, and the app will:
- Detect vulnerabilities (Command Injection, SQLi, XSS, etc.)
- Generate an AI summary of the issues
- Suggest fixes using GPT
- Show & download cleaned, secure code
- Provide bug bounty scoring based on severity

---

## 🚀 Features

✅ Upload ZIP or Paste Code  
✅ Detect common vulnerabilities via regex  
✅ AI-powered explanation and fix suggestions (OpenAI GPT)  
✅ Full report with severity, details, and fixes  
✅ Download cleaned code and report  
✅ Bug bounty scoring system  
✅ Chart visualization of issues  
✅ Simple Bootstrap UI

---

## 🧱 Project Structure

AegisScan/
├── app.py # Flask backend
├── llm_helper.py # OpenAI GPT logic
├── templates/
│ └── report.html # Result UI
├── static/
│ └── style.css # Optional CSS
├── uploads/ # Uploaded files (auto-created)
├── requirements.txt # Python dependencies
└── .env # (You create this with your OpenAI key)

TEXT

---

## ⚙️ Prerequisites

- Python 3.8 or above
- OpenAI account + API key: https://platform.openai.com/account/api-keys

---

## 🛠️ Installation & Setup

### 1. Clone the repository or download the ZIP

```bash
git clone https://github.com/prasath666/ai-code-scanner.git
cd ai-code-scanner
Or download the repo manually and extract it.

2. Create a virtual environment (optional but recommended)
BASH
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
BASH
pip install -r requirements.txt
4. Create a .env file in the root folder
ENV
OPENAI_API_KEY=your_openai_api_key_here
▶️ How to Run the App
BASH
python app.py
Then open your browser and go to:

TEXT
http://127.0.0.1:5000
🖥️ How to Use
📁 Upload a .zip file containing your source code
📝 Or paste your code directly into the box
Click "Scan"
Wait for the AI to analyze and process
View:
Detected vulnerabilities
Severity report
AI-generated summary
Suggested fixes
Download buttons for report and fixed code
📊 Supported Vulnerability Types
✅ Command Injection (Python, C/C++)
✅ SQL Injection (PHP, Python)
✅ Unsafe eval() usage
✅ Insecure Deserialization
✅ XSS (JavaScript/HTML)
✅ Buffer Overflow (C/C++)
✅ Dangerous Functions (system(), exec(), etc.)
📂 Example Test Cases
Test it with:

Python code using os.system, pickle.load, eval()
PHP files with raw SQL queries
C/C++ code with gets() or sprintf()
📤 Output
📄 Full vulnerability report (AI + regex)
🧠 GPT-explained summary and fixes
🔧 Cleaned/fixed version of the code
💾 Download buttons for both
🧠 Powered by
OpenAI GPT-4 / GPT-3.5
Python Flask
Regex-based static code analysis
Bootstrap (for UI)
📦 Requirements
TEXT
flask
openai
python-dotenv
(Already listed in requirements.txt)

🙋 FAQ
Q: Does it work offline?
A: No. You need an internet connection and a valid OpenAI API key.

Q: What code languages are supported?
A: Regex patterns and GPT handle Python, C/C++, PHP, JavaScript, and Java well.

Q: Is it safe to upload code?
A: Yes. Files are only processed locally and not stored permanently.

📄 License
This project is open-source and free to use under the MIT License.

👤 Author
Made with  by Durga Prasath 


