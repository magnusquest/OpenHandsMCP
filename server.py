from fastmcp import FastMCP

mcp = FastMCP("OpenHands FastMCP Server")

@mcp.tool()
def openhands_agent(task: str) -> str:
    """
    Simulate delegating a task to an OpenHands agent and returning a status message.
    Args:
        task (str): The description of the task to delegate to OpenHands.
    Returns:
        str: A message indicating the task was delegated.
    """
    # In a real implementation, this would call the OpenHands API or trigger an agent workflow.
    # Here, we just simulate the delegation.
    return f"Task '{task}' has been delegated to the OpenHands agent."

if __name__ == "__main__":
    mcp.run()
