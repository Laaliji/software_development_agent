#!/usr/bin/env python3
"""Centralized memory system for all agents."""

import os
from typing import Dict, List, Optional
from datetime import datetime

from ..models import Task, BugReport, TaskStatus
from ..utils.file_utils import save_project_file


class ProjectMemory:
    """Shared memory system for all agents."""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.bug_reports: Dict[str, BugReport] = {}
        self.project_files: Dict[str, str] = {}  # filename -> content
        self.communication_log: List[Dict] = []
        self.project_status = "active"

    def add_task(self, task: Task):
        """Add a task to memory."""
        self.tasks[task.id] = task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with a specific status."""
        return [task for task in self.tasks.values() if task.status == status]

    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks sorted by priority."""
        pending = self.get_tasks_by_status(TaskStatus.PENDING)
        return sorted(pending, key=lambda x: x.priority)

    def get_completed_task_ids(self) -> List[str]:
        """Get IDs of all completed tasks."""
        return [task.id for task in self.tasks.values() 
                if task.status == TaskStatus.COMPLETED]

    def update_task_status(self, task_id: str, status: TaskStatus, notes: str = ""):
        """Update task status with optional notes."""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = status
            if notes:
                task.completion_notes = notes

    def add_bug_report(self, bug: BugReport):
        """Add a bug report to memory."""
        self.bug_reports[bug.id] = bug

    def get_open_bugs(self) -> List[BugReport]:
        """Get all open (unfixed) bugs."""
        return [bug for bug in self.bug_reports.values() if bug.fixed_at is None]

    def get_critical_bugs(self) -> List[BugReport]:
        """Get all critical severity bugs."""
        return [bug for bug in self.bug_reports.values() if bug.is_critical()]

    def log_communication(self, from_agent: str, to_agent: str, message: str):
        """Log communication between agents."""
        self.communication_log.append({
            "timestamp": datetime.now().isoformat(),
            "from": from_agent,
            "to": to_agent,
            "message": message
        })

    def save_file(self, filename: str, content: str):
        """Save file to memory and filesystem."""
        self.project_files[filename] = content
        save_project_file(filename, content)

    def get_project_stats(self) -> Dict:
        """Get comprehensive project statistics."""
        total_tasks = len(self.tasks)
        completed_tasks = len(self.get_tasks_by_status(TaskStatus.COMPLETED))
        failed_tasks = len(self.get_tasks_by_status(TaskStatus.FAILED))
        open_bugs = len(self.get_open_bugs())
        critical_bugs = len(self.get_critical_bugs())

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "progress_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "open_bugs": open_bugs,
            "critical_bugs": critical_bugs,
            "files_created": len(self.project_files)
        }