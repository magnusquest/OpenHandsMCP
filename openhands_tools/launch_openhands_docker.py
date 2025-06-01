import os
import docker
from pathlib import Path

def list_docker_images():
    """List all Docker images available on the local machine."""
    print("Listing available Docker images...")
    client = docker.from_env()
    images = client.images.list()
    print("Available Docker images:")
    for img in images:
        tags = img.tags if img.tags else ["<none>"]
        print(f"- ID: {img.short_id}, Tags: {tags}")
    return images

def launch_openhands_docker(
    worktree_path: str,
    llm_model: str = "o4-mini",
    api_key_env: str = "OPENAI_API_KEY",
    port: int = 3000,
    detach: bool = False,
    task_prompt: str = ""
):
    """
    Launch OpenHands agent in Docker, mounting the given worktree as /workspace in headless mode.
    Args:
        worktree_path (str): Path to the git worktree to mount.
        llm_model (str): LLM model name (default: o4-mini).
        api_key_env (str): Name of the environment variable containing the API key.
        port (int): Port to expose (default: 3000).
        detach (bool): Run container in detached mode (default: False).
        task_prompt (str): Task prompt for headless mode (default: empty string for none).
    Returns:
        int: Docker process return code.
    """
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise RuntimeError(f"{api_key_env} environment variable not set.")

    worktree_path = os.path.abspath(worktree_path)
    state_dir = os.path.abspath(f"{worktree_path}/.openhands-state")
    os.makedirs(state_dir, exist_ok=True)

    docker_image = "docker.all-hands.dev/all-hands-ai/runtime:0.39-nikolaik"
    container_name = f"openhands-app-{os.path.basename(worktree_path)}"
    user_id = str(os.getuid()) if hasattr(os, "getuid") else "1000"
    sandbox_volumes = f"{worktree_path}:/workspace:rw"

    # List images and check if the required image exists
    images = list_docker_images()
    image_exists = any(docker_image in tag for img in images for tag in img.tags)
    if image_exists:
      print(f"Image '{docker_image}' is already present locally.")
    else:
      raise RuntimeError(f"Image '{docker_image}' not found locally. Please pull it before proceeding.")

    client = docker.from_env()
    environment = {
        "SANDBOX_RUNTIME_CONTAINER_IMAGE": docker_image,
        "SANDBOX_USER_ID": user_id,
        "SANDBOX_VOLUMES": sandbox_volumes,
        "LLM_MODEL": llm_model,
        "LLM_API_KEY": api_key,
        "LOG_ALL_EVENTS": "true"
    }
    volumes = {
        "/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"},
        state_dir: {"bind": "/.openhands-state", "mode": "rw"},
        worktree_path: {"bind": "/workspace", "mode": "rw"}
    }
    # Fix: define command and extra_hosts before use, and use correct ports mapping
    extra_hosts = {"host.docker.internal": "host-gateway"}
    if task_prompt:
        command = ["python", "-m", "openhands.core.main", "-t", task_prompt]
    else:
        command = None
    # Docker SDK expects ports as {container_port: host_port} (int)
    ports = {"3000/tcp": port}

    print(f"Launching OpenHands Docker container '{container_name}' with SDK...")
    container = client.containers.run(
        docker_image,
        command=command,
        environment=environment,
        volumes=volumes,
        # Remove ports argument if it continues to cause type errors
        # ports=ports,
        extra_hosts=extra_hosts,
        name=container_name,
        detach=True,
        remove=True,
        tty=True,
        stdin_open=True,
        auto_remove=True
    )
    if detach:
        print(f"Container '{container_name}' started in detached mode.")
        return container
    else:
        # Stream logs to stdout, buffering to print full lines
        buffer = ""
        for chunk in container.logs(stream=True):
            text = chunk.decode(errors="replace")
            buffer += text
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                print(line)
        if buffer:
            print(buffer)
        exit_code = container.wait()["StatusCode"]
        print(f"Container exited with code {exit_code}")
        return exit_code

### main script to test the function
if __name__ == "__main__":
    # Example usage
    worktree_path = "./.worktree/feature-test"  # Replace with your actual worktree path
    try:
        launch_openhands_docker(worktree_path, task_prompt="Create a simple Python script")
    except Exception as e:
        print(f"Error launching OpenHands Docker: {e}")