# Weather Agent

A weather information agent built with the Microsoft Agent Framework that provides weather data for 10 predefined cities using mocked data.

## Description

The Weather Agent is an Azure AI Agent Service-based agent (non-persistent) that responds to user queries about weather conditions in supported cities. It uses a simple tool function to fetch mocked weather data including temperature, weather conditions, and humidity levels.

## Features

- **10 Supported Cities**: New York, Los Angeles, Chicago, Houston, Miami, Seattle, Boston, San Francisco, Denver, and Phoenix
- **Mocked Weather Data**: Returns temperature, weather condition, and humidity for each city
- **Non-Persistent**: Creates a new agent instance for each session
- **Azure AI Agent Service**: Leverages Azure AI Foundry for agent execution

## Supported Cities

The agent provides weather information for the following cities:

1. New York
2. Los Angeles
3. Chicago
4. Houston
5. Miami
6. Seattle
7. Boston
8. San Francisco
9. Denver
10. Phoenix

## Prerequisites

Before running the agent, ensure you have:

1. **Python 3.11+** installed
2. **Azure AI Foundry project** with an AI Agent Service
3. **Environment variables** properly configured in `.env` file:
   - `AZURE_AI_PROJECT_ENDPOINT`: Your Azure AI project endpoint
   - `AZURE_AI_MODEL_DEPLOYMENT_NAME`: Your model deployment name
   - `APPLICATIONINSIGHTS_CONNECTION_STRING`: (Optional) Application Insights connection string for telemetry

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables by copying `.env.sample` to `.env` and filling in your values:
   ```bash
   cp .env.sample .env
   # Edit .env with your actual Azure credentials
   ```

## Usage

### Running in CLI Mode

Run the agent directly:

```bash
python src/agents/weather_agent/weather_agent.py
```

Example interaction:
```
You: What's the weather in New York?
Agent: Weather in New York: 72°F, Partly Cloudy, Humidity: 65%

You: Tell me about the weather in Seattle
Agent: Weather in Seattle: 62°F, Rainy, Humidity: 85%

You: What about Tokyo?
Agent: Weather data not available for Tokyo. Available cities: New York, Los Angeles, Chicago, Houston, Miami, Seattle, Boston, San Francisco, Denver, Phoenix
```

### Running with DevUI

Start the DevUI interface:

```bash
devui ./src/agents/weather_agent --port 8080
```

The agent will be automatically discovered and available in the DevUI interface.

## Tool Functions

### `get_weather(city: str) -> str`

Retrieves mocked weather information for a specified city.

**Parameters:**
- `city` (str): The name of the city

**Returns:**
- str: Weather information including temperature, condition, and humidity, or an error message if the city is not supported

## Agent Configuration

- **Agent Type**: Azure AI Agent (non-persistent)
- **Cleanup**: Automatically cleans up agent instances after session ends
- **Model**: Uses the model specified in `AZURE_AI_MODEL_DEPLOYMENT_NAME`
- **Instructions**: "You are a helpful weather assistant. Provide weather information for cities when asked. Use the get_weather tool to fetch weather data."

## Architecture

- **File Structure**:
  ```
  weather_agent/
  ├── __init__.py          # Exports agent for DevUI discovery
  ├── weather_agent.py     # Main agent implementation
  └── README.md           # This file
  ```

- **Key Components**:
  - `WEATHER_DATA`: Dictionary containing mocked weather data for 10 cities
  - `get_weather()`: Tool function for retrieving weather data
  - `create_agent()`: Factory function that creates the agent instance
  - `main()`: CLI interaction loop

## Observability

The agent includes OpenTelemetry observability integration. If Application Insights connection string is not configured, the agent will continue to work but will log a warning about telemetry being unavailable.

## Limitations

- Weather data is mocked and does not reflect real-time conditions
- Only 10 cities are supported
- Requires valid Azure AI Agent Service credentials to run

## Troubleshooting

### "Missing required environment variables" error
Ensure your `.env` file has valid values for `AZURE_AI_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT_NAME`.

### "Invalid connection string" warning
The Application Insights connection string is not properly configured. The agent will continue to work without telemetry.

### Authentication errors
Ensure you have proper Azure credentials configured. The agent uses `DefaultAzureCredential` which supports multiple authentication methods (Azure CLI, environment variables, managed identity, etc.).

## License

This agent is part of the MAF Demo repository and follows the same license terms.
