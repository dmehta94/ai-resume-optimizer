"""
AI Resume Optimizer - Production Version

Analyzes resumes against job descriptions using OpenAI GPT-4 to identify
ATS alignment gaps, missing keywords, and optimization opportunities.

Author: Deval Mehta
Built with: Claude AI (collaboration partner)
Date: March 2026
"""

import os
import sys
import json
from typing import Optional, Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv
import pdfplumber

# Load environment variables
load_dotenv()

# Set encoding to UTF-8 for console output
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configuration constants
OPENAI_MODEL = "gpt-4"
ANALYSIS_TEMPERATURE = 0.3
ANALYSIS_MAX_TOKENS = 2000
OPTIMIZATION_TEMPERATURE = 0.5
OPTIMIZATION_MAX_TOKENS = 3000


def read_pdf(filepath: str) -> Optional[str]:
    """
    Extract text from a PDF file using pdfplumber.
    
    Args:
        filepath: Path to the PDF file to read
        
    Returns:
        Extracted text from all pages, or None if extraction fails
        
    Example:
        >>> text = read_pdf("my_resume.pdf")
        >>> print(len(text))
        3247
    """
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


def read_file(filepath: str) -> Optional[str]:
    """
    Read text from a file, supporting both .txt and .pdf formats.
    
    Automatically detects file type by extension and calls appropriate
    reader function. For PDFs, uses pdfplumber for text extraction.
    
    Args:
        filepath: Path to the file to read (.txt or .pdf)
        
    Returns:
        File contents as string, or None if reading fails
        
    Raises:
        FileNotFoundError: If file doesn't exist at specified path
        
    Example:
        >>> resume = read_file("my_resume.pdf")
        >>> print(f"Loaded {len(resume)} characters")
    """
    try:
        if filepath.lower().endswith('.pdf'):
            print("Detected PDF file, extracting text...")
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


def get_multiline_input(prompt: str) -> str:
    """
    Get multiline input from user via terminal.
    
    Prompts user to paste text and type 'DONE' on a new line when finished.
    Handles both manual typing and copy-paste input.
    
    Args:
        prompt: Message to display to user before input
        
    Returns:
        Combined input from all lines as single string
        
    Example:
        >>> job_desc = get_multiline_input("Paste job description:")
        >>> print(f"Received {len(job_desc)} characters")
    """
    print(prompt)
    print("(Paste your text below, then type 'DONE' on a new line when finished)")
    print("-" * 80)
    
    lines: List[str] = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'DONE':
                break
            lines.append(line)
        except EOFError:
            break
    
    return '\n'.join(lines)


def analyze_resume(resume_text: str, job_description: str) -> Optional[Dict[str, Any]]:
    """
    Analyze resume against job description using GPT-4.
    
    Sends resume and job description to OpenAI GPT-4 with a structured prompt
    requesting JSON output containing ATS scores, keyword analysis, Boolean
    search strings, and recommendations.
    
    Args:
        resume_text: Full text content of the resume
        job_description: Full text of the job posting
        
    Returns:
        Dictionary containing analysis results with keys:
            - ats_alignment_score (int): 0-100 score
            - ats_summary (str): Explanation of score
            - boolean_search_string (str): Recruiter search query
            - boolean_match_score (int): 0-100 score
            - keywords_found (list): Keywords present in resume
            - keywords_missing (list): Keywords absent from resume
            - strengths (list): Resume strengths for this role
            - gaps (list): Areas needing improvement
            - recommendations (list): Specific action items
        Returns None if API call fails
        
    Example:
        >>> analysis = analyze_resume(resume_text, job_desc)
        >>> print(f"ATS Score: {analysis['ats_alignment_score']}%")
    """
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
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS analyzer and resume optimization specialist."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=ANALYSIS_TEMPERATURE,
            max_tokens=ANALYSIS_MAX_TOKENS
        )
        
        result = response.choices[0].message.content.strip()
        
        # Clean up markdown formatting that GPT-4 sometimes adds
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


def generate_optimized_resume(
    resume_text: str,
    job_description: str,
    analysis: Dict[str, Any]
) -> Optional[str]:
    """
    Generate an optimized version of the resume using GPT-4.
    
    Uses analysis results to create an improved resume that better matches
    the job description while maintaining authenticity. Incorporates missing
    keywords naturally and strengthens existing bullet points.
    
    Args:
        resume_text: Original resume content
        job_description: Target job posting text
        analysis: Analysis results from analyze_resume()
        
    Returns:
        Optimized resume text, or None if generation fails
        
    Note:
        The optimization maintains the original structure and does not
        fabricate experience. All suggestions should be manually reviewed
        before use.
        
    Example:
        >>> optimized = generate_optimized_resume(resume, job_desc, analysis)
        >>> with open("optimized_resume.txt", "w") as f:
        >>>     f.write(optimized)
    """
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
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert resume writer who optimizes resumes for ATS systems while maintaining honesty and authenticity."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=OPTIMIZATION_TEMPERATURE,
            max_tokens=OPTIMIZATION_MAX_TOKENS
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error generating optimized resume: {e}")
        return None


def format_analysis_report(analysis: Dict[str, Any]) -> str:
    """
    Format analysis results into a human-readable text report.
    
    Converts the structured JSON analysis into a formatted report with
    sections for ATS alignment, Boolean search analysis, keywords,
    strengths, gaps, and recommendations.
    
    Args:
        analysis: Analysis dictionary from analyze_resume()
        
    Returns:
        Formatted report as string ready for display or file output
        
    Example:
        >>> report = format_analysis_report(analysis)
        >>> print(report)
        >>> with open("analysis_report.txt", "w") as f:
        >>>     f.write(report)
    """
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


def save_output(content: str, filename: str) -> None:
    """
    Save content to a file with UTF-8 encoding.
    
    Args:
        content: Text content to write to file
        filename: Path/name of output file
        
    Returns:
        None
        
    Example:
        >>> save_output(report, "analysis_report.txt")
        ✓ Saved: analysis_report.txt
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Saved: {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")


def main() -> None:
    """
    Main execution flow for the AI Resume Optimizer.
    
    Orchestrates the complete workflow:
    1. Prompts user for resume file path
    2. Reads and validates resume content
    3. Prompts for job description
    4. Calls GPT-4 for analysis
    5. Displays and saves analysis report
    6. Optionally generates optimized resume
    
    Returns:
        None
        
    Example:
        >>> python resume_optimizer.py
        [Interactive prompts follow]
    """
    print("=" * 80)
    print("AI RESUME OPTIMIZER")
    print("=" * 80)
    print()
    
    # Get resume
    resume_file = input(
        "Enter path to your resume file (.txt or .pdf, default: my_resume.pdf): "
    ).strip()
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
        
        optimized_resume = generate_optimized_resume(
            resume_text,
            job_description,
            analysis
        )
        
        if optimized_resume:
            print("✓ Optimized resume generated")
            save_output(optimized_resume, "optimized_resume.txt")
        else:
            print("Failed to generate optimized resume.")
    
    # Final output summary
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
