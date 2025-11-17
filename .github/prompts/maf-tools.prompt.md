# Microsoft Agent Framework - Adding Tools and MCP Servers

This prompt helps you add tools and Model Context Protocol (MCP) servers to Microsoft Agent Framework agents in Python.

## Overview

The Microsoft Agent Framework supports multiple types of tools to extend agent capabilities:

1. **Function Tools** - Your own Python functions that agents can call
2. **Built-in/Hosted Tools** - Pre-built tools for web search, file search, code interpreter
3. **MCP (Model Context Protocol) Tools** - Connect to external MCP servers for additional capabilities

## 1. Adding Function Tools

> **Official Documentation**: [Agent Tools Overview](https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-tools?pivots=programming-language-python)
>
> Always refer to the official documentation for the most up-to-date instructions on adding tools to agents.

### Function Tool Requirements

Function tools must:
- Have clear docstrings explaining their purpose
- Use type annotations for all parameters
- Use `Annotated` with `Field(description=...)` for parameter descriptions
- Be deterministic and LLM-friendly
- Handle errors gracefully

### Example Function Tool

```python
from typing import Annotated
from pydantic import Field

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."
```

### Adding Tools at Agent Construction

```python
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient

# Create agent with tools defined at construction
agent = ChatAgent(
    chat_client=OpenAIChatClient(),
    instructions="You are a helpful assistant",
    tools=[get_weather]  # Tools available for all runs
)

result = await agent.run("What's the weather like in Amsterdam?")
```

### Adding Tools Per-Run

```python
# Agent created without tools
agent = ChatAgent(
    chat_client=OpenAIChatClient(),
    instructions="You are a helpful assistant"
)

# Provide tools for specific runs
result = await agent.run(
    "What's the weather in Seattle?",
    tools=[get_weather]  # Tool provided for this run only
)

# Use different tools for different runs
result2 = await agent.run(
    "What's the current time?", 
    tools=[get_time]  # Different tool
)

# Mix agent-level and run-level tools
agent_with_base_tools = ChatAgent(
    chat_client=OpenAIChatClient(),
    instructions="You are a helpful assistant",
    tools=[get_time]  # Base tool
)

# This run has access to both get_time and get_weather
result = await agent_with_base_tools.run(
    "What's the weather and time in New York?",
    tools=[get_weather]  # Additional tool
)
```

## 2. Adding Built-in and Hosted Tools

### Web Search Tool

```python
from agent_framework import ChatAgent, HostedWebSearchTool
from agent_framework.openai import OpenAIChatClient

agent = ChatAgent(
    chat_client=OpenAIChatClient(),
    instructions="You are a helpful assistant with web search capabilities",
    tools=[
        HostedWebSearchTool(
            additional_properties={
                "user_location": {
                    "city": "Seattle",
                    "country": "US"
                }
            }
        )
    ]
)

result = await agent.run("What are the latest news about AI?")
```

### Code Interpreter Tool

```python
from agent_framework import ChatAgent, HostedCodeInterpreterTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async with AzureCliCredential() as credential:
    agent = ChatAgent(
        chat_client=AzureAIAgentClient(async_credential=credential),
        instructions="You are a data analysis assistant",
        tools=[HostedCodeInterpreterTool()]
    )
    
    result = await agent.run("Analyze this dataset and create a visualization")
```

### File Search Tool

```python
from agent_framework import ChatAgent, HostedFileSearchTool, HostedVectorStoreContent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async with AzureCliCredential() as credential:
    agent = ChatAgent(
        chat_client=AzureAIAgentClient(async_credential=credential),
        instructions="You are a document search assistant",
        tools=[
            HostedFileSearchTool(
                inputs=[
                    HostedVectorStoreContent(vector_store_id="vs_123")
                ],
                max_results=10
            )
        ]
    )
    
    result = await agent.run("Find information about quarterly reports")
```

## 3. Adding MCP (Model Context Protocol) Tools

