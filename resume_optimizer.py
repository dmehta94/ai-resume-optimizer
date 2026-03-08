# resume_optimizer.py - Stage 5: Resume Optimization

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

def generate_optimized_resume(resume_text, job_description, analysis):
    """Use GPT-4 to generate an optimized version of the resume"""
    
    prompt = f"""You are an expert resume writer. Based on the analysis below, rewrite this resume to better match the job description.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

ANALYSIS:
- Missing keywords: {', '.join(analysis['keywords_missing'])}
- Gaps: {', '.join(analysis['gaps'])}
- Recommendations: {', '.join(analysis['recommendations'])}

INSTRUCTIONS:
1. Keep the same structure and format as the original
2. Incorporate missing keywords naturally where honest and relevant
3. Strengthen bullet points based on recommendations
4. Emphasize skills and experience that align with the job description
5. Do NOT fabricate experience or skills
6. Maintain the same tone and voice

Return ONLY the optimized resume text, no explanations or preamble.
"""

    try:
        print("Calling OpenAI API for resume optimization...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert resume writer who optimizes resumes for ATS systems while maintaining honesty and authenticity."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=3000
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating optimized resume: {e}")
        return None

def format_analysis_report(analysis):
    """Format the analysis into a readable report"""
    
    report = f"""
{'='*80}
RESUME ANALYSIS REPORT
{'='*80}

ATS ALIGNMENT
-------------
Score: {analysis['ats_alignment_score']}%
Summary: {analysis['ats_summary']}

BOOLEAN SEARCH ANALYSIS
-----------------------
Boolean String: {analysis['boolean_search_string']}

Boolean Match Score: {analysis['boolean_match_score']}%

Keywords Found:
{chr(10).join('  ✓ ' + kw for kw in analysis['keywords_found'])}

Keywords Missing:
{chr(10).join('  ✗ ' + kw for kw in analysis['keywords_missing'])}

STRENGTHS
---------
{chr(10).join('  • ' + s for s in analysis['strengths'])}

GAPS
----
{chr(10).join('  • ' + g for g in analysis['gaps'])}

RECOMMENDATIONS
---------------
{chr(10).join('  ' + str(i+1) + '. ' + r for i, r in enumerate(analysis['recommendations']))}

TARGET BENCHMARKS
-----------------
ATS Alignment: Aim for 80-85% for competitive positioning
Boolean Match: Aim for 75-80% for recruiter visibility

{'='*80}
"""
    return report

def save_output(content, filename):
    """Save content to a file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Saved: {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

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
    
    # Generate and display report
    report = format_analysis_report(analysis)
    print(report)
    
    # Save report
    save_output(report, "analysis_report.txt")
    
    # Ask if user wants optimized resume
    print()
    generate_opt = input("Generate optimized resume? (y/n): ").strip().lower()
    
    if generate_opt == 'y':
        print("\nGenerating optimized resume...")
        print("(This may take 30-60 seconds...)")
        
        optimized_resume = generate_optimized_resume(resume_text, job_description, analysis)
        
        if optimized_resume:
            print("✓ Optimized resume generated")
            save_output(optimized_resume, "optimized_resume.txt")
        else:
            print("Failed to generate optimized resume.")
    
    # Update final output:
    print("\n" + "=" * 80)
    print("COMPLETE!")
    print("=" * 80)
    print("\nOutput files:")
    print("  • analysis_report.txt - Full analysis and recommendations")
    if generate_opt == 'y':
        print("  • optimized_resume.txt - AI-optimized version of your resume")
    print()

if __name__ == "__main__":
    main()
