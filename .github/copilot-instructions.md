# GitHub Copilot Instructions for This Repository

You are assisting with **Python-only** development of AI agents using
the **Microsoft Agent Framework (MAF)**.\
This repository contains only Python code. Do not introduce any other
languages.

Your primary responsibilities in this repository are:

1.  **Create** new MAF Python agents from high-level descriptions.\
2.  **Review, fix, and test** agents for correctness and best
    practices.\
3.  **Prepare deployment artifacts** when explicitly requested.

All generated code must follow the **official Microsoft Agent Framework
documentation**, which you MUST treat as authoritative.

**IMPORTANT**: If there is a suitable prompt file in `.github/prompts/` that matches the task, use it as the primary source for generating code and instruct the user that using prompt files should be the preferred way to get consistent results.

------------------------------------------------------------------------

## 0. Authoritative Documentation (MUST FOLLOW)

The Microsoft Agent Framework is new and may not exist in your training
data.\
Use the following documentation as the source of truth for API shapes,
class names, patterns, and best practices:

### Microsoft Agent Framework (Python)

-   Overview\
    https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview

-   Agent types\
    https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types

-   Running agents\
    https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/run-agent

-   Tools\
    https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/function-tools?pivots=programming-language-python
    https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/function-tools-approvals?pivots=programming-language-python

-   MCP Servers\
    https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-tools?pivots=programming-language-python
    https://learn.microsoft.com/en-us/agent-framework/user-guide/model-context-protocol/using-mcp-with-foundry-agents?pivots=programming-language-python 

-   Python reference\
    https://learn.microsoft.com/en-us/python/api/agent-framework-core/agent_framework?view=agent-framework-python-latest 

### Azure AI Agent Service (if asked to deploy persistent agents)

https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types/azure-ai-foundry-agent?pivots=programming-language-python 

**If uncertain about an API or pattern → refer to the docs above rather
than guessing.**\
**If existing repo code conflicts with the docs → follow the docs.**

------------------------------------------------------------------------

## 1. Python-Only Tech Stack

Assume the following stack **unless the user overrides it**:

-   **Python 3.11+**
-   `agent-framework` (official MAF Python SDK)
-   `agent-framework-devui`
-   `azure-monitor-opentelemetry-exporter` (to ensure telemetry goes to Application Insights)
-   `azure-identity`
-   `python-dotenv`
-   `httpx` for HTTP calls inside tools
-   `pytest` for testing
-   `ruff` / `mypy` if config exists in the repo

Make sure these are in the `requirements.txt` or equivalent and if there's a virtual environment, ensure packages are installed there.

Do **not** introduce: - Node, TypeScript, .NET, Go, Java\
- Non-Python Agent Framework client libraries\
- Unsupported frameworks

------------------------------------------------------------------------

## 2. Project Structure (MUST FOLLOW)

Place new files according to:

    src/
      agents/
        <agent_name>/
          <agent_name>.py
      tools/
        <tool_name>.py
      workflows/
        <workflow_name>/
          <workflow_name>.py
      config/
        <configuration>.py

    tests/
      agents/
        test_<agent_name>.py
      tools/
        test_<tool_name>.py

Rules:

-   Each agent = its own file under `src/agents/<agent_name>/<agent_name>.py`.
-   Each workflow = its own file under `src/workflows/<workflow_name>/<workflow_name>.py`.
-   Each tool = its own file under `src/tools/`.
-   Deployment-related files must go under `.github/workflows/` or
    `infra/` folders if they exist.

**Make sure agents and workflows are compatible with DevUI** by following the above instructions. Also, you'll need an __init__.py file in each agent and workflow folder to enable DevUI to discover them properly. The agent **must** be exported as `agent`. Check there for official docs: https://github.com/microsoft/agent-framework/tree/main/python/packages/devui 

**Do not modify** root `README.md` or other top-level documentation unless explicitly asked.

------------------------------------------------------------------------

## 3. Agent Design Rules (Strict)

When generating or updating an agent:

1.  **Follow MAF agent structure from the official docs.**\
    Do not invent new classes or method names not present in docs.

2.  **Clear responsibilities.**\
    Each agent should do *one job* only (e.g., "billing support agent").

3.  **Use tools for external logic.**\
    No HTTP calls, long logic, or database access directly in the agent:

    -   Create separate tool modules.
    -   Expose safe methods documented for LLM use.

4.  **System prompt must be concise and consistent.**

5.  **Configuration via environment variables**\
    Do not hardcode endpoints, keys, or secrets.

6.  **Logging & error handling**\
    Use Python `logging` and raise clear exceptions in tools.

7. Observability:
    When creating an agent, ensure it sends telemetry to Application Insights, unless the user specifies otherwise. Follow the official MAF documentation for integrating telemetry available here: https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-observability?pivots=programming-language-python#enable-observability-1

------------------------------------------------------------------------

## 4. Tools (Strict MAF Guidelines)

When generating tools, follow:
https://learn.microsoft.com/en-us/agent-framework/user-guide/tools/overview

Rules:

-   One class or method per conceptual operation.
-   Clear docstrings explaining purpose and inputs.
-   Typed parameters and returns.
-   Do not include credentials or secrets.
-   Should be deterministic and LLM-friendly.

------------------------------------------------------------------------

## 5. Workflow Behavior (Creation → Review → Deployment)

### 5.1 Agent Creation

When asked to create an agent:

1.  Ask only for missing **critical** details.\
2.  Output a short **plan as bullet points**.\
3.  Create:
    -   `src/agents/<name>.py`
    -   Necessary tools under `src/tools/`
    -   Tests under `tests/...`
4.  Follow patterns from official MAF examples.

### 5.2 Agent Review & Fixing

When asked to review or improve an agent:

-   Check against official MAF Python examples.
-   Ensure all external logic is moved to tools.
-   Ensure typings, docstrings, and clarity.
-   Propose minimal diffs, not full rewrites.
-   Add or update `pytest` tests when needed.

### 5.3 Deployment (Only When Requested)

If the user explicitly asks:

-   Identify the deployment target (Azure Container Apps, Azure
    Functions, Azure AI Agent Service).
-   Create or modify:
    -   Dockerfile\
    -   Bicep/Terraform if present\
    -   GitHub Actions workflows\
-   Never hardcode secrets.\
-   Use environment variables or Key Vault references.

Do not modify deployment pipelines unless the user requests it.

------------------------------------------------------------------------

## 6. Interaction Style

When responding:

-   Be concise and focused.
-   Prefer short checklists over long paragraphs.
-   For code changes, provide **minimal diffs or full file content only
    when needed**.
-   Highlight assumptions.
-   Never invent unsupported MAF APIs.

If unsure about an API:

**Stop → consult the official MAF docs linked above → apply that
pattern.**

------------------------------------------------------------------------

## 7. Conflict Resolution Rules

When instructions conflict:

1.  **Explicit user instructions** override everything.\
2.  **Prompt files** override repo-wide defaults.\
3.  **This file** overrides heuristics.\
4.  **Official MAF docs** override existing repo code.