> **Official Documentation**: [Using MCP Tools with Agents](https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-tools?pivots=programming-language-python)
>
> Always refer to the official documentation for the most up-to-date instructions on MCP tool integration.

### MCP Tool Types

The Agent Framework supports three types of MCP connections:

#### MCPStdioTool - Local MCP Servers

For MCP servers that run as local processes using standard input/output:

```python
import asyncio
from agent_framework import ChatAgent, MCPStdioTool
from agent_framework.openai import OpenAIChatClient

async def local_mcp_example():
    """Example using a local MCP server via stdio."""
    async with (
        MCPStdioTool(
            name="calculator", 
            command="uvx", 
            args=["mcp-server-calculator"]
        ) as mcp_server,
        ChatAgent(
            chat_client=OpenAIChatClient(),
            name="MathAgent",
            instructions="You are a helpful math assistant that can solve calculations.",
        ) as agent,
    ):
        result = await agent.run(
            "What is 15 * 23 + 45?", 
            tools=mcp_server
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(local_mcp_example())
```

#### MCPStreamableHTTPTool - HTTP/SSE MCP Servers

For MCP servers accessible over HTTP with Server-Sent Events:

```python
import asyncio
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async def http_mcp_example():
    """Example using an HTTP-based MCP server."""
    async with (
        AzureCliCredential() as credential,
        MCPStreamableHTTPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
            headers={"Authorization": "Bearer your-token"},
        ) as mcp_server,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            name="DocsAgent",
            instructions="You help with Microsoft documentation questions.",
        ) as agent,
    ):
        result = await agent.run(
            "How to create an Azure storage account using az cli?",
            tools=mcp_server
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(http_mcp_example())
```

#### MCPWebsocketTool - WebSocket MCP Servers

For MCP servers using WebSocket connections:

```python
import asyncio
from agent_framework import ChatAgent, MCPWebsocketTool
from agent_framework.openai import OpenAIChatClient

async def websocket_mcp_example():
    """Example using a WebSocket-based MCP server."""
    async with (
        MCPWebsocketTool(
            name="realtime-data",
            url="wss://api.example.com/mcp",
        ) as mcp_server,
        ChatAgent(
            chat_client=OpenAIChatClient(),
            name="DataAgent",
            instructions="You provide real-time data insights.",
        ) as agent,
    ):
        result = await agent.run(
            "What is the current market status?",
            tools=mcp_server
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(websocket_mcp_example())
```

## 4. Azure AI Foundry Hosted MCP Tools

> **Official Documentation**: [Using MCP with Azure AI Foundry Agents](https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-with-foundry-agents?pivots=programming-language-python)
>
> Always refer to the official documentation for the most up-to-date instructions on Azure AI Foundry MCP integration.

For Azure AI Foundry agents, use `HostedMCPTool` where the MCP server is hosted and managed by Azure:

### Basic Azure AI Foundry MCP Integration

```python
import asyncio
from agent_framework import HostedMCPTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

async def basic_foundry_mcp_example():
    """Basic example of Azure AI Foundry agent with hosted MCP tools."""
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential) as chat_client,
    ):
        # Enable Azure AI observability (optional but recommended)
        await chat_client.setup_azure_ai_observability()

        # Create agent with hosted MCP tool
        agent = chat_client.create_agent(
            name="MicrosoftLearnAgent", 
            instructions="You answer questions by searching Microsoft Learn content only.",
            tools=HostedMCPTool(
                name="Microsoft Learn MCP",
                url="https://learn.microsoft.com/api/mcp",
            ),
        )

        # Simple query without approval workflow
        result = await agent.run(
            "Please summarize the Azure AI Agent documentation related to MCP tool calling?"
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(basic_foundry_mcp_example())
```

### Multi-Tool Azure AI Foundry MCP Configuration

