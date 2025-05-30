# GitHub Quarterly Board Reporter

A Python tool that generates quarterly board reports from GitHub repository commits using Google's Gemini AI.

## Features

- Fetch commits from any GitHub repository within a date range
- Automatically categorize commits by quarters
- Generate AI-powered board reports suitable for executive presentations
- Configurable date ranges and custom prompts
- Support for environment variables and command-line arguments

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### Required API Keys

1. **GitHub Personal Access Token (PAT)**:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate a new token with `repo` scope (for private repos) or `public_repo` (for public repos)

2. **Google AI API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create an API key for Gemini

### Environment Variables

Set your API keys as environment variables:

```bash
export GITHUB_TOKEN="your_github_token_here"
export GENAI_API_KEY="your_google_ai_key_here"
```

Or create a `.env` file (not tracked in git):
```
GITHUB_TOKEN=your_github_token_here
GENAI_API_KEY=your_google_ai_key_here
```

## Usage

### Basic Usage

```bash
python git_summary_tool.py \
  --repo "owner/repository" \
  --since "2025-01-01T00:00:00Z" \
  --until "2025-06-30T23:59:59Z"
```

### Advanced Usage

```bash
python git_summary_tool.py \
  --repo "microsoft/vscode" \
  --since "2025-01-01T00:00:00Z" \
  --until "2025-06-30T23:59:59Z" \
  --q1-start "2025-02-01T00:00:00Z" \
  --q1-end "2025-04-30T23:59:59Z" \
  --github-token "your_token" \
  --genai-key "your_key"
```

### Parameters

- `--repo`: GitHub repository in `owner/repo` format (required)
- `--since`: Start date in ISO format (required)
- `--until`: End date in ISO format (required)
- `--q1-start`: Custom Q1 start date (optional, defaults to since date)
- `--q1-end`: Custom Q1 end date (optional, defaults to until date)
- `--github-token`: GitHub PAT (optional if set as env var)
- `--genai-key`: Google AI API key (optional if set as env var)

## Examples

### Analyze a Popular Open Source Project

```bash
python git_summary_tool.py \
  --repo "facebook/react" \
  --since "2025-01-01T00:00:00Z" \
  --until "2025-05-30T23:59:59Z"
```

### Custom Quarter Definition

```bash
python git_summary_tool.py \
  --repo "your-org/your-repo" \
  --since "2025-01-01T00:00:00Z" \
  --until "2025-12-31T23:59:59Z" \
  --q1-start "2025-03-01T00:00:00Z" \
  --q1-end "2025-05-31T23:59:59Z"
```

## Output

The tool generates summaries organized into these categories:

- 🚀 New features and improvements
- 🐛 Bug fixes and stability
- 📈 Performance and infrastructure
- 🔒 Security and compliance
- 📚 Documentation and tooling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this tool in your own projects!

## Troubleshooting

### Common Issues

1. **API Rate Limits**: GitHub API has rate limits. For large repositories, you might need to add delays between requests.

2. **Date Format**: Ensure dates are in ISO format with timezone (Z suffix for UTC).

3. **Repository Access**: Make sure your GitHub token has access to the repository you're trying to analyze.

### Error Messages

- `GitHub API error`: Check your GitHub token and repository access
- `API key required`: Set your environment variables or pass keys as arguments
- `Repository not found`: Verify the repository name format (`owner/repo`)
