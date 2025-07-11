import asyncio
from azure.identity.aio import DefaultAzureCredential
from semantic_kernel.agents import AzureAIAgent
from semantic_kernel.kernel import Kernel
from semantic_kernel.functions import KernelPlugin
from orchestration.runtime import OrchestrationRuntime
from orchestration.handoff import setup_and_invoke_orchestration
from skills.tools import ToolsPlugin


kernel = Kernel()
tools = KernelPlugin.from_object("tools", ToolsPlugin())
kernel.add_plugin(tools)

async def main():
    PROJECT_ENDPOINT = "https://vitafoundry.services.ai.azure.com/api/projects/VITA"

    async with (
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(credential=creds, endpoint=PROJECT_ENDPOINT) as project_client,
    ):
        # 1) Runtime starten
        runtime_wrapper = OrchestrationRuntime()
        runtime_wrapper.start()

        # 4) Orchestration ausführen
        orchestration_result, created_ids = await setup_and_invoke_orchestration(
            project_client=project_client,
            task="Greet the customer who is reaching out for support.",
            runtime=runtime_wrapper.runtime,
            kernel=kernel,
        )
        value = await orchestration_result.get()
        print(value)

        # 5) Aufräumen
        for agent_id in created_ids:
            await project_client.agents.delete_agent(agent_id=agent_id)
        await runtime_wrapper.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())
