#!/usr/bin/env python3
"""Logging system for the software development agents."""

import logging
from datetime import datetime
from typing import Optional


class AgentLogger:
    """Custom logger for agent communications and actions."""

    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger("SoftwareDevAgents")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Create console handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_agent_action(self, agent_name: str, action: str, details: str = ""):
        """Log an agent action."""
        message = f"[{agent_name}] {action}"
        if details:
            message += f" - {details}"
        self.logger.info(message)

    def log_communication(self, from_agent: str, to_agent: str, message: str):
        """Log communication between agents."""
        comm_msg = f"[{from_agent}] → [{to_agent}]: {message}"
        self.logger.info(comm_msg)
        print(comm_msg)  # Also print to console for visibility

    def log_task_update(self, task_id: str, status: str, agent: str):
        """Log task status updates."""
        self.logger.info(f"Task {task_id} updated to {status} by {agent}")

    def log_error(self, agent_name: str, error: str, details: str = ""):
        """Log errors."""
        message = f"[{agent_name}] ERROR: {error}"
        if details:
            message += f" - {details}"
        self.logger.error(message)

    def log_project_milestone(self, milestone: str, details: str = ""):
        """Log project milestones."""
        message = f"🎯 MILESTONE: {milestone}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
        print(f"\n{message}\n")


# Global logger instance
agent_logger = AgentLogger()