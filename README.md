# AI Resume Optimizer

A proof of concept AI-powered resume optimization tool using OpenAI GPT-4 for ATS analysis and keyword matching. ** Supports both PDF and text resumes.**

## Overview

This tool analyzes your resume against job descriptions to provide:
- **ATS Alignment Scoring**: Quantifies resume-job match (0 - 100%)
- **Boolean Search Analysis**: Generates recruiter search strings and identifies keyword gaps
- **Actionable Recommendations**: Specific suggestions for resume optimization
- **Automated Resume Rewriting**: AI-powered resume optimization while maintaining authenticity
- **PDF Support**: Extracts text from PDF resumes automatically using pdfplumber

## Features

- **Comprehensive Analysis**: ATS scores, Boolean matching, strengths, gaps, and recommendations
- **PDF & Text Support**: Works with both .pdf and .txt resume files
- **Keyword Gap Detection**: Identifies missing keywords critical for ATS systems
- **Smart Optimization**: Rewrites your resume to better match job descriptions while maintaining honesty
- **File Output**: Saves analysis reports and optimized resumes for easy review
- **Privacy-Focused**: All processing happens via API - your resume stays on your machine

## Tech Stack

- Python 3.11.1
- OpenAI API (GPT-4)
- pdfplumber (PDF text extraction)
- Prompt Engineering

## Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ~$0.50 - 1.00 in OpenAI credits per analysis

## Installation

1. ** Clone the repository**
```bash
git clone https://github.com/dmehta94/ai-resume-optimizer.git
cd ai-resume-optimizer
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate (GitBash on Windows):
source venv/Scripts/activate

# Or Mac/Linux:
source venv/bin/activate

# Or Windows PowerShell:
venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up OpenAI API key**

Create a `.env` file in the project root:
```
OPENAI_API_KEY=sk-your-api-key-here
```


**Never commit your `.env` file to Git!**

## Usage

### Quick Start

1. **Add your resume to the project folder**
   - PDF format: `my_resume.pdf` (recommended)
   - Or text format: `my_resume.txt`

2. ** Run the optimizer**
```bash
python resume_optimizer.py
```

3. **Follow the prompts**
   - Press Enter to use default (`my_resume.pdf`)
   - Or enter path to your resume file
   - Paste the job description when prompted
   - Type `DONE` on a new line when finished
   - Wait 30 - 60 seconds for analysis
   - Choose whether to generate an optimized resume

### Sample Session
```
$python resume_optimizer.py

================================================================================
AI RESUME OPTIMIZER
================================================================================

Enter path to your resume file (.txt or .pdf, default: my_resume.pdf): 

Reading resume from my_resume.pdf...
Detected PDF file, extracting text...
✓ Resume loaded (3247 characters)

================================================================================

Paste the job description below:
(Paste your text below, then type 'DONE' on a new line when finished)
--------------------------------------------------------------------------------
Are you a passionate techie looking to use your personal strengths to help 
shape the future of an international media group? As a Data Science Trainee...
[paste full job description]
DONE

✓ Job description received (2891 characters)

================================================================================
Analyzing resume against job description...
(This may take 30-60 seconds...)
================================================================================

Calling OpenAI API...
✓ Analysis complete!

================================================================================
RESUME ANALYSIS REPORT
================================================================================

ATS ALIGNMENT
-------------
Score: 82%
Summary: Strong technical alignment with machine learning and Python skills...

[Full report displays...]

✓ Saved: analysis_report.txt

Generate optimized resume? (y/n): y

Generating optimized resume...
(This may take 30-60 seconds...)
Calling OpenAI API for resume optimization...
✓ Optimized resume generated
✓ Saved: optimized_resume.txt

================================================================================
COMPLETE!
================================================================================

Output files:
  • analysis_report.txt - Full analysis and recommendations
  • optimized_resume.txt - AI-optimized version of your resume
```

## Supported File Formats

### Resume Files
- **PDF** (`.pdf`) - Automatically extracts text using pdfplumber
- **Text** (`.txt`) - Plain text resumes

### Job Descriptions
- Paste directly into the terminal (any format)
- No file needed - just copy from job posting

## Output files

### `analysis_report.txt`
Comprehensive analysis including:
- ATS alignment score (0 - 100%)
- Boolean search string
- Keywords found vs. missing
- Resume strengths
- Gap analysis
- Actionable recommendations

### `optimized_resume.txt`
AI-rewritten version of your resume that:
- Incorporates missing keywords naturally
- Strengthens weak points
- Emphasizes relevant experience
- Maintains honesty (no fabrication)
- Preserves your voice and tone

## Project Structure
```
ai-resume-optimizer\
├── .env                      # Your API key (not in repo)
├── .gitignore               # Excludes sensitive files
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── resume_optimizer.py      # Main script
├── my_resume.pdf           # Your resume (not in repo)
├── analysis_report.txt     # Generated analysis (not in repo)
└── optimized_resume.txt    # Generated resume (not in repo)
```

## How It Works

1. **PDF Text Extraction**: Uses pdfplumber to extract text from PDF resumes
2. **Input Collection**: Reads resume, accepts pasted job description
3. **API Analysis**: Sends both to GPT-4 with structured prompt
4. **JSON Parsing**: Extracts scores, keywords, gaps, recommendations
5. **Report Generation**: Formats analysis into readable report
6. **Resume Optimization**: (Optional) Generates improved resume based on analysis
7. **File Output**: Saves all results for review.

## Cost Estimate

- Analysis: ~$0.05 - 0.10 per job
- Resume optimization: ~$0.10 - 0.15 per job
- **Total: ~$0.15 - 0.25 per complete analysis**

For 10 job applications: ~$1.50 - 2.50

## Privacy & Security

- Your resume stays on your machine (except API calls)
- API key stored in `.env` (not committed to Git)
- Generated files excluded from Git via `.gitignore`
- OpenAI doesn't train models on API data (as of March 2026)

## Troubleshooting

### PDF text looks garbled
- Some PDFs have text as images (scanned documents)
- Try converting to .txt or use a different PDF

### "No module named 'pdfplumber'"
```bash
pip install pdfplumber
```

### Virtual environment won't activate (GitBash on Windows)
```bash
# Try this syntax:
source venv/Scripts/activate

# Or skip venv and install globally:
pip install -r requirements.txt
```


## Limitations

- Requires active internet connection
- Costs money (OpenAI API credits)
- Quality depends on resume/job description clarity
- Cannot guarantee ATS success (just improves odds)
- Optimizations should be reviewed before use
- PDF extraction quality varies by PDF complexity

## Future Enhancements
- [ ] Batch processing multiple jobs
- [ ] LinkedIn profile and GitHub project integration
- [ ] Save/load analysis history
- [ ] Command-line arguments
- [ ] Web interface
- [ ] Support for Word documents (`.docx`)


## Contributing
This is a personal project, but suggestions welcome via Issues!

## License

MIT License - feel free to use and modify

## Author

**Deval Mehta**
- GitHub: [@dmehta94](https://github.com/dmehta94)
- LinkedIn: [linkedin.com/in/dmehta94](https://linkedin.com/in/dmehta94)

## Acknowledgements

- Built as part of a data science job application process
- Demonstrates practical application of LLMs and prompt engineering
- Created in March 2026 to demonstrate proficiency in building applications with Generative AI
- Support by Claude Sonnet 4.5 for troubleshooting and ideation

---

**Built with GPT-4** 
