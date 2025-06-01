import os
import subprocess
from pathlib import Path

def check_worktree_exists(worktree_path: str) -> bool:
    """Check if the specified worktree directory exists and is a directory."""
    return os.path.isdir(worktree_path)

def launch_openhands_docker(worktree_path: str, llm_model: str = "o4-mini", api_key_env: str = "OPENAI_API_KEY", port: int = 3000, detach: bool = False):
    """
    Launch OpenHands agent in Docker, mounting the given worktree as /workspace.
    Args:
        worktree_path (str): Path to the git worktree to mount.
        llm_model (str): LLM model name (default: o4-mini).
        api_key_env (str): Name of the environment variable containing the API key.
        port (int): Port to expose (default: 3000).
        detach (bool): Run container in detached mode (default: False).
    Returns:
        int: Docker process return code.
    """
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise RuntimeError(f"{api_key_env} environment variable not set.")

    worktree_path = os.path.abspath(worktree_path)
    state_dir = os.path.expanduser("~/.openhands-state")
    os.makedirs(state_dir, exist_ok=True)

    docker_image = "docker.all-hands.dev/all-hands-ai/openhands:0.39"
    runtime_image = "docker.all-hands.dev/all-hands-ai/runtime:0.39-nikolaik"
    container_name = f"openhands-app-{os.path.basename(worktree_path)}"
    detach_flag = "-d" if detach else "-it"

    if not check_worktree_exists(worktree_path):
        raise FileNotFoundError(f"Worktree path '{worktree_path}' does not exist or is not a directory.")

    cmd = [
        "docker", "run", detach_flag, "--rm", "--pull=always",
        "-e", f"SANDBOX_RUNTIME_CONTAINER_IMAGE={runtime_image}",
        "-e", f"LLM_MODEL={llm_model}",
        "-e", f"LLM_API_KEY={api_key}",
        "-e", "LOG_ALL_EVENTS=true",
        "-v", f"/var/run/docker.sock:/var/run/docker.sock",
        "-v", f"{state_dir}:/.openhands-state",
        "-v", f"{worktree_path}:/workspace:rw",
        "-p", f"{port}:3000",
        "--add-host", "host.docker.internal:host-gateway",
        "--name", container_name,
        docker_image
    ]
    # Add SANDBOX_VOLUMES for explicit workspace mount (recommended by docs)
    sandbox_volumes = f"{worktree_path}:/workspace:rw"
    cmd.insert(cmd.index("-e") + 1, f"SANDBOX_VOLUMES={sandbox_volumes}")
    cmd.insert(cmd.index("-e") + 1, "-e")

    print("Launching OpenHands Docker with command:")
    print(" ".join(cmd))
    return subprocess.call(cmd)
