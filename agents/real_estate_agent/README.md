# Real Estate Market Insights Agent

An Azure AI Foundry Agent specialized in real estate market analysis and insights.

## 🏡 Features

- **Property Search**: Search for properties by location, type, price range, and bedrooms
- **Market Trend Analysis**: Analyze market trends for specific locations and timeframes
- **Mortgage Calculator**: Calculate monthly payments with detailed cost breakdowns
- **Neighborhood Information**: Get comprehensive neighborhood profiles
- **Property Comparison**: Compare multiple properties side-by-side

## 📁 Directory Structure

This agent is organized for DevUI discovery:

```
agents/
├── __init__.py
└── real_estate_agent/
    ├── __init__.py              # Exports 'agent' variable
    └── real_estate_agent.py     # Agent implementation with tools
```

## 🚀 Usage

### With DevUI

The agent is automatically discovered by the DevUI when you run:

```bash
python -m agent_framework.devui
```

Navigate to the DevUI interface and select "Real Estate Insights Agent" from the available agents.

### Standalone

You can also run the agent standalone:

```bash
python agents/real_estate_agent/real_estate_agent.py
```

## 🔧 Configuration

The agent uses environment variables from the root `.env` file:

```env
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

## 💬 Example Queries

- "What are the current market trends in Seattle?"
- "Search for houses in Portland with 3 bedrooms under $500,000"
- "Calculate the monthly mortgage for a $450,000 home with 20% down"
- "Tell me about the neighborhood in Capitol Hill, Seattle"
- "Compare these properties: 123 Main St, 456 Oak Ave"

## 🛠️ Tools

The agent has access to the following tools:

1. **search_properties**: Search for properties matching criteria
2. **get_market_trends**: Get market analysis for a location
3. **calculate_mortgage**: Calculate mortgage payments
4. **get_neighborhood_info**: Get neighborhood details
5. **compare_properties**: Compare multiple properties

## 📝 Notes

- All property data is currently simulated for demonstration purposes
- In production, these tools should be connected to real estate APIs
- The agent uses Azure CLI authentication by default
