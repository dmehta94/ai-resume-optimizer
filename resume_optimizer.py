# resume_optimizer.py - Stage 1: Project Structure

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set encoding to UTF-8 for console printout
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

def main():
    """Main execution flow"""
    print("=" * 80)
    print("AI RESUME OPTIMIZER")
    print("=" * 80)
    print()
    print("✓ Environment loaded")
    print(f"✓ API Key present: {bool(os.getenv('OPENAI_API_KEY'))}")

if __name__ == "__main__":
    main()
