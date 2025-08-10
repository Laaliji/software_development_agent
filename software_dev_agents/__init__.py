#!/usr/bin/env python3
"""Software Development Agent System

A collaborative multi-agent system for software development with PM, Coder, and QA roles.
"""

from .orchestrator import SoftwareDevTeam
from .models import TaskStatus, AgentRole, Task, BugReport
from .memory import ProjectMemory
from .agents import ProjectManagerAgent, CoderAgent, QAAgent

__version__ = "1.0.0"
__author__ = "AI Software Development Team"

__all__ = [
    'SoftwareDevTeam',
    'TaskStatus', 'AgentRole', 'Task', 'BugReport',
    'ProjectMemory',
    'ProjectManagerAgent', 'CoderAgent', 'QAAgent'
]