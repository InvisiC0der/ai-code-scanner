# AegisScan – AI-Powered Code Vulnerability Scanner

AegisScan is a Flask-based web application that uses AI (OpenAI GPT) and regex-based scanning to detect, explain, and fix security vulnerabilities in source code.

You can upload ZIP files or paste code directly, and the application will:
- Detect vulnerabilities such as Command Injection, SQL Injection, and XSS
- Generate an AI summary of detected issues
- Suggest fixes using AI
- Provide cleaned and secured code for download
- Generate severity scoring similar to bug bounty reports

---

## Features

- Upload ZIP files or paste source code
- Detect common vulnerabilities using regex scanning
- AI-powered explanations and remediation suggestions
- Detailed report including severity levels and fixes
- Downloadable cleaned code and analysis report
- Vulnerability scoring system
- Visualization charts for issue distribution
- Simple Bootstrap-based interface

---

## Project Structure

AegisScan/
├── app.py  
├── llm_helper.py  
├── templates/  
│   └── report.html  
├── static/  
│   └── style.css  
├── uploads/  
├── requirements.txt  
└── .env  

---

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

---

## Installation and Setup

### Clone Repository
git clone https://github.com/prasath666/ai-code-scanner.git  
cd ai-code-scanner

### Create Virtual Environment (Optional)
python -m venv venv

Activate environment:

Windows:  
venv\Scripts\activate  

Linux / macOS:  
source venv/bin/activate

### Install Dependencies
pip install -r requirements.txt

### Create Environment File

Create a `.env` file in the root directory:

OPENAI_API_KEY=your_api_key_here

---

## Running the Application

python app.py

Open browser and visit:  
http://127.0.0.1:5000

---

## Usage

1. Upload a ZIP file containing source code or paste code directly.
2. Click Scan.
3. Wait for analysis.
4. View results including:
   - Detected vulnerabilities
   - Severity report
   - AI-generated explanations
   - Suggested fixes
5. Download cleaned code or report if needed.

---

## Supported Vulnerability Types

- Command Injection
- SQL Injection
- Unsafe eval usage
- Insecure Deserialization
- Cross-Site Scripting (XSS)
- Buffer Overflow
- Dangerous system functions

Supported languages include Python, C, C++, PHP, JavaScript, and Java.

---

## Example Test Inputs

- Python scripts using os.system, eval, or pickle.load
- PHP files with raw SQL queries
- C/C++ programs using unsafe functions such as gets or sprintf

---

## Output

- Full vulnerability report
- AI-generated explanations and fixes
- Secure version of analyzed code
- Downloadable files

---

## Technology Stack

- Python
- Flask
- OpenAI API
- Regex-based static analysis
- Bootstrap

---

## Requirements

flask  
openai  
python-dotenv  

---

## FAQ

Does it work offline?  
No. Internet access and a valid API key are required.

Which languages are supported?  
Python, C, C++, PHP, JavaScript, and Java.

Is uploaded code stored?  
No. Files are processed locally and not permanently stored.

---

## Author

Durga Prasath
