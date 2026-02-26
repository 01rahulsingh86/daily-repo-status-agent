import os
from datetime import datetime
from github import Github, Auth

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")

gh = Github(auth=Auth.Token(GITHUB_TOKEN))
repo = gh.get_repo(REPO_NAME)

stale_days = 7
now = datetime.utcnow()

for pr in repo.get_pulls(state="open"):
    age = (now - pr.created_at).days
    if age >= stale_days:
        pr.create_issue_comment(
            f"⚠️ PR #{pr.number} has been open for {age} days. Consider reviewing."
        )

print("✅ PR risk check complete")
