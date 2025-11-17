# MAF Demo - Automate Agent Creation with GitHub Copilot

Accelerate AI agent development with the **Microsoft Agent Framework (MAF)** using GitHub Copilot prompts and custom agents.

## Purpose

This repository demonstrates how to **automate the creation and review of MAF agents** using GitHub Copilot. Instead of manually writing boilerplate code, use pre-built prompts and specialized Copilot agents to generate production-ready agent code quickly and consistently.

The goal is to:
- Reduce repetitive coding tasks when building MAF agents
- Ensure agents follow official MAF best practices and documentation
- Provide a starting point for developers learning the Microsoft Agent Framework
- Foster a community-driven collection of reusable prompts and agent templates

## Available Resources

### 📝 Prompts

Located in `.github/prompts/`:

- **`maf-create-agent.prompt.md`** - Comprehensive prompt for creating new MAF agents with proper structure, DevUI compatibility, and telemetry

### 🤖 GitHub Copilot Agents

Located in `.github/agents/`:

- **`MAFAgentCreator`** - Specialized agent for creating new MAF agents following official documentation
- **`MAFAgentReviewer`** - Expert reviewer that validates agent correctness, structure, and compliance

### 🏗️ Example Agents

Located in `src/agents/`:

- **`real_estate_agent`** - A fully functional real estate market insights agent demonstrating:
  - Property search capabilities
  - Market trend analysis
  - Mortgage calculations
  - Neighborhood insights
  - Property comparisons

This example shows what a complete MAF agent looks like when generated using the automation tools in this repository.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Azure subscription with Azure AI Foundry project
- Azure CLI installed and authenticated
- GitHub Copilot enabled in VS Code

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mooncowboy/maf-demo.git
   cd maf-demo
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   AZURE_AI_PROJECT_ENDPOINT=<your-azure-ai-endpoint>
   AZURE_AI_MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
   APPLICATIONINSIGHTS_CONNECTION_STRING=<your-app-insights-connection-string>
   ```

### Running an Agent

#### Using the CLI

Run any agent directly:
```bash
python src/agents/real_estate_agent/real_estate_agent.py
```

#### Using MAF DevUI

For a visual interface to interact with agents:
```bash
# From the repository root
devui .
```

The DevUI will automatically discover all agents that follow the proper structure (exports named `agent` in `__init__.py`).

### Creating Your Own Agent

#### Option 1: Use GitHub Copilot Chat Agents (Recommended)

1. Open GitHub Copilot Chat in VS Code
2. Type `@MAFAgentCreator create a new agent for [your use case]`
3. Follow the prompts to specify agent type, name, and purpose
4. The agent will be created with proper structure and best practices

#### Option 2: Use the Prompt File

1. Open `.github/prompts/maf-create-agent.prompt.md`
2. Reference this prompt in Copilot Chat: `Use #file:maf-create-agent.prompt.md to create...`
3. Provide the required information (agent name, type, purpose)
4. Let Copilot generate the code

#### Option 3: Use Copilot Instructions

The repository includes `.github/copilot-instructions.md` which automatically guides Copilot when you work in this workspace. Simply describe what you want to build, and Copilot will follow the MAF best practices.

## Repository Structure

```
maf-demo/
├── .github/
│   ├── agents/              # GitHub Copilot custom agents
│   │   ├── MAFAgentCreator.agent.md
│   │   └── MAFAgentReviewer.agent.md
│   ├── prompts/             # Reusable prompts for agent creation
│   │   └── maf-create-agent.prompt.md
│   └── copilot-instructions.md  # Workspace-wide Copilot guidance
├── src/
│   ├── agents/              # Your MAF agents
│   │   └── real_estate_agent/
│   ├── tools/               # Reusable tools for agents
│   └── workflows/           # Multi-agent workflows
├── tests/                   # Unit tests
├── requirements.txt
└── README.md
```

## Contributing

We welcome contributions! Help grow this collection of MAF automation resources:

### How to Contribute

1. **Add New Prompts** - Create specialized prompts for different agent types or use cases
2. **Create Copilot Agents** - Build custom agents that automate specific MAF development tasks
3. **Share Example Agents** - Contribute well-documented example agents for different domains
4. **Improve Documentation** - Enhance instructions, add tutorials, or fix errors

### Contribution Guidelines

- Follow the existing project structure
- Ensure all prompts reference official MAF documentation
- Test agents before submitting
- Include clear descriptions and usage examples
- Update this README with new resources

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-prompt`)
3. Commit your changes (`git commit -m 'Add new MAF prompt for...'`)
4. Push to the branch (`git push origin feature/new-prompt`)
5. Open a Pull Request

## Resources

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [MAF Python API Reference](https://learn.microsoft.com/en-us/python/api/agent-framework-core/agent_framework)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-studio/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with ❤️ using the Microsoft Agent Framework and GitHub Copilot.
