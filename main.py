import asyncio

from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent

from config.settings import load_settings
from orchestration.runtime import OrchestrationRuntime
from orchestration.handoff import setup_and_invoke_orchestration

async def main():
    """
    Main function to run the modularized agent orchestration system.
    """
    PROJECT_ENDPOINT = "https://vitafoundry.services.ai.azure.com/api/projects/VITA"
    try:
        async with (
            DefaultAzureCredential() as creds,
            AzureAIAgent.create_client(credential=creds, endpoint=PROJECT_ENDPOINT) as project_client,
        ):
            # Initialize runtime
            runtime_wrapper = OrchestrationRuntime()
            runtime_wrapper.start()

            # Orchestrate agents
            orchestration_result, created_agent_ids = await setup_and_invoke_orchestration(
                project_client=project_client,
                task="Greet the customer who is reaching out for support.",
                runtime=runtime_wrapper.runtime,
            )

            # Wait for results
            value = await orchestration_result.get()
            print(value)

            # Cleanup: delete any agents that were created in this session
            for agent_id in created_agent_ids:
                try:
                    await project_client.agents.delete_agent(agent_id=agent_id)
                    print(f"Deleted agent {agent_id}")
                except Exception as cleanup_exc:
                    print(f"Failed to delete agent {agent_id}: {cleanup_exc}")

            # Stop runtime after invocation is complete
            await runtime_wrapper.stop_when_idle()
    except Exception as e:
        print(f"[Main] Error in main orchestration: {e}")

if __name__ == "__main__":
    asyncio.run(main())
