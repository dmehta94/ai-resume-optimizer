# AI Resume Optimizer

AI-powered resume analysis using OpenAI GPT-4 to identify ATS gaps, missing keywords, and optimization opportunities for job applications.

**Author:** Deval Mehta  
**Built with:** Claude AI (collaboration partner)  
**Stack:** Python, OpenAI API, pdfplumber  
**Context:** Portfolio project for data science job search (March 2026)

---

## What It Does

Analyzes your resume against a job description and provides:
- **ATS Alignment Score** (0-100%) - How well your resume matches the job
- **Keyword Gap Analysis** - What critical terms are missing
- **Boolean Search String** - How recruiters might search for candidates
- **AI-Optimized Resume** - Suggested improvements (optional, requires review)

**Example output:**
```
ATS Alignment: 82%
Boolean Match: 76%

Keywords Found: Python, SQL, Machine Learning, scikit-learn, TensorFlow
Keywords Missing: Generative AI, AWS, Docker

Recommendations:
1. Add generative AI project to demonstrate LLM experience
2. Include cloud platform keywords (AWS/Azure/GCP)
3. Emphasize "problem-solving mindset" in summary
```

---

## Why I Built This

**Context:** I was applying to data science roles (including Bertelsmann Future Leaders Graduate Program) and manually comparing my resume against 10+ job descriptions—spending 2 hours per application trying to spot keyword gaps and optimize for ATS systems.

**Problem:** Manual optimization is slow, subjective, and inconsistent. Hard to see yourself from a recruiter's perspective.

**Solution:** Automated the analysis using GPT-4's semantic understanding to:
- Score resume-job alignment quantitatively
- Identify specific missing keywords
- Generate recruiter Boolean search strings
- Suggest optimizations while maintaining authenticity

**Results:**
- Used for 15+ applications
- Improved my own resume from 72% → 85% ATS alignment
- Identified blind spots (missing "generative AI" despite having experience)
- Reduced analysis time from ~2 hours → 5 minutes per job

**Cost:** ~$0.20 per analysis (acceptable for job search)

---

## Quick Start

**Install:**
```bash
git clone https://github.com/dmehta94/ai-resume-optimizer.git
cd ai-resume-optimizer
pip install -r requirements.txt
```

**Configure:**
```bash
# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

**Run:**
```bash
python resume_optimizer.py
```

Then:
1. Press Enter to use `my_resume.pdf` (or specify different file)
2. Paste job description
3. Type `DONE`
4. Review analysis (saved to `analysis_report.txt`)
5. Optionally generate optimized resume (saved to `optimized_resume.txt`)

---

## What I Learned

**Technical:**
- **Prompt engineering:** Getting consistent structured JSON from GPT-4 (had to handle markdown code block wrapping)
- **PDF extraction:** Text-based vs. scanned PDFs have different challenges
- **Error handling:** Graceful degradation and clear user feedback matter
- **Type hints:** Make code self-documenting, easier to debug

**Data Science:**
- LLMs excel at semantic analysis but need careful prompting
- Validation critical—GPT-4 occasionally hallucinates keywords
- Automation vs. judgment trade-off: AI suggests, humans decide
- ATS systems are literal—need exact keyword matches, not just semantic similarity

**Software Engineering:**
- Separation of concerns (read_file, analyze_resume, generate_optimized_resume)
- Google-style docstrings improve code clarity
- User experience matters even in CLI tools

**Unexpected:**
- Building this revealed I was underselling my collaboration skills on my own resume
- Hardest part: prompting GPT-4 to improve resumes WITHOUT fabricating experience
- Resume writing is more pattern-matching than I expected

---

## How It Works

**Architecture:**
```
Resume (PDF/TXT) + Job Description
    ↓
PDF text extraction (pdfplumber)
    ↓
GPT-4 analysis with structured prompt
    ↓
JSON response parsing
    ↓
Formatted report + optional optimized resume
```

**Key functions:**
- `read_pdf()` - Extract text from PDF
- `analyze_resume()` - Send to GPT-4, get structured analysis
- `generate_optimized_resume()` - Create improved version
- `format_analysis_report()` - Format JSON into readable text

**Tech stack:**
- `openai` - GPT-4 API
- `pdfplumber` - PDF text extraction
- `python-dotenv` - Environment variables

---

## Limitations

- Costs ~$0.20 per analysis (OpenAI API)
- Requires manual review of AI suggestions
- Scanned/image PDFs won't work (need OCR)
- Single job at a time (no batch processing)
- AI can over-optimize or suggest irrelevant keywords

---

## Sample Output

Files generated:
- `analysis_report.txt` - Full analysis with scores and recommendations
- `optimized_resume.txt` - AI-improved version (if requested)

The analysis includes:
- ATS alignment score and summary
- Boolean search string recruiters might use
- Keywords found vs. missing
- Specific strengths for this role
- Gaps to address
- Actionable recommendations

---

## Future Ideas

If I continue this:
- [ ] GitHub integration (pull repos/languages automatically)
- [ ] Batch processing (one resume vs. multiple jobs)
- [ ] Cover letter generation
- [ ] LinkedIn data import
- [ ] Cost tracking

---

## Credits

**Author:** Deval Mehta  
**Collaboration partner:** Claude AI (Anthropic)

Built in collaboration with Claude AI for:
- Code review and architecture decisions
- Prompt engineering refinement
- Documentation structure

This human-AI collaboration was appropriate for a tool that itself uses LLMs—and reflects how modern software development increasingly works.

**Built with:**
- [OpenAI GPT-4](https://openai.com/gpt-4)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Claude AI](https://claude.ai)

---

## License

MIT License - Free to use and modify

Copyright (c) 2026 Deval Mehta

---

## Contact

**Deval Mehta**  
Data Scientist | Machine Learning

- GitHub: [@dmehta94](https://github.com/dmehta94)
- LinkedIn: [linkedin.com/in/dmehta94](https://linkedin.com/in/dmehta94)

Questions or suggestions? Open an issue or reach out on LinkedIn.

---

*Portfolio project built during data science job search, March 2026*
