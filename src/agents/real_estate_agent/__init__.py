"""
Real Estate Market Insights Agent

This module exports the real estate agent for use with the DevUI.
The agent must be exported as 'agent' to be discovered by the DevUI.
"""

# Import the agent from the real_estate_agent module
from .real_estate_agent import agent

# Re-export for DevUI discovery
__all__ = ['agent']
