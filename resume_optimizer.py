# resume_optimizer.py - Stage 2: File Reading with PDF Support

# Import necessary libraries and modules
import os
import sys
from dotenv import load_dotenv
import pdfplumber

# Load environment variables
load_dotenv()

# Set encoding to UTF-8 for console printout
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

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
            # Read as text file
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

def main():
    """Main execution flow"""
    print("=" * 80)
    print("AI RESUME OPTIMIZER")
    print("=" * 80)
    print()
    
    # Get resume from file
    resume_file = input("Enter path to your resume file (.txt or .pdf, default: my_resume.pdf): ").strip()
    if not resume_file:
        resume_file = "my_resume.pdf"
    
    print(f"\nReading resume from {resume_file}...")
    resume_text = read_file(resume_file)
    
    if not resume_text:
        print("Failed to read resume file. Exiting.")
        return
    
    print(f"✓ Resume loaded ({len(resume_text)} characters)")
    
    # Get job description via paste
    print("\n" + "=" * 80)
    job_description = get_multiline_input("\nPaste the job description below:")
    
    if not job_description.strip():
        print("\nNo job description provided. Exiting.")
        return
    
    print(f"\n✓ Job description received ({len(job_description)} characters)")
    print("\n✓ Ready for analysis (not yet implemented)")

if __name__ == "__main__":
    main()
