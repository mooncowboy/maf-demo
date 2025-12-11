# Insurance Agent

An Azure AI Agent Service-based agent that helps users understand insurance policies.

## Overview

This agent uses the Microsoft Agent Framework (MAF) with Azure AI Agent Service to provide assistance with insurance-related questions. It can help users understand:

- Different types of insurance policies
- Coverage details
- Insurance terminology
- Policy comparisons

## Agent Type

- **Type**: Azure AI Foundry Agent (AzureAIAgentClient)
- **Persistence**: Non-persistent (session-based)
- **Runtime**: Azure AI Agent Service

## Prerequisites

1. Azure AI Agent Service endpoint and model deployment
2. Azure credentials configured (DefaultAzureCredential)
3. Required environment variables set

## Environment Variables

Create a `.env` file in the repository root with:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<your_service_name>.services.ai.azure.com/api/projects/<your_project_name>
AZURE_AI_MODEL_DEPLOYMENT_NAME=<your_model_deployment_name>
APPLICATIONINSIGHTS_CONNECTION_STRING=<your_application_insights_connection_string>
ENABLE_OTEL=True
```

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### CLI Mode

Run the agent from the repository root:

```bash
python -m src.agents.insure_agent.insure_agent
```

Or:

```bash
cd src/agents/insure_agent
python insure_agent.py
```

### DevUI Mode

Run the agent in DevUI:

```bash
devui ./src/agents/insure_agent --port 8080
```

Then open your browser to `http://localhost:8080`

## Example Interactions

```
You: What is term life insurance?
Agent: [Provides explanation of term life insurance]

You: What's the difference between comprehensive and collision coverage?
Agent: [Explains the differences]
```

## Features

- Non-persistent session-based interactions
- Azure AI Agent Service integration
- Observability via Application Insights
- Simple CLI interface

## Notes

- This agent does not provide legal or financial advice
- Information provided is for educational purposes
- Consult with licensed insurance professionals for specific policy decisions
