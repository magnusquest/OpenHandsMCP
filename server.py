from fastmcp import FastMCP
import sys
from worktree_tools.create_worktree import create_worktree
from worktree_tools.remove_worktree import remove_worktree
from openhands_tools.launch_openhands_docker import launch_openhands_docker

mcp = FastMCP("OpenHands FastMCP Server")

@mcp.tool()
def start_openhands_agent(task: str, prompt: str = "create hello world python script") -> str:
    """
    Create a git worktree for the given task and launch OpenHands agent in Docker to handle the task.
    Args:
        task (str): The description of the task/feature name to delegate to OpenHands.
        prompt (str): The prompt to pass to the OpenHands agent in headless mode.
    Returns:
        str: A message indicating the worktree was created and the task was delegated.
    """
    try:
        create_worktree(task)
        worktree_path = f".worktree/feature-{task}"
        launch_openhands_docker(worktree_path, task_prompt=prompt)
        return f"Worktree created and OpenHands agent launched for '{task}' with prompt: '{prompt}'."
    except Exception as e:
        return f"Failed to create worktree or launch OpenHands for '{task}': {e}"

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
