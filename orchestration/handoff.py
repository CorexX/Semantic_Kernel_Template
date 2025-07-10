"""
orchestration/handoff.py

Handles the setup and invocation of the handoff orchestration for agent collaboration.
"""

from semantic_kernel.agents import HandoffOrchestration
from chat.callbacks import streaming_agent_response_callback
from chat.user_input import human_response_function
from agents.agents import init_agents

async def setup_and_invoke_orchestration(project_client, task, runtime):
    """
    Sets up the handoff orchestration and invokes it with the given task and runtime.

    Args:
        project_client: The Azure AI project client.
        task (str): The task to be performed by the agents.
        runtime: The orchestration runtime.

    Returns:
        The result of the orchestration invocation.
    """
    try:
        agents, handoffs, created_agent_ids = await init_agents(project_client)
        handoff_orchestration = HandoffOrchestration(
            members=agents,
            handoffs=handoffs,
            streaming_agent_response_callback=streaming_agent_response_callback,
            human_response_function=human_response_function,
        )
        orchestration_result = await handoff_orchestration.invoke(
            task=task,
            runtime=runtime,
        )
        return orchestration_result, created_agent_ids
    except Exception as e:
        print(f"[Orchestration] Error during orchestration setup or invocation: {e}")
        raise
