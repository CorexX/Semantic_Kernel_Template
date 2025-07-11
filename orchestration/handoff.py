"""
orchestration/handoff.py

Handles the setup and invocation of the handoff orchestration for agent collaboration.
"""

# === Imports ===
from semantic_kernel.agents import HandoffOrchestration
from chat.callbacks import streaming_agent_response_callback
from chat.user_input import human_response_function
from agents.agents import init_agents

# === Function Definitions ===
async def setup_and_invoke_orchestration(project_client, task, runtime, kernel=None):
    """
    Sets up the handoff orchestration and invokes it with the given task and runtime.

    Args:
        project_client: The Azure AI project client.
        task (str): The task to be performed by the agents.
        runtime: The orchestration runtime.
        kernel: Optional kernel to attach to agents.

    Returns:
        tuple: (orchestration_result, created_agent_ids)
    """
    try:
        # Initialize agents and handoff mapping
        agents, handoffs, created_agent_ids = await init_agents(project_client, kernel)

        # Create the HandoffOrchestration object with callbacks for streaming and user input
        handoff_orchestration = HandoffOrchestration(
            members=agents,
            handoffs=handoffs,
            streaming_agent_response_callback=streaming_agent_response_callback,
            human_response_function=human_response_function,
        )

        # Invoke the orchestration process with the provided task and runtime
        orchestration_result = await handoff_orchestration.invoke(
            task=task,
            runtime=runtime,
        )
        return orchestration_result, created_agent_ids
    except Exception as e:
        # Log and re-raise any errors during orchestration setup or invocation
        print(f"[Orchestration] Error during orchestration setup or invocation: {e}")
        raise
