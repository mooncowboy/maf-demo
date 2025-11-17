"""
Weather Agent

This module exports the weather agent for use with the DevUI.
The agent must be exported as 'agent' to be discovered by the DevUI.
"""

# Import the agent from the weather_agent module
from .weather_agent import agent

# Re-export for DevUI discovery
__all__ = ['agent']
