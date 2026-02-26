import os
from datetime import datetime, timedelta

from github import Github
from github import Auth
from openai import OpenAI

# --------------------
# ENV VARS
# --------------------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")

if not all([GITHUB_TOKEN, OPENAI_API_KEY, REPO_NAME]):
    raise RuntimeError("Missing required environment variables")

# --------------------
# GitHub Client (new auth)
# --------------------
auth = Auth.Token(GITHUB_TOKEN)
gh = Github(auth=auth)
repo = gh.get_repo(REPO_NAME)

# --------------------
# Time window
# --------------------
since = datetime.utcnow() - timedelta(days=1)

issues = repo.get_issues(state="all", since=since)
prs = repo.get_pulls(state="open")
commits = repo.get_commits(since=since)

# --------------------
# LLM Client (new OpenAI API)
# --------------------
client = OpenAI(api_key=OPENAI_API_KEY)

prompt = f"""
Repository: {REPO_NAME}

Activity in the last 24 hours:
- Issues updated/created: {issues.totalCount}
- Open pull requests: {prs.totalCount}
- Commits pushed: {commits.totalCount}

Write a concise daily repository status report for maintainers.
Include:
- Current health
- Risks or blockers
- Progress highlights
- Recommended next actions
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

report = response.choices[0].message.content

# --------------------
# Create GitHub Issue
# --------------------
repo.create_issue(
    title=f"Daily Repo Status – {datetime.utcnow().strftime('%Y-%m-%d')}",
    body=report,
    labels=["daily-status"]
)

print(" Daily repo status issue created successfully")
