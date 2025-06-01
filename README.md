# OpenHands FastMCP Server

This project scaffolds a FastMCP-based Model Context Protocol (MCP) server designed for rapid prototyping and feature development with OpenHands agents. Each feature or task is developed in an isolated git worktree/branch, enabling parallel, agent-driven automation with human-in-the-loop chat for guidance and review.

## Project Goals

- Enable fast, isolated feature development using OpenHands agents and FastMCP
- Integrate with git worktree for parallel task branches
- Support containerized agent environments (Docker)
- Provide CLI/API for agent task kickoff and real-time chat
- Automate and document the workflow for reproducibility

## High-Level Workflow

1. **Repository Preparation**: Use `git worktree` to create a new working directory and branch for each feature/task.
2. **Containerized Agent Environment**: Start an OpenHands Docker container, mounting the worktree as the workspace.
3. **Agent Task Kickoff**: Initiate a new task by sending a prompt/goal to the OpenHands agent (via CLI, API, or chat interface).
4. **Development Workflow**: The agent writes code, commits changes, and pushes to the feature branch. Human reviews and merges as needed.
5. **Documentation & Automation**: Document the workflow and optionally automate steps with scripts or Makefiles.

## Example Use Cases

- Add new REST endpoints or tools to the MCP server
- Integrate external APIs or services
- Prototype and test new agent capabilities

## Running with SSE and MCP Inspector

To run the FastMCP server with SSE transport and inspect it using the MCP Inspector:

1. Start the server with SSE transport:

   ```sh
   uv run fastmcp run server.py --transport sse --host 0.0.0.0 --port 8000
   ```

2. In a separate terminal, launch the MCP Inspector in development mode:

   ```sh
   uv run fastmcp dev server.py
   ```

- The Inspector will connect to your running server and provide a web-based interface for inspection and testing.
- If you see 404 errors on /sse, ensure you are running the server with `--transport sse`.

## Example: Using the MCP Client

You can interact with this FastMCP server programmatically using the MCP client:

```python
from fastmcp import Client

async def main():
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        result = await client.call_tool("start_openhands_agent", {"task": "my-feature"})
        print(f"Result: {result.text}")
```
