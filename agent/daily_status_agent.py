import os
from github import Github
from datetime import datetime, timedelta
import openai

# ENV VARS
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")

openai.api_key = OPENAI_API_KEY

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

since = datetime.utcnow() - timedelta(days=1)

issues = repo.get_issues(state="all", since=since)
prs = repo.get_pulls(state="all")
commits = repo.get_commits(since=since)

summary_input = f"""
Repo: {REPO_NAME}

Issues (last 24h): {issues.totalCount}
PRs (open): {prs.totalCount}
Commits (last 24h): {commits.totalCount}

Write a concise daily repo status for maintainers.
Include risks, progress, and next actions.
"""

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": summary_input}]
)

report = response.choices[0].message.content

repo.create_issue(
    title=f"Daily Repo Status – {datetime.utcnow().strftime('%Y-%m-%d')}",
    body=report,
    labels=["daily-status"]
)

print("Daily status issue created")
