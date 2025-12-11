"""Insurance agent using Azure AI Agent Service to help users understand insurance policies."""

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from agent_framework_azure_ai import AzureAIAgentClient
from agent_framework.observability import setup_observability

# Load environment variables
load_dotenv()

# Setup observability
setup_observability()


def create_insure_agent() -> AzureAIAgentClient:
    """Create and return an insurance agent using Azure AI Agent Service.
    
    This agent helps users understand insurance policies.
    
    Returns:
        AzureAIAgentClient: A non-persistent Azure AI agent client
    """
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model_deployment_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    
    if not endpoint or not model_deployment_name:
        raise ValueError(
            "Missing required environment variables. "
            "Please set AZURE_AI_PROJECT_ENDPOINT and AZURE_AI_MODEL_DEPLOYMENT_NAME"
        )
    
    # Create non-persistent agent client
    agent = AzureAIAgentClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
        model=model_deployment_name,
        instructions="You are an insurance expert assistant. Help users understand insurance policies, coverage types, and answer questions about insurance. Be clear, concise, and helpful."
    )
    
    return agent


def main():
    """Run the insurance agent in CLI mode."""
    print("Insurance Agent - Help with understanding insurance policies")
    print("=" * 60)
    print("Type 'quit' or 'exit' to end the conversation.\n")
    
    try:
        agent = create_insure_agent()
        print("Agent initialized successfully!\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
            
            try:
                response = agent.run(user_input)
                print(f"\nAgent: {response}\n")
            except Exception as e:
                print(f"\nError processing request: {e}\n")
                
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
