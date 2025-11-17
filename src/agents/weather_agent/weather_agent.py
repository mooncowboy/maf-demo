"""
Weather Agent - Provides weather information for specific cities using mocked data.
"""

import asyncio
import os
from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from agent_framework_azure_ai import AzureAIAgentClient
from agent_framework.observability import setup_observability

# Load environment variables
load_dotenv()

# Mocked weather data for 10 cities
WEATHER_DATA = {
    "New York": {"temperature": "72°F", "condition": "Partly Cloudy", "humidity": "65%"},
    "Los Angeles": {"temperature": "85°F", "condition": "Sunny", "humidity": "45%"},
    "Chicago": {"temperature": "68°F", "condition": "Cloudy", "humidity": "70%"},
    "Houston": {"temperature": "88°F", "condition": "Hot and Humid", "humidity": "80%"},
    "Miami": {"temperature": "82°F", "condition": "Sunny", "humidity": "75%"},
    "Seattle": {"temperature": "62°F", "condition": "Rainy", "humidity": "85%"},
    "Boston": {"temperature": "70°F", "condition": "Partly Cloudy", "humidity": "60%"},
    "San Francisco": {"temperature": "65°F", "condition": "Foggy", "humidity": "70%"},
    "Denver": {"temperature": "75°F", "condition": "Sunny", "humidity": "35%"},
    "Phoenix": {"temperature": "95°F", "condition": "Very Hot", "humidity": "25%"}
}


def get_weather(city: str) -> str:
    """Get weather information for a specific city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        Weather information including temperature, condition, and humidity
    """
    if city in WEATHER_DATA:
        weather = WEATHER_DATA[city]
        return f"Weather in {city}: {weather['temperature']}, {weather['condition']}, Humidity: {weather['humidity']}"
    else:
        available_cities = ", ".join(WEATHER_DATA.keys())
        return f"Weather data not available for {city}. Available cities: {available_cities}"


def create_agent():
    """Create and return a weather agent instance."""
    # Set up observability (skip if connection string is not properly configured)
    try:
        setup_observability()
    except (ValueError, Exception) as e:
        print(f"Warning: Could not set up observability: {e}")
        print("Continuing without telemetry...")
    
    # Get configuration from environment
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model_deployment_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    
    if not project_endpoint or not model_deployment_name:
        raise ValueError(
            "Missing required environment variables. "
            "Please set AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME"
        )
    
    # Create async credential
    credential = DefaultAzureCredential()
    
    # Create Azure AI Agent client (non-persistent)
    # This will create a new agent for each session and clean it up automatically
    client = AzureAIAgentClient(
        project_endpoint=project_endpoint,
        model_deployment_name=model_deployment_name,
        async_credential=credential,
        should_cleanup_agent=True
    )
    
    # Create the agent with instructions and tools
    agent = client.create_agent(
        name="Weather Agent",
        instructions="You are a helpful weather assistant. Provide weather information for cities when asked. Use the get_weather tool to fetch weather data.",
        tools=[get_weather]
    )
    
    return agent


# Create agent instance for DevUI discovery
agent = create_agent()


async def run_agent_async():
    """Run the weather agent in interactive CLI mode (async)."""
    print("Weather Agent - Ask me about the weather in any of our supported cities!")
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    agent = create_agent()
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        
        try:
            response = await agent.run(user_input)
            print(f"Agent: {response.content}\n")
        except Exception as e:
            print(f"Error: {e}\n")


def main():
    """Run the weather agent in interactive CLI mode."""
    asyncio.run(run_agent_async())


if __name__ == "__main__":
    main()
