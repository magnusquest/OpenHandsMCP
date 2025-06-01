#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def remove_worktree(feature_name):
    repo_root = Path.cwd()
    worktree_dir = repo_root / ".worktree"
    worktree_path = worktree_dir / f"feature-{feature_name}"
    branch_name = f"feature/{feature_name}"

    # Remove the worktree if it exists
    if worktree_path.exists():
        subprocess.run(["git", "worktree", "remove", "--force", str(worktree_path)], check=True)
        print(f"Worktree removed: {worktree_path}")
    else:
        print(f"Worktree path '{worktree_path}' does not exist.")

    # Delete the branch if it exists
    branch_check = subprocess.run(["git", "rev-parse", "--verify", branch_name], capture_output=True, text=True)
    if branch_check.returncode == 0:
        subprocess.run(["git", "branch", "-D", branch_name], check=True)
        print(f"Branch deleted: {branch_name}")
    else:
        print(f"Branch '{branch_name}' does not exist.")
