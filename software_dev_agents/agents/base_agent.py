#!/usr/bin/env python3
"""Abstract base class for all agents."""

from abc import ABC, abstractmethod
from typing import Optional

from ..models import AgentRole, Task
from ..memory import ProjectMemory
from ..utils.logger import agent_logger


class BaseAgent(ABC):
    """Abstract base class for all software development agents."""

    def __init__(self, name: str, role: AgentRole, memory: ProjectMemory):
        self.name = name
        self.role = role
        self.memory = memory
        self.logger = agent_logger

    def communicate(self, to_agent: str, message: str):
        """Send a message to another agent."""
        self.memory.log_communication(self.name, to_agent, message)
        self.logger.log_communication(self.name, to_agent, message)

    def log_action(self, action: str, details: str = ""):
        """Log an action performed by this agent."""
        self.logger.log_agent_action(self.name, action, details)

    def log_error(self, error: str, details: str = ""):
        """Log an error encountered by this agent."""
        self.logger.log_error(self.name, error, details)

    @abstractmethod
    def get_capabilities(self) -> list:
        """Return a list of capabilities this agent provides."""
        pass

    def get_role_name(self) -> str:
        """Get the human-readable role name."""
        role_names = {
            AgentRole.PROJECT_MANAGER: "Project Manager",
            AgentRole.CODER: "Developer",
            AgentRole.QA_TESTER: "QA Tester"
        }
        return role_names.get(self.role, "Unknown Role")

    def can_handle_task(self, task: Task) -> bool:
        """Check if this agent can handle the given task."""
        return task.assigned_to == self.role