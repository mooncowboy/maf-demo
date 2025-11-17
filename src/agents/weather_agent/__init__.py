"""
Weather Agent - Azure AI Agent Service

This module exports the weather agent for use with the DevUI.
The agent must be exported as 'agent' to be discovered by the DevUI.
"""

from .weather_agent import agent

__all__ = ["agent"]
