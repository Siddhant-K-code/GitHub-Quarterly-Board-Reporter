import os
import requests
import google.generativeai as genai
from datetime import datetime, timezone
from dateutil.parser import parse
import argparse

class GitHubCommitSummarizer:
    def __init__(self, github_token, genai_api_key, repo):
        self.github_token = github_token
        self.repo = repo
        self.headers = {"Authorization": f"token {github_token}"}
        self.per_page = 100
        
        genai.configure(api_key=genai_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def fetch_commits(self, since, until):
        all_commits = []
        page = 1
        while True:
            url = f"https://api.github.com/repos/{self.repo}/commits"
            params = {
                "since": since,
                "until": until,
                "per_page": self.per_page,
                "page": page
            }
            r = requests.get(url, headers=self.headers, params=params)
            if r.status_code != 200:
                raise Exception(f"GitHub API error: {r.text}")
            commits = r.json()
            if not commits:
                break
            all_commits.extend(commits)
            if len(commits) < self.per_page:
                break
            page += 1
        return all_commits

    def categorize_by_quarter(self, commits, q1_start, q1_end):
        q1, q2 = [], []
        
        for c in commits:
            date = parse(c['commit']['author']['date'])
            msg = c['commit']['message'].splitlines()[0]
            if q1_start <= date <= q1_end:
                q1.append(f"- {msg}")
            elif date > q1_end:
                q2.append(f"- {msg}")
        return "\n".join(q1), "\n".join(q2)

    def summarize_commits(self, commits_text, period_name, custom_prompt=None):
        if custom_prompt:
            prompt = custom_prompt.format(commits=commits_text, period=period_name)
        else:
            prompt = f"""
You're summarizing development work for {period_name}. This is for a team presentation. Focus on user-facing changes, product improvements, and significant technical work.

Here are the commit messages:
{commits_text}

Summarize under these sections:
- 🚀 New features and improvements
- 🐛 Bug fixes and stability
- 📈 Performance and infrastructure
- 🔒 Security and compliance
- 📚 Documentation and tooling

Only include relevant and valuable changes. Be clear and concise.
"""
        response = self.model.generate_content(prompt)
        return response.text.strip()

def main():
    parser = argparse.ArgumentParser(description='Generate quarterly board reports from GitHub commits')
    parser.add_argument('--repo', required=True, help='GitHub repository in format owner/repo')
    parser.add_argument('--since', required=True, help='Start date in ISO format (e.g., 2025-01-15T00:00:00Z)')
    parser.add_argument('--until', required=True, help='End date in ISO format')
    parser.add_argument('--q1-start', help='Q1 start date (defaults to since date)')
    parser.add_argument('--q1-end', help='Q1 end date (defaults to until date)')
    parser.add_argument('--github-token', help='GitHub PAT (or set GITHUB_TOKEN env var)')
    parser.add_argument('--genai-key', help='Google AI API key (or set GENAI_API_KEY env var)')
    
    args = parser.parse_args()
    
    github_token = args.github_token or os.getenv('GITHUB_TOKEN')
    genai_key = args.genai_key or os.getenv('GENAI_API_KEY')
    
    if not github_token:
        raise ValueError("GitHub token required. Use --github-token or set GITHUB_TOKEN env var")
    if not genai_key:
        raise ValueError("Google AI API key required. Use --genai-key or set GENAI_API_KEY env var")
    
    # Parse dates
    q1_start = datetime.fromisoformat(args.q1_start.replace('Z', '+00:00')) if args.q1_start else datetime.fromisoformat(args.since.replace('Z', '+00:00'))
    q1_end = datetime.fromisoformat(args.q1_end.replace('Z', '+00:00')) if args.q1_end else datetime.fromisoformat(args.until.replace('Z', '+00:00'))
    
    summarizer = GitHubCommitSummarizer(github_token, genai_key, args.repo)
    
    print(f"Fetching commits for {args.repo} from {args.since} to {args.until}...")
    commits = summarizer.fetch_commits(args.since, args.until)
    print(f"Found {len(commits)} commits")
    
    q1_text, q2_text = summarizer.categorize_by_quarter(commits, q1_start, q1_end)
    
    if q1_text:
        print(f"\n=== Q1 Summary for {args.repo} ===\n")
        print(summarizer.summarize_commits(q1_text, "Q1"))
    
    if q2_text:
        print(f"\n=== Q2 Summary for {args.repo} ===\n")
        print(summarizer.summarize_commits(q2_text, "Q2"))

if __name__ == "__main__":
    main()
