# Weather Agent

An Azure AI Agent Service agent that provides weather information for major US cities.

## Overview

The Weather Agent allows users to query weather information for 10 predefined major US cities using mocked data. This is a demonstration agent built using the Microsoft Agent Framework (MAF).

## Features

- **Weather Lookup Tool**: Get current weather conditions for supported cities
- **10 Mocked Cities**: New York, Los Angeles, Chicago, Houston, Phoenix, Philadelphia, San Antonio, San Diego, Dallas, San Jose
- **Azure AI Agent Service Integration**: Non-persistent agent using Azure AI
- **Observability**: Built-in Application Insights telemetry support

## Prerequisites

Before running this agent, you need:

1. **Azure AI Foundry Project**: Set up an Azure AI project
2. **Azure CLI**: Authenticated with appropriate permissions
3. **Environment Variables**: Configure the following in your `.env` file:
   ```
   AZURE_AI_PROJECT_ENDPOINT=https://<your_service>.services.ai.azure.com/api/projects/<your_project>
   AZURE_AI_MODEL_DEPLOYMENT_NAME=<your_model_deployment>
   ```

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env` file (see `.env.sample` for template)

3. Authenticate with Azure CLI:
   ```bash
   az login
   ```

## Usage

### Running via CLI

From the repository root:
```bash
python src/agents/weather_agent/weather_agent.py
```

Then interact with the agent:
```
You: What's the weather in New York?
Agent: [Weather information response]

You: Tell me about Chicago weather
Agent: [Weather information response]

You: exit
Goodbye!
```

### Running via DevUI

From the repository root:
```bash
devui ./src/agents/weather_agent --port 8080
```

Then open your browser to `http://localhost:8080` to interact with the agent through the web interface.

## Available Cities

The agent has mocked weather data for the following 10 cities:
- New York
- Los Angeles
- Chicago
- Houston
- Phoenix
- Philadelphia
- San Antonio
- San Diego
- Dallas
- San Jose

## Tool: get_weather

**Description**: Get weather information for a city

**Parameters**:
- `city` (string): The name of the city to get weather for

**Returns**: Weather information including temperature (°F), condition, and humidity percentage

**Example Tool Call**:
```python
get_weather("New York")
# Returns: "Weather in New York: 72°F, Partly Cloudy, Humidity: 65%"
```

## Architecture

- **Agent Type**: Azure AI Agent Service (non-persistent)
- **Runtime**: Local MAF agent connecting to Azure AI
- **Tools**: 1 function tool (get_weather)
- **Telemetry**: Application Insights (when ENABLE_OTEL=True)

## Development Notes

This agent was created following the Microsoft Agent Framework best practices:
- Uses official MAF Python SDK
- Follows DevUI discovery pattern (exports `agent` variable)
- Implements observability with Application Insights
- Uses Azure CLI credential for authentication
- Non-persistent agent (no agent ID storage)

## Limitations

- Weather data is mocked and not real-time
- Only supports 10 predefined US cities
- Requires Azure AI project setup and valid credentials
