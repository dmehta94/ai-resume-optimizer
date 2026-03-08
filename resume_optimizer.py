# resume_optimizer.py - Stage 3: OpenAI integration

# Import necessary libraries and modules
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import json
import pdfplumber

# Load environment variables
load_dotenv()

# Set encoding to UTF-8 for console printout
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def read_pdf(filepath):
    """Extract text from a PDF file using pdfplumber"""
    try:
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def read_file(filepath):
    """Read text from a file (supports .txt and .pdf)"""
    try:
        if filepath.lower().endswith('.pdf'):
            print(f"Detected PDF file, extracting text...")
            return read_pdf(filepath)
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
    except FileNotFoundError:
        print(f"Error: Could not find file {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def get_multiline_input(prompt):
    """Get multiline input from user"""
    print(prompt)
    print("(Paste your text below, then type 'DONE' on a new line when finished)")
    print("-" * 80)
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            lines.append(line)
        except EOFError:
            break
    
    return '\n'.join(lines)

def analyze_resume(resume_text, job_description):
    """Use GPT-4 to analyze resume against job description"""
    
    prompt = f"""You are an expert ATS (Applicant Tracking System) analyzer and resume coach. 
Analyze the following resume against the job description and provide a comprehensive report.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide your analysis in the following JSON format:
{{
    "ats_alignment_score": <number 0-100>,
    "ats_summary": "<brief explanation of score>",
    
    "boolean_search_string": "<complete Boolean search string a recruiter would use>",
    "boolean_match_score": <number 0-100>,
    "keywords_found": ["keyword1", "keyword2", ...],
    "keywords_missing": ["keyword1", "keyword2", ...],
    
    "strengths": ["strength1", "strength2", "strength3"],
    "gaps": ["gap1", "gap2", "gap3"],
    
    "recommendations": [
        "recommendation1",
        "recommendation2",
        "recommendation3"
    ]
}}

Be specific and actionable. Focus on concrete skills, keywords, and experience mentioned in both documents.
"""

    try:
        print("Calling OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert ATS analyzer and resume optimization specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content.strip()
        
        # Clean up markdown formatting
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()
        
        return json.loads(result)
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def main():
    """Main execution flow"""
    print("=" * 80)
    print("AI RESUME OPTIMIZER")
    print("=" * 80)
    print()
    
    # Get resume
    resume_file = input("Enter path to your resume file (.txt or .pdf, default: my_resume.pdf): ").strip()
    if not resume_file:
        resume_file = "my_resume.pdf"
    
    print(f"\nReading resume from {resume_file}...")
    resume_text = read_file(resume_file)
    
    if not resume_text:
        print("Failed to read resume file. Exiting.")
        return
    
    print(f"✓ Resume loaded ({len(resume_text)} characters)")
    
    # Get job description
    print("\n" + "=" * 80)
    job_description = get_multiline_input("\nPaste the job description below:")
    
    if not job_description.strip():
        print("\nNo job description provided. Exiting.")
        return
    
    print(f"\n✓ Job description received ({len(job_description)} characters)")
    
    # Analyze
    print("\n" + "=" * 80)
    print("Analyzing resume against job description...")
    print("(This may take 30-60 seconds...)")
    print("=" * 80)
    
    analysis = analyze_resume(resume_text, job_description)
    
    if not analysis:
        print("Failed to analyze resume. Exiting.")
        return
    
    print("\n✓ Analysis complete!")
    print("\nRaw JSON output:")
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
