import os
from openai import OpenAI
from dotenv import load_dotenv

# ---------------------------------------------------
# Load environment variables
# ---------------------------------------------------

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------------------
# 1. High-Level Summary (Simple Explanation)
# ---------------------------------------------------

def explain_issues(raw_report):
    """
    Generates a beginner-friendly summary of vulnerabilities
    from the scanned code report.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return "❌ OpenAI API key not found. Please set it in the .env file."

    prompt = f"""
You are a cybersecurity expert.

Analyze the following vulnerability report and explain the important issues in beginner-friendly language.

Only explain REAL security issues. If no issues, say "No significant vulnerabilities found."

Here is the report:

{raw_report}

Give a clean, beginner-friendly explanation:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful cybersecurity assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error contacting OpenAI: {str(e)}"

# ---------------------------------------------------
# 2. Detailed Fixes with Code Examples
# ---------------------------------------------------

def explain_with_fixes(raw_report):
    """
    Analyzes code and returns a detailed vulnerability report,
    including explanations and fixed code examples.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return "❌ OpenAI API key not found. Please set it in the .env file."

    prompt = f"""
You are a cybersecurity expert.

Analyze the following code and explain any real vulnerabilities in beginner-friendly terms.

Then, provide secure, fixed versions of the code with explanations.

ONLY include real vulnerabilities. If nothing is wrong, say "No significant vulnerabilities found."

Code to analyze:

{raw_report}

Return your output in this format:

1. [Vulnerability Name]
   - What is happening:
   - Why it's a problem:
   - How to fix it:
   - 💡 Fix example code (clean and safe):

Conclusion:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful cybersecurity assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error contacting OpenAI: {str(e)}"

def extract_fixed_code(fix_suggestions):
    """
    Extracts fixed code blocks from the GPT response.
    Looks for lines after '💡 Fix example code (clean and safe):'
    """
    lines = fix_suggestions.splitlines()
    fixed_blocks = []
    inside_block = False
    current_block = []

    for line in lines:
        if "💡 Fix example code" in line:
            inside_block = True
            current_block = []
            continue
        if inside_block:
            if line.strip() == "" and current_block:
                fixed_blocks.append("\n".join(current_block).strip())
                inside_block = False
            else:
                current_block.append(line)
    if current_block:
        fixed_blocks.append("\n".join(current_block).strip())
    return "\n\n".join(fixed_blocks).strip()
