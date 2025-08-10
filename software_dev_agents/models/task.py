#!/usr/bin/env python3
"""Task model with business logic."""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from .enums import AgentRole, TaskStatus, Priority


@dataclass
class Task:
    id: str
    title: str
    description: str
    assigned_to: AgentRole
    status: TaskStatus
    priority: int  # 1-5, 1 being highest
    dependencies: List[str]
    created_at: str
    due_date: Optional[str] = None
    completion_notes: Optional[str] = None
    code_files: List[str] = None

    def __post_init__(self):
        if self.code_files is None:
            self.code_files = []

    def mark_in_progress(self):
        """Mark task as in progress."""
        self.status = TaskStatus.IN_PROGRESS

    def mark_completed(self, notes: str = ""):
        """Mark task as completed with optional notes."""
        self.status = TaskStatus.COMPLETED
        self.completion_notes = notes

    def mark_failed(self, error_message: str):
        """Mark task as failed with error message."""
        self.status = TaskStatus.FAILED
        self.completion_notes = error_message

    def add_code_file(self, filename: str):
        """Add a code file to this task."""
        if filename not in self.code_files:
            self.code_files.append(filename)

    def is_ready_to_start(self, completed_tasks: List[str]) -> bool:
        """Check if all dependencies are completed."""
        return all(dep_id in completed_tasks for dep_id in self.dependencies)

    def get_priority_label(self) -> str:
        """Get human-readable priority label."""
        priority_map = {1: "Critical", 2: "High", 3: "Medium", 4: "Low", 5: "Lowest"}
        return priority_map.get(self.priority, "Unknown")