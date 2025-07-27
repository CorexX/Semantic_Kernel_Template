"""
main.py

Entry point for the Semantic Kernel Orchestration system.
- Initializes the kernel and plugins.
- Sets up Azure AI credentials and project client.
- Starts the orchestration runtime.
- Invokes the orchestration process for agent collaboration.
- Cleans up created agents and stops the runtime.
"""

# === Imports ===
import asyncio
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent
from semantic_kernel.kernel import Kernel
from semantic_kernel.functions import KernelPlugin
from orchestration.runtime import OrchestrationRuntime
from orchestration.handoff import setup_and_invoke_orchestration
from skills.tools import ToolsPlugin

# === Kernel and Plugin Setup ===
# Initialize the Semantic Kernel, which is the core of the orchestration system.
# Adds the ToolsPlugin for general utility functions.
kernel = Kernel()
tools = KernelPlugin.from_object("tools", ToolsPlugin())
kernel.add_plugin(tools)

# === Main Async Function ===
async def main():
    """
    Main entry point for running the orchestration system.

    - Authenticates with Azure using DefaultAzureCredential.
    - Creates the Azure AI project client.
    - Starts the orchestration runtime.
    - Invokes the orchestration process with a sample task.
    - Prints the orchestration result.
    - Cleans up created agents and stops the runtime.
    """
    PROJECT_ENDPOINT = "https://vitafoundry.services.ai.azure.com/api/projects/VITA"

    async with (
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(credential=creds, endpoint=PROJECT_ENDPOINT) as project_client,
    ):
        # Start the orchestration runtime 
        runtime_wrapper = OrchestrationRuntime()
        runtime_wrapper.start()

        # Invoke the orchestration process with a sample support task
        orchestration_result, created_ids = await setup_and_invoke_orchestration(
            project_client=project_client,
            task="Greet the customer who is reaching out for support.",
            runtime=runtime_wrapper.runtime,
            kernel=kernel,
        )
        value = await orchestration_result.get()
        print(value)

        # Clean up: delete created agents and stop the runtime when idle
        for agent_id in created_ids:
            await project_client.agents.delete_agent(agent_id=agent_id)
        await runtime_wrapper.stop_when_idle()

# === Entrypoint ===
if __name__ == "__main__":
    asyncio.run(main())
