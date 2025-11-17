"""
Weather Agent

An Azure AI agent that provides weather information for specific cities.
"""

import asyncio
import os
from typing import Annotated

from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from agent_framework.azure import AzureAIAgentClient
from agent_framework.observability import setup_observability

# Load environment variables
load_dotenv()

# Weather data for 10 mocked cities
WEATHER_DATA = {
    "New York": {"temperature": 72, "condition": "Sunny", "humidity": 65},
    "London": {"temperature": 59, "condition": "Cloudy", "humidity": 78},
    "Tokyo": {"temperature": 68, "condition": "Rainy", "humidity": 85},
    "Paris": {"temperature": 64, "condition": "Partly Cloudy", "humidity": 70},
    "Sydney": {"temperature": 75, "condition": "Sunny", "humidity": 60},
    "Berlin": {"temperature": 57, "condition": "Windy", "humidity": 72},
    "Toronto": {"temperature": 66, "condition": "Clear", "humidity": 68},
    "Dubai": {"temperature": 95, "condition": "Hot and Sunny", "humidity": 45},
    "Singapore": {"temperature": 88, "condition": "Humid", "humidity": 90},
    "Mumbai": {"temperature": 86, "condition": "Monsoon", "humidity": 88}
}


def get_weather(city: Annotated[str, "The name of the city to get weather for"]) -> str:
    """
    Get weather information for a specific city.
    
    Args:
        city: The name of the city
        
    Returns:
        Weather information as a string
    """
    if city in WEATHER_DATA:
        weather = WEATHER_DATA[city]
        return f"Weather in {city}: {weather['condition']}, Temperature: {weather['temperature']}°F, Humidity: {weather['humidity']}%"
    else:
        available_cities = ", ".join(WEATHER_DATA.keys())
        return f"Sorry, weather data is not available for {city}. Available cities are: {available_cities}"


def list_cities() -> str:
    """
    List all available cities with weather data.
    
    Returns:
        A comma-separated list of available cities
    """
    return "Available cities: " + ", ".join(WEATHER_DATA.keys())


# Initialize the Azure AI client
client = AzureAIAgentClient(
    async_credential=DefaultAzureCredential(),
    project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
    model_deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
)

# Create the agent (non-persistent)
agent = client.create_agent(
    name="WeatherAgent",
    instructions="You are a helpful weather assistant. You can provide weather information for specific cities. Use the get_weather tool to fetch weather data for a city, and the list_cities tool to show available cities.",
    tools=[get_weather, list_cities]
)


async def main():
    """Main CLI interaction loop."""
    # Setup observability
    setup_observability()
    
    print("Weather Agent - Type 'exit' or 'quit' to end the conversation.")
    print("Ask about weather in any of these cities:", ", ".join(WEATHER_DATA.keys()))
    print("-" * 80)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            response = await agent.run(user_input)
            print(f"\nAgent: {response}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
