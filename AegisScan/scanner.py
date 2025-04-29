# scanner.py

import openai

def full_code_analysis(code_text):
    prompt = f"""
You are a cybersecurity expert specialized in vulnerability research and reverse engineering.

Analyze the following Python code and generate a structured vulnerability report with:

1. **Detected Vulnerabilities**
   - Title
   - Description
   - Affected Lines (if possible)
   - Severity: High / Medium / Low
   - CWE ID (if known)
   - Exploitability (1–10)
   - Fix Suggestion

2. **Threat Profile for Each Vulnerability**
   - Threat Actor: (e.g. insider, external hacker)
   - Attack Vector: (e.g. input injection, API abuse)
   - Impact: (e.g. Data leak, RCE)
   - Likelihood: (Low/Medium/High)
   - Reverse Engineering Risk: (Low/Medium/High)

3. **Reverse Engineering Risk**
   - Any signs of obfuscation, dynamic execution, or code hiding
   - Mention techniques like base64, marshal, compile, exec, etc.

Respond in Markdown format with clear sections.

Code:
{code_text}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can switch to "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=2000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
