#!/usr/bin/env python3
"""
Example usage of the GitHub Quarterly Board Reporter
"""

import os
from git_summary_tool import GitHubCommitSummarizer
from datetime import datetime, timezone

def example_usage():
    # You can either use environment variables or pass keys directly
    github_token = os.getenv('GITHUB_TOKEN', 'your_github_token_here')
    genai_key = os.getenv('GENAI_API_KEY', 'your_genai_key_here')
    
    # Initialize the summarizer
    repo = "microsoft/vscode"  # Example repository
    summarizer = GitHubCommitSummarizer(github_token, genai_key, repo)
    
    # Define date ranges
    since = "2024-01-01T00:00:00Z"
    until = "2024-06-30T23:59:59Z"
    
    q1_start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    q1_end = datetime(2024, 3, 31, 23, 59, 59, tzinfo=timezone.utc)
    
    try:
        print(f"Fetching commits for {repo}...")
        commits = summarizer.fetch_commits(since, until)
        print(f"Found {len(commits)} commits")
        
        # Categorize by quarters
        q1_text, q2_text = summarizer.categorize_by_quarter(commits, q1_start, q1_end)
        
        # Generate summaries
        if q1_text:
            print("\n=== Q1 2024 Summary ===")
            print(summarizer.summarize_commits(q1_text, "Q1 2024"))
        
        if q2_text:
            print("\n=== Q2 2024 Summary ===")
            print(summarizer.summarize_commits(q2_text, "Q2 2024"))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_usage()
