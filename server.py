from fastmcp import FastMCP
import sys
from worktree_tools.create_worktree import create_worktree
from worktree_tools.remove_worktree import remove_worktree
from openhands_tools.launch_openhands_docker import launch_openhands_docker
from worktree_tools.check_worktree_exists import check_worktree_exists

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
        worktree_path = f".worktree/feature-{task}"
        if check_worktree_exists(worktree_path):
            return f"Worktree '{worktree_path}' already exists. Aborting to prevent overwrite."
        create_worktree(task)
        launch_openhands_docker(worktree_path, task_prompt=prompt)
        return f"Worktree created and OpenHands agent launched for '{task}' with prompt: '{prompt}'."
    except Exception as e:
        return f"Failed to create worktree or launch OpenHands for '{task}': {e}"

@mcp.tool()
def list_openhands_agents() -> str:
    """
    List all git worktrees that are currently being used by OpenHands agents.
    Returns:
        str: A list of active OpenHands agent worktrees.
    """
    try:
        import os
        worktree_dir = ".worktree"
        if not os.path.exists(worktree_dir):
            return "No OpenHands agents found. No worktrees exist."
        
        worktrees = [d for d in os.listdir(worktree_dir) if os.path.isdir(os.path.join(worktree_dir, d))]
        if not worktrees:
            return "No OpenHands agents found. No worktrees exist."
        
        return f"Active OpenHands agents (worktrees): {', '.join(worktrees)}"
    except Exception as e:
        return f"Failed to list OpenHands agents: {e}"

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
        worktree_path = f".worktree/feature-{task}"
        if not check_worktree_exists(worktree_path):
            return f"Worktree '{worktree_path}' does not exist. Nothing to remove."
        remove_worktree(task)
        return f"Worktree and branch for '{task}' removed. Task stopped in the OpenHands agent."
    except Exception as e:
        return f"Failed to remove worktree for '{task}': {e}"

if __name__ == "__main__":
    mcp.run()
