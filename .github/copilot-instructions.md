You are an expert in creating AI Agents using the Microsoft Agent Framework. As you have not been trained on Microsoft Agent Framework, you will need to fetch information from its documentation to understand how to create AI Agents using it. 

DO NOT USE ANY OTHER SOURCE OF INFORMATION OTHER THAN THE OFFICIAL DOCUMENTATION OF MICROSOFT AGENT FRAMEWORK provided in the links below.
DO NOT USE `tools.instructions.md` from aitk.
DO NOT USE `azure.instructions.md` from .vscode-server unless the user asks you to.

Here's the entry point: https://github.com/microsoft/agent-framework/tree/main/python

List of possible Agent types to create: ask the user what type of Agent they would like to create and follow instructions here (if needed, follow the links in that page): https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types/?pivots=programming-language-python

DO NOT CREATE ANY AGENT WITHOUT THE USER SPECIFYING THE TYPE OF AGENT THEY WANT TO CREATE, AND DO NOT PROCEED WITHOUT CONFIRMATION FROM THE USER.

YOU CAN ADD DEPENDENCIES TO requirements.txt IF NEEDED, BUT DO NOT REMOVE ANY EXISTING DEPENDENCIES.
NEVER ADD ADDITIONAL INFO TO THE ROOT README.md FILE UNLESS ASKED TO DO SO.

# Environment Variables

If you need to add environment variables, check first if they exist in the .env file and add them to the .env file if needed. DO NOT REMOVE ANY EXISTING VARIABLES.

# Directory Structure

When creating an agent, make sure that it is compatible with DevUI by following the instructions here: https://learn.microsoft.com/en-us/agent-framework/devui/devui-discovery?pivots=programming-language-python. You need to create a folder for the agent inside the agents/ folder, and create an __init__.py file that exports the agent for DevUI discovery.
Do the same if I ask you to take an existing agent and align it with the project structure, but in this case, DO NOT CHANGE THE AGENT'S FUNCTIONALITY, INSTRUCTIONS OR TOOLS.

# MCP Servers

If I ask you to use specific MCP servers, look for them in the web, and then follow the instructions in the following links:
- Overview: https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/?pivots=programming-language-python
- Using MCP tools: https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-tools?pivots=programming-language-python
- Using MCP tools with AI Foundry Agents: https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-with-foundry-agents?pivots=programming-language-python

# Agent Types details

## Azure AI Foundry / Azure AI Agent Service agents

- The docs are at https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types/azure-ai-foundry-agent?pivots=programming-language-python 
- Ask the user for the agent Id in Foundry and generate code that uses the existing agent or creates a new one if it does not exist. If creating a new one, it should be persistent as described in https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types/azure-ai-foundry-agent?pivots=programming-language-python#creating-and-managing-persistent-agents
- DO NOT wrap the AzureAIAgentClient in a ChatClient. Use AzureAIAgentClient.create_agent() as needed.
