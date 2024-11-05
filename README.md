## GitHub PR status validator
Detects force-merged pull requests by checking both status checks and check runs on the merge and last commits, ensuring all required checks passed before merging.

Example of how to use the script:

Step 1: Set Environment Variables

```
export GITHUB_TOKEN="your_github_token"
export GITHUB_OWNER="your_org_or_username"
export GITHUB_REPO="your_repository_name"
```

Step 2: Run the Script
Once the environment variables are set, run the script in your Python environment:
```
python main.py
```

Expected Output
The script will output a list of PRs that were force-merged without meeting all checks. For example:
```
2024-11-05 23:42:48,221 - INFO - GitHub token and repository details retrieved from environment variables.
2024-11-05 23:42:48,222 - INFO - Searching for force merged PRs in repository: your_org_or_username/your_repository_name
2024-11-05 23:42:49,511 - INFO - Checking PR #18: go: bump github.com/onsi/gomega from 1.35.0 to 1.35.1
2024-11-05 23:42:49,511 - INFO - PR #18 is merged. Checking commit statuses and check runs.
2024-11-05 23:42:50,526 - INFO - No statuses found for commit 01cb75ca997bfbca9c0b43f10d70d1280d96f1c8.
2024-11-05 23:42:51,107 - INFO - Found 6 check runs for commit 01cb75ca997bfbca9c0b43f10d70d1280d96f1c8
2024-11-05 23:42:51,107 - INFO - Check Run: Dependabot, Status: completed, Conclusion: success
2024-11-05 23:42:51,107 - INFO - Check Run: Dependabot, Status: completed, Conclusion: success
2024-11-05 23:42:51,108 - INFO - Check Run: Dependabot, Status: completed, Conclusion: success
2024-11-05 23:42:51,108 - INFO - Check Run: Dependabot, Status: completed, Conclusion: success
2024-11-05 23:42:51,108 - INFO - Check Run: Check for spelling errors, Status: completed, Conclusion: failure
2024-11-05 23:42:51,108 - INFO - Check Run: lint, Status: completed, Conclusion: failure
2024-11-05 23:42:51,108 - WARNING - PR #18 was force merged without all checks passing.
2024-11-05 23:43:14,602 - INFO - Completed search for force merged PRs.
2024-11-05 23:43:14,602 - INFO - Force Merged PRs:
2024-11-05 23:43:14,602 - INFO - - PR #18: go: bump github.com/onsi/gomega from 1.35.0 to 1.35.1 (merged at 2024-11-03 18:10:02+00:00)
```

Explanation
The script:

1. Checks each closed PR in the specified repository.
2. Outputs warnings for any PRs that were force-merged without passing all required checks, along with PR details.

This makes it easy to audit any PRs merged without meeting all requirements.
