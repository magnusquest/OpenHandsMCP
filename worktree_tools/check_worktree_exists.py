def check_worktree_exists(worktree_path: str) -> bool:
    """Check if the specified worktree directory exists and is a directory."""
    import os
    return os.path.isdir(worktree_path)
