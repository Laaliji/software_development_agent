#!/usr/bin/env python3
"""Main workflow orchestrator for the software development team."""

import json
from dataclasses import asdict
from typing import Dict

from ..memory import ProjectMemory
from ..agents import ProjectManagerAgent, CoderAgent, QAAgent
from ..models import TaskStatus, AgentRole
from ..utils.logger import agent_logger


class SoftwareDevTeam:
    """Main orchestrator for the software development team."""

    def __init__(self):
        self.memory = ProjectMemory()
        self.pm = ProjectManagerAgent(self.memory)
        self.coder = CoderAgent(self.memory)
        self.qa = QAAgent(self.memory)
        self.logger = agent_logger

    def develop_project(self, requirements: str):
        """Main development workflow."""
        self.logger.log_project_milestone("Starting Software Development Process")
        
        # Phase 1: Project Planning
        self._execute_planning_phase(requirements)
        
        # Phase 2: Development Loop
        self._execute_development_loop()
        
        # Phase 3: Final Report
        self._generate_final_report()

    def _execute_planning_phase(self, requirements: str):
        """Execute the project planning phase."""
        self.logger.log_project_milestone("Phase 1: Project Planning")
        
        tasks = self.pm.create_project_plan(requirements)
        self.logger.log_project_milestone(
            "Planning completed", 
            f"{len(tasks)} tasks created"
        )

    def _execute_development_loop(self):
        """Execute the main development loop."""
        self.logger.log_project_milestone("Phase 2: Development Loop")
        
        iteration = 1
        max_iterations = 10
        
        while iteration <= max_iterations:
            self.logger.log_project_milestone(f"Iteration {iteration}")
            
            # Get next task
            current_task = self.pm.assign_next_task()
            if not current_task:
                self.logger.log_project_milestone("No more tasks to assign")
                break

            # Execute task based on assigned agent
            if current_task.assigned_to == AgentRole.CODER:
                self._execute_coder_task(current_task)
            elif current_task.assigned_to == AgentRole.QA_TESTER:
                self._execute_qa_task(current_task)

            # Show progress
            self._log_progress()
            
            # Check if project is complete
            status = self.pm.get_project_status()
            if status['progress_percentage'] >= 100:
                self.logger.log_project_milestone("Project completed successfully! 🎉")
                break
                
            iteration += 1

    def _execute_coder_task(self, task):
        """Execute a coding task."""
        success = self.coder.implement_task(task)
        
        if success:
            # QA tests the implementation
            test_results = self.qa.run_tests(task)
            
            # Check for test failures and create bug reports
            failed_tests = [t for t in test_results if t.is_failing()]
            for failed_test in failed_tests:
                self.qa.create_bug_report(failed_test)

    def _execute_qa_task(self, task):
        """Execute a QA task."""
        test_results = self.qa.run_tests(task)
        self.memory.update_task_status(
            task.id, 
            TaskStatus.COMPLETED,
            f"Created {len(test_results)} tests"
        )

    def _log_progress(self):
        """Log current project progress."""
        status = self.pm.get_project_status()
        progress_msg = (
            f"Progress: {status['completed_tasks']}/{status['total_tasks']} "
            f"tasks completed ({status['progress_percentage']:.1f}%)"
        )
        
        if status['open_bugs'] > 0:
            progress_msg += f", {status['open_bugs']} open bugs"
        
        self.logger.log_project_milestone("Progress Update", progress_msg)

    def _generate_final_report(self):
        """Generate and save final project report."""
        self.logger.log_project_milestone("Phase 3: Final Report")
        
        status = self.pm.get_project_status()
        
        # Generate comprehensive report
        report = self._create_project_report(status)
        print(report)
        
        # Save project summary
        self._save_project_summary(status)
        
        self.logger.log_project_milestone(
            "Final report generated",
            f"Project files saved to: ./generated_project/"
        )

    def _create_project_report(self, status: Dict) -> str:
        """Create a detailed project report."""
        project_status = "COMPLETED" if status['progress_percentage'] >= 100 else "IN PROGRESS"
        
        report = f"""
=== PROJECT COMPLETION REPORT ===
Project Status: {project_status}
Tasks Completed: {status['completed_tasks']}/{status['total_tasks']}
Tasks Failed: {status['failed_tasks']}
Progress: {status['progress_percentage']:.1f}%
Open Bugs: {status['open_bugs']}
Critical Bugs: {status['critical_bugs']}
Files Created: {status['files_created']}

Generated Files:"""
        
        for filename in self.memory.project_files.keys():
            report += f"\n  - {filename}"
        
        # Add QA report if available
        if status['completed_tasks'] > 0:
            report += "\n\n" + self.qa.generate_test_report()
        
        return report

    def _save_project_summary(self, status: Dict):
        """Save detailed project summary to JSON."""
        summary = {
            "project_info": {
                "status": status,
                "completion_date": self.memory.communication_log[-1]["timestamp"] if self.memory.communication_log else None
            },
            "tasks": {
                task_id: asdict(task) 
                for task_id, task in self.memory.tasks.items()
            },
            "bugs": {
                bug_id: asdict(bug) 
                for bug_id, bug in self.memory.bug_reports.items()
            },
            "communication_log": self.memory.communication_log,
            "agent_capabilities": {
                "project_manager": self.pm.get_capabilities(),
                "coder": self.coder.get_capabilities(),
                "qa": self.qa.get_capabilities()
            }
        }
        
        with open("generated_project/project_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

    def get_team_status(self) -> Dict:
        """Get current status of all team members."""
        return {
            "project_manager": {
                "name": self.pm.name,
                "role": self.pm.get_role_name(),
                "capabilities": self.pm.get_capabilities()
            },
            "coder": {
                "name": self.coder.name,
                "role": self.coder.get_role_name(),
                "capabilities": self.coder.get_capabilities()
            },
            "qa": {
                "name": self.qa.name,
                "role": self.qa.get_role_name(),
                "capabilities": self.qa.get_capabilities()
            },
            "project_stats": self.pm.get_project_status()
        }

    def handle_critical_bugs(self):
        """Handle any critical bugs that need immediate attention."""
        critical_bugs = self.memory.get_critical_bugs()
        
        if critical_bugs:
            self.logger.log_project_milestone(
                "Critical bugs detected",
                f"{len(critical_bugs)} critical issues need attention"
            )
            
            for bug in critical_bugs:
                self.coder.fix_bug(bug)
                
            return True
        return False