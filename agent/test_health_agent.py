import os
from github import Github, Auth

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")

gh = Github(auth=Auth.Token(GITHUB_TOKEN))
repo = gh.get_repo(REPO_NAME)

# Example: check latest workflow runs
workflows = repo.get_workflows()
alerts = []

for wf in workflows:
    runs = wf.get_runs(status="completed")
    for run in runs[:5]:
        if run.conclusion != "success":
            alerts.append(f"Workflow {wf.name} failed at {run.created_at}")

if alerts:
    body = "\n".join(alerts)
    repo.create_issue(
        title="⚠️ Test/CI Health Alert",
        body=body,
        labels=["ci-failure"]
    )

print("✅ Test health agent completed")
