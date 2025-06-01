#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def ensure_clean_repo():
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Not a git repository or git is not installed.", file=sys.stderr)
        sys.exit(1)
    if result.stdout.strip():
        print("Error: Repository has uncommitted changes. Please commit or stash them before creating a worktree.", file=sys.stderr)
        sys.exit(1)

def create_worktree(feature_name):
    repo_root = Path.cwd()
    worktree_dir = repo_root / ".worktree"
    worktree_dir.mkdir(exist_ok=True)
    worktree_path = worktree_dir / f"feature-{feature_name}"
    branch_name = f"feature/{feature_name}"

    # Check if branch already exists
    branch_check = subprocess.run(["git", "rev-parse", "--verify", branch_name], capture_output=True, text=True)
    if branch_check.returncode == 0:
        raise Exception(f"Branch '{branch_name}' already exists.")

    # Check if worktree already exists
    if worktree_path.exists():
        raise Exception(f"Worktree path '{worktree_path}' already exists.")

    # Create the new branch from current HEAD
    subprocess.run(["git", "branch", branch_name], check=True)
    # Add the worktree
    subprocess.run(["git", "worktree", "add", str(worktree_path), branch_name], check=True)
    print(f"Worktree created at: {worktree_path}")
    print(f"Branch name: {branch_name}")
