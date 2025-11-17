"""
Weather Agent - Azure AI Agent Service
Allows users to query weather information for specific cities.
"""

import asyncio
import os
from typing import Annotated

from agent_framework.azure import AzureAIAgentClient
from agent_framework.observability import setup_observability
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

# Mock weather data for 10 cities
MOCK_WEATHER_DATA = {
    "New York": {"temperature": 72, "condition": "Partly Cloudy", "humidity": 65},
    "Los Angeles": {"temperature": 85, "condition": "Sunny", "humidity": 45},
    "Chicago": {"temperature": 68, "condition": "Cloudy", "humidity": 70},
    "Houston": {"temperature": 88, "condition": "Hot and Humid", "humidity": 80},
    "Phoenix": {"temperature": 95, "condition": "Clear", "humidity": 20},
    "Philadelphia": {"temperature": 70, "condition": "Overcast", "humidity": 60},
    "San Antonio": {"temperature": 90, "condition": "Sunny", "humidity": 50},
    "San Diego": {"temperature": 75, "condition": "Clear", "humidity": 55},
    "Dallas": {"temperature": 82, "condition": "Partly Cloudy", "humidity": 55},
    "San Jose": {"temperature": 78, "condition": "Foggy", "humidity": 75},
}


def get_weather(city: Annotated[str, "The name of the city to get weather for"]) -> str:
    """Get weather information for a city."""
    if city in MOCK_WEATHER_DATA:
        weather = MOCK_WEATHER_DATA[city]
        return f"Weather in {city}: {weather['temperature']}°F, {weather['condition']}, Humidity: {weather['humidity']}%"
    else:
        available_cities = ", ".join(MOCK_WEATHER_DATA.keys())
        return f"Sorry, weather data is only available for: {available_cities}"


def create_weather_agent() -> AzureAIAgentClient:
    """Create and configure the Weather Agent."""
    setup_observability()
    
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    
    if not endpoint or not model:
        raise ValueError(
            "AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME must be set"
        )
    
    # Create non-persistent Azure AI agent using create_agent
    client = AzureAIAgentClient(
        async_credential=DefaultAzureCredential()
    )
    
    return client.create_agent(
        name="WeatherAgent",
        instructions="You are a helpful weather assistant. Use the get_weather tool to provide weather information for cities. Only provide weather for the available cities.",
        tools=[get_weather],
    )


async def run_cli():
    """Run the weather agent in CLI mode."""
    weather_agent = create_weather_agent()
    
    print("Weather Agent - Type 'exit' or 'quit' to end the conversation")
    print(f"Available cities: {', '.join(MOCK_WEATHER_DATA.keys())}")
    print("-" * 60)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        response = await weather_agent.run(user_input)
        print(f"\nAgent: {response}")


# Setup observability at module level
setup_observability()

# Export agent for DevUI discovery
agent = AzureAIAgentClient(
    async_credential=DefaultAzureCredential()
).create_agent(
    name="WeatherAgent",
    instructions="You are a helpful weather assistant. Use the get_weather tool to provide weather information for cities. Only provide weather for the available cities.",
    tools=[get_weather],
)


if __name__ == "__main__":
    asyncio.run(run_cli())
