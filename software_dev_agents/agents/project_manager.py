#!/usr/bin/env python3
"""Project Manager Agent implementation."""

import uuid
from datetime import datetime
from typing import List, Optional, Dict

from .base_agent import BaseAgent
from ..models import Task, TaskStatus, AgentRole
from ..memory import ProjectMemory


class ProjectManagerAgent(BaseAgent):
    """Project Manager agent responsible for planning and coordination."""

    def __init__(self, memory: ProjectMemory):
        super().__init__("ProjectManager", AgentRole.PROJECT_MANAGER, memory)

    def get_capabilities(self) -> list:
        """Return PM capabilities."""
        return [
            "Project planning",
            "Task creation and assignment",
            "Progress tracking",
            "Resource coordination",
            "Status reporting"
        ]

    def create_project_plan(self, requirements: str) -> List[Task]:
        """Create initial project plan based on requirements."""
        self.log_action("Creating project plan", f"Requirements: {requirements[:100]}...")
        
        # Create tasks based on requirements analysis
        tasks = self._analyze_requirements_and_create_tasks(requirements)
        
        # Add tasks to memory
        for task in tasks:
            self.memory.add_task(task)
        
        self.communicate("Coder", f"Created {len(tasks)} tasks for the project")
        self.log_action("Project plan created", f"{len(tasks)} tasks generated")
        
        return tasks

    def _analyze_requirements_and_create_tasks(self, requirements: str) -> List[Task]:
        """Analyze requirements and generate appropriate tasks."""
        # For demo, creating a simple todo app plan
        # In a real implementation, this would use NLP/AI to analyze requirements
        
        base_tasks = [
            {
                "title": "Setup project structure",
                "description": "Create basic project structure with HTML, CSS, JS files",
                "assigned_to": AgentRole.CODER,
                "priority": 1
            },
            {
                "title": "Implement HTML structure", 
                "description": "Create the main HTML file with todo list structure",
                "assigned_to": AgentRole.CODER,
                "priority": 1
            },
            {
                "title": "Implement CSS styling",
                "description": "Style the todo application with modern CSS",
                "assigned_to": AgentRole.CODER,
                "priority": 2
            },
            {
                "title": "Implement JavaScript functionality",
                "description": "Add/delete/toggle todo items functionality", 
                "assigned_to": AgentRole.CODER,
                "priority": 1
            },
            {
                "title": "Write unit tests",
                "description": "Create comprehensive tests for todo functionality",
                "assigned_to": AgentRole.QA_TESTER,
                "priority": 2
            }
        ]

        tasks = []
        for task_data in base_tasks:
            task = Task(
                id=str(uuid.uuid4()),
                title=task_data["title"],
                description=task_data["description"],
                assigned_to=task_data["assigned_to"],
                status=TaskStatus.PENDING,
                priority=task_data["priority"],
                dependencies=[],
                created_at=datetime.now().isoformat()
            )
            tasks.append(task)

        return tasks

    def assign_next_task(self) -> Optional[Task]:
        """Find and assign the next available task."""
        pending_tasks = self.memory.get_pending_tasks()
        completed_task_ids = self.memory.get_completed_task_ids()
        
        # Find tasks that are ready to start (dependencies met)
        ready_tasks = [
            task for task in pending_tasks 
            if task.is_ready_to_start(completed_task_ids)
        ]
        
        if not ready_tasks:
            return None

        # Get highest priority task
        next_task = ready_tasks[0]
        next_task.mark_in_progress()
        
        agent_name = "Coder" if next_task.assigned_to == AgentRole.CODER else "QA"
        self.communicate(agent_name, f"Assigned task: {next_task.title}")
        self.log_action("Task assigned", f"{next_task.title} to {agent_name}")
        
        return next_task

    def get_project_status(self) -> Dict:
        """Get comprehensive project status."""
        return self.memory.get_project_stats()

    def review_progress(self) -> str:
        """Generate a progress review report."""
        stats = self.get_project_status()
        
        report = f"""
=== PROJECT PROGRESS REVIEW ===
Total Tasks: {stats['total_tasks']}
Completed: {stats['completed_tasks']}
Failed: {stats['failed_tasks']}
Progress: {stats['progress_percentage']:.1f}%
Open Bugs: {stats['open_bugs']}
Critical Bugs: {stats['critical_bugs']}
Files Created: {stats['files_created']}
"""
        
        self.log_action("Progress review generated")
        return report

    def prioritize_tasks(self) -> List[Task]:
        """Re-prioritize pending tasks based on current project state."""
        pending_tasks = self.memory.get_pending_tasks()
        critical_bugs = self.memory.get_critical_bugs()
        
        # If there are critical bugs, prioritize bug fixes
        if critical_bugs:
            self.log_action("Critical bugs detected", f"{len(critical_bugs)} critical issues")
            # In a real implementation, would create bug fix tasks
        
        return pending_tasks