"""
config/settings.py

Handles environment variable loading and configuration for Azure AI agent settings.
"""

import os
import json
from dotenv import load_dotenv
from semantic_kernel.agents import AzureAIAgentSettings

def load_agent_definitions(config_path="config/agents.json"):
    """
    Loads agent definitions from a JSON configuration file.

    Args:
        config_path (str): Path to the agent configuration JSON file.

    Returns:
        list: List of agent definition dictionaries.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            agent_defs = json.load(f)
        return agent_defs
    except Exception as e:
        print(f"[Config] Error loading agent definitions: {e}")
        raise

def load_settings():
    """
    Loads environment variables and returns AzureAIAgentSettings.

    Returns:
        AzureAIAgentSettings: Configured settings for Azure AI Agent.

    Raises:
        EnvironmentError: If required environment variables are missing.
    """
    try:
        load_dotenv()
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

        if not project_endpoint or not model_deployment:
            raise EnvironmentError(
                "Missing required environment variables: PROJECT_ENDPOINT and/or MODEL_DEPLOYMENT_NAME."
            )

        ai_agent_settings = AzureAIAgentSettings(
            project_endpoint=project_endpoint,
            model_deployment_name=model_deployment
        )
        return ai_agent_settings
    except Exception as e:
        print(f"[Config] Error loading settings: {e}")
        raise
