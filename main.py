import os
import logging
from github import Github

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Read GitHub token, organization, and repository name from env varibles
token = os.getenv("GITHUB_TOKEN")
owner = os.getenv("GITHUB_OWNER")
repo_name = os.getenv("GITHUB_REPO")

logger.info("GitHub token and repository details retrieved from environment variables.")

# Authenticate
g = Github(token)

def find_force_merged_prs(owner, repo_name):
    logger.info(f"Searching for force merged PRs in repository: {owner}/{repo_name}")
    repo = g.get_repo(f"{owner}/{repo_name}")
    closed_prs = repo.get_pulls(state="closed")
    force_merged_prs = []

    for pr in closed_prs:
        logger.info(f"Checking PR #{pr.number}: {pr.title}")
        
        if pr.merged_at:
            logger.info(f"PR #{pr.number} is merged. Checking commit statuses and check runs.")
            
            # Check both the merge commit and the last commit on the PR branch
            merge_commit_sha = pr.merge_commit_sha
            head_commit_sha = pr.head.sha

            # Function to check commit statuses and check runs for a given commit SHA
            def check_commit_status_and_runs(commit_sha):
                commit = repo.get_commit(commit_sha)
                
                # Check Commit Statuses
                combined_status = commit.get_combined_status()
                statuses = combined_status.statuses
                has_failed_statuses = any(
                    status.state in ["failure", "pending"] for status in statuses
                )

                # Log statuses
                if statuses:
                    logger.info(f"Found {len(statuses)} statuses for commit {commit_sha}")
                    for status in statuses:
                        logger.info(f"Status Context: {status.context}, State: {status.state}")
                else:
                    logger.info(f"No statuses found for commit {commit_sha}.")

                # Check Check Runs (GitHub Actions or other Checks API integrations)
                check_runs = commit.get_check_runs()
                has_failed_runs = any(
                    run.conclusion in ["failure", "cancelled", "timed_out"] or run.status == "in_progress"
                    for run in check_runs
                )

                # Log check runs
                if check_runs.totalCount > 0:
                    logger.info(f"Found {check_runs.totalCount} check runs for commit {commit_sha}")
                    for run in check_runs:
                        logger.info(f"Check Run: {run.name}, Status: {run.status}, Conclusion: {run.conclusion}")
                else:
                    logger.info(f"No check runs found for commit {commit_sha}.")

                # true if either statuses or check runs have failed or are pending
                return has_failed_statuses or has_failed_runs

            # Check the merge commit first, then fall back to the PR's head commit
            has_failed_or_pending_checks = check_commit_status_and_runs(merge_commit_sha)
            if not has_failed_or_pending_checks:
                logger.info(f"Falling back to checking last commit on PR branch for PR #{pr.number}.")
                has_failed_or_pending_checks = check_commit_status_and_runs(head_commit_sha)

            # Record the PR if there are failed or pending statuses or check runs
            if has_failed_or_pending_checks:
                logger.warning(f"PR #{pr.number} was force merged without all checks passing.")
                force_merged_prs.append(pr)
            else:
                logger.info(f"PR #{pr.number} passed all required checks before merging.")
        else:
            logger.info(f"PR #{pr.number} was closed but not merged.")
    
    logger.info("Completed search for force merged PRs.")
    return force_merged_prs

force_merged_prs = find_force_merged_prs(owner, repo_name)
logger.info("Force Merged PRs:")
for pr in force_merged_prs:
    logger.info(f"- PR #{pr.number}: {pr.title} (merged at {pr.merged_at})")

