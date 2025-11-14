"""
Delete all agents from Azure AI Agent Service (Azure AI Foundry)

This script lists and deletes all agents in the configured Azure AI project.
It uses the Azure AI Projects client to manage persistent agents.
"""

import asyncio
import os
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def delete_all_agents():
    """Delete all agents from Azure AI Agent Service."""
    
    # Get configuration from environment
    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    
    if not endpoint:
        print("Error: AZURE_AI_PROJECT_ENDPOINT environment variable not set")
        print("Please set it in your .env file")
        return
    
    print(f"Connecting to Azure AI Project: {endpoint}")
    print("-" * 80)
    
    async with (
        AzureCliCredential() as credential,
        AIProjectClient(
            endpoint=endpoint,
            credential=credential
        ) as project_client,
    ):
        try:
            # List all agents
            print("Fetching list of agents...")
            agents_list = []
            async for agent in project_client.agents.list_agents():
                agents_list.append(agent)
            
            if not agents_list:
                print("\nNo agents found in the project.")
                return
            
            print(f"\nFound {len(agents_list)} agent(s):\n")
            
            # Display agent information
            for i, agent in enumerate(agents_list, 1):
                print(f"{i}. Name: {agent.name}")
                print(f"   ID: {agent.id}")
                print(f"   Model: {agent.model}")
                print(f"   Created: {agent.created_at}")
                print()
            
            # Confirm deletion
            response = input("\nDo you want to delete ALL these agents? (yes/no): ")
            
            if response.lower() not in ['yes', 'y']:
                print("Deletion cancelled.")
                return
            
            # Delete each agent
            print("\nDeleting agents...")
            deleted_count = 0
            failed_count = 0
            
            for agent in agents_list:
                try:
                    await project_client.agents.delete_agent(agent.id)
                    print(f"✓ Deleted: {agent.name} (ID: {agent.id})")
                    deleted_count += 1
                except Exception as e:
                    print(f"✗ Failed to delete {agent.name} (ID: {agent.id}): {str(e)}")
                    failed_count += 1
            
            print("-" * 80)
            print(f"\nDeletion complete:")
            print(f"  Successfully deleted: {deleted_count}")
            print(f"  Failed: {failed_count}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print("\nMake sure you are authenticated with Azure CLI:")
            print("  az login")


if __name__ == "__main__":
    asyncio.run(delete_all_agents())
