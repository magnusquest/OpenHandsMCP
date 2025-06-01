from fastmcp import FastMCP
import sys
from worktree_tools.create_worktree import create_worktree
from worktree_tools.remove_worktree import remove_worktree

mcp = FastMCP("OpenHands FastMCP Server")

@mcp.tool()
def start_openhands_agent(task: str) -> str:
    """
    Create a git worktree for the given task and simulate delegating it to an OpenHands agent.
    Args:
        task (str): The description of the task/feature name to delegate to OpenHands.
    Returns:
        str: A message indicating the worktree was created and the task was delegated.
    """
    try:
        create_worktree(task)
        return f"Worktree created and task '{task}' delegated to the OpenHands agent."
    except Exception as e:
        return f"Failed to create worktree for '{task}': {e}"

@mcp.tool()
def stop_openhands_agent(task: str) -> str:
    """
    Remove the git worktree and branch for the given task and simulate stopping the OpenHands agent.
    Args:
        task (str): The description of the task/feature name to stop in OpenHands.
    Returns:
        str: A message indicating the worktree and branch were removed and the task was stopped.
    """
    try:
        remove_worktree(task)
        return f"Worktree and branch for '{task}' removed. Task stopped in the OpenHands agent."
    except Exception as e:
        return f"Failed to remove worktree for '{task}': {e}"

if __name__ == "__main__":
    mcp.run()
