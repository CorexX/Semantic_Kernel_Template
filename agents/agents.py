"""
agents/agents.py

Initializes and configures multiple agents (new and existing) for the orchestration system.
Handles agent creation, fetching, and handoff configuration.

Functions:
- create_or_fetch_agent: Creates a new agent or fetches an existing one based on config.
- build_handoffs_dict: Builds the handoff mapping for orchestration.
- init_agents: Main entry point to initialize agents and handoffs.

Returns from init_agents:
    tuple: (list of agents, OrchestrationHandoffs instance, list of created agent IDs)
"""

# === Imports ===
from semantic_kernel.agents import AzureAIAgent, OrchestrationHandoffs
from config.settings import load_agent_definitions, load_settings

# === Agent Creation ===
async def create_or_fetch_agent(agent_cfg, project_client, created_agent_ids, kernel=None):
    """
    Create a new agent or fetch an existing agent based on the configuration.

    Args:
        agent_cfg (dict): Agent configuration.
        project_client: Azure AI project client.
        created_agent_ids (list): List to append created agent IDs for cleanup.
        kernel: Optional kernel to attach to the agent.

    Returns:
        AzureAIAgent: The initialized agent.
    """
    agent_name = agent_cfg.get("name", "Agent")
    if agent_cfg.get("type") == "new":
        # Create a new agent using the specified or default model deployment
        model_deployment_name = agent_cfg.get("model_deployment_name")
        if not model_deployment_name:
            ai_agent_settings = load_settings()
            model_deployment_name = ai_agent_settings.model_deployment_name
        agent_definition = await project_client.agents.create_agent(
            model=model_deployment_name,
            name=agent_name,
            instructions=agent_cfg.get("instructions", ""),
            description=agent_cfg.get("description", "")
        )
        created_agent_ids.append(agent_definition.id)
    elif agent_cfg.get("type") == "existing":
        # Fetch an existing agent by ID
        agent_id = agent_cfg.get("agent_id")
        if not agent_id:
            raise ValueError("Missing agent_id for existing agent in config.")
        agent_definition = await project_client.agents.get_agent(agent_id=agent_id)
    else:
        raise ValueError(f"Unknown agent type in config: {agent_cfg.get('type')}")
    agent = AzureAIAgent(
        client=project_client,
        definition=agent_definition,
        kernel=kernel
    )
    # Ensure the agent's .name property matches the config for orchestration
    try:
        agent.name = agent_name
    except Exception:
        # Some agent objects may not allow setting .name; ignore if so
        pass
    return agent

# === Handoff Mapping ===
def build_handoffs_dict(agent_configs):
    """
    Build the handoff mapping for orchestration.

    Args:
        agent_configs (list): List of agent configuration dictionaries.

    Returns:
        dict: Mapping of agent names to their handoff connections.
    """
    handoffs_dict = {}
    for agent_cfg in agent_configs:
        agent_name = agent_cfg.get("name", "Agent")
        handoff_names = agent_cfg.get("handoffs", [])
        handoffs_dict[agent_name] = handoff_names
    return handoffs_dict

# === Initialization ===
async def init_agents(project_client, kernel=None):
    """
    Initializes multiple agents (new and existing) and orchestration handoffs.

    Args:
        project_client: The Azure AI project client.
        kernel: Optional kernel to attach to agents.

    Returns:
        tuple: (list of agents, OrchestrationHandoffs instance, list of created agent IDs)
    """
    try:
        agent_configs = load_agent_definitions()
        created_agent_ids = []
        agents = []

        # Create or fetch all agents as specified in the config
        for agent_cfg in agent_configs:
            agent = await create_or_fetch_agent(agent_cfg, project_client, created_agent_ids, kernel)
            agents.append(agent)

        # Build the handoff connections dictionary
        handoffs_dict = build_handoffs_dict(agent_configs)

        # Create the OrchestrationHandoffs object
        handoffs = OrchestrationHandoffs(handoffs_dict)
        return agents, handoffs, created_agent_ids
    except Exception as e:
        # Log and re-raise any errors during agent initialization
        print(f"[Agents] Error initializing agents: {e}")
        raise