```python
async def multi_tool_mcp_example():
    """Example using multiple hosted MCP tools."""
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentClient(async_credential=credential) as chat_client,
    ):
        await chat_client.setup_azure_ai_observability()

        # Create agent with multiple MCP tools
        agent = chat_client.create_agent(
            name="MultiToolAgent",
            instructions="You can search documentation and access GitHub repositories.",
            tools=[
                HostedMCPTool(
                    name="Microsoft Learn MCP",
                    url="https://learn.microsoft.com/api/mcp",
                    approval_mode="never_require",  # Auto-approve documentation searches
                ),
                HostedMCPTool(
                    name="GitHub MCP", 
                    url="https://api.github.com/mcp",
                    approval_mode="always_require",  # Require approval for GitHub operations
                    headers={"Authorization": "Bearer github-token"},
                ),
            ],
        )

        result = await agent.run(
            "Find Azure documentation and also check the latest commits in microsoft/semantic-kernel"
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(multi_tool_mcp_example())
```

### Azure AI Foundry MCP Approval Modes

- `"never_require"` or `"never"`: Tools execute automatically without approval
- `"always_require"` or `"always"`: All tool invocations require user approval
- Custom approval rules can also be configured

## 5. Popular MCP Servers

Common MCP servers you can use:

- **Calculator**: `uvx mcp-server-calculator` - Mathematical computations
- **Filesystem**: `uvx mcp-server-filesystem` - File system operations
- **GitHub**: `npx @modelcontextprotocol/server-github` - GitHub repository access
- **SQLite**: `uvx mcp-server-sqlite` - Database operations
- **Microsoft Learn**: `https://learn.microsoft.com/api/mcp` - Microsoft documentation

## 6. Environment Configuration

### For Azure AI Foundry Agents

```python
import os

# Set required environment variables
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = "https://<your-project>.services.ai.azure.com/api/projects/<project-id>"
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o-mini"  # Optional, defaults to this
```

### For OpenAI Agents

```python
import os

os.environ["OPENAI_API_KEY"] = "your-api-key"
```

## Best Practices

1. **Tool Organization**: Create separate tool modules under `src/tools/` directory
2. **Clear Docstrings**: Every tool function must have a clear docstring explaining its purpose
3. **Type Annotations**: Use proper type hints and Pydantic `Field` descriptions
4. **Error Handling**: Tools should handle errors gracefully and return meaningful error messages
5. **Security**: Never hardcode API keys, credentials, or secrets in tool code
6. **Resource Management**: Use `async with` for proper cleanup of MCP connections
7. **Observability**: Enable Azure AI observability for production agents
8. **Approval Workflows**: Configure appropriate approval modes for sensitive operations

## Complete Example: Agent with Multiple Tool Types

```python
import asyncio
from typing import Annotated
from pydantic import Field
from agent_framework import ChatAgent, HostedMCPTool, MCPStdioTool, HostedWebSearchTool
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

# Custom function tool
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."

async def comprehensive_example():
    """Agent with function tools, hosted tools, and MCP tools."""
    async with (
        AzureCliCredential() as credential,
        MCPStdioTool(
            name="calculator",
            command="uvx",
            args=["mcp-server-calculator"]
        ) as calculator_mcp,
        AzureAIAgentClient(async_credential=credential) as chat_client,
    ):
        await chat_client.setup_azure_ai_observability()
        
        agent = chat_client.create_agent(
            name="SuperAgent",
            instructions="You are a versatile assistant with access to weather, calculations, web search, and Microsoft documentation.",
            tools=[
                # Function tool
                get_weather,
                # Hosted web search
                HostedWebSearchTool(),
                # Hosted MCP tool
                HostedMCPTool(
                    name="Microsoft Learn",
                    url="https://learn.microsoft.com/api/mcp",
                ),
                # Local MCP tool
                calculator_mcp,
            ],
        )
        
        result = await agent.run(
            "What's the weather in Seattle, calculate 15 * 23, and find Azure AI documentation?"
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(comprehensive_example())
```

## References

- [Agent Tools Overview](https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-tools?pivots=programming-language-python)
- [Using MCP Tools with Agents](https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-tools?pivots=programming-language-python)
- [Using MCP with Azure AI Foundry Agents](https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-with-foundry-agents?pivots=programming-language-python)
