# Weather Agent

An Azure AI agent that provides weather information for specific cities using mocked data.

## Overview

The Weather Agent is a conversational AI assistant built with the Microsoft Agent Framework (MAF) that can answer questions about weather conditions in 10 different cities around the world.

## Features

- **Weather Queries**: Get current weather information including temperature, condition, and humidity for any of the supported cities
- **City List**: View all available cities with weather data
- **Natural Conversation**: Interact naturally with the agent to ask about weather conditions

## Available Cities

The agent provides weather data for the following 10 cities:
- New York
- London
- Tokyo
- Paris
- Sydney
- Berlin
- Toronto
- Dubai
- Singapore
- Mumbai

## Architecture

- **Agent Type**: Azure AI Foundry / Azure AI Agent Service (non-persistent)
- **Runtime**: Azure AI with DefaultAzureCredential authentication
- **Tools**: 
  - `get_weather`: Retrieves weather data for a specific city
  - `list_cities`: Lists all available cities
- **Observability**: Integrated with Application Insights via OpenTelemetry

## Prerequisites

- Python 3.11 or higher
- Azure subscription with Azure AI Foundry project
- Azure CLI authenticated (`az login`) or appropriate credentials configured (e.g., DefaultAzureCredential)
- Required environment variables set (see below)

**Note**: The agent requires valid Azure credentials to run. Without proper authentication, the agent will fail when attempting to connect to Azure AI services.

## Environment Variables

The following environment variables must be set in the `.env` file:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your_service_name>.services.ai.azure.com/api/projects/<your_project_name>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your_model_deployment_name>
APPLICATIONINSIGHTS_CONNECTION_STRING=<your_application_insights_connection_string>
```

## Running the Agent

### CLI Mode

Run the agent directly from the command line:

```bash
# From the repository root
python src/agents/weather_agent/weather_agent.py
```

### DevUI Mode

Launch the agent in the DevUI for a visual interface:

```bash
# From the repository root
devui ./src/agents/weather_agent --port 8080
```

Then open your browser to `http://localhost:8080`

## Example Interactions

```
You: What's the weather like in Tokyo?
Agent: Weather in Tokyo: Rainy, Temperature: 68°F, Humidity: 85%

You: List all available cities
Agent: Available cities: New York, London, Tokyo, Paris, Sydney, Berlin, Toronto, Dubai, Singapore, Mumbai

You: Tell me about the weather in Paris
Agent: Weather in Paris: Partly Cloudy, Temperature: 64°F, Humidity: 70%
```

## Implementation Details

The agent uses:
- **Azure AI Agent Service** for the agent runtime
- **DefaultAzureCredential** for Azure authentication
- **Function tools** for weather data retrieval
- **Mocked data** stored in a Python dictionary for demonstration purposes

## Development

To modify the agent:

1. Edit `weather_agent.py` to change agent behavior or add new tools
2. Update the `WEATHER_DATA` dictionary to add or modify city data
3. Adjust the agent instructions to change how it responds to queries

## Notes

- This agent uses mocked weather data for demonstration purposes
- The agent is non-persistent, meaning it doesn't maintain state between runs
- All weather data is static and does not reflect real-time conditions
