#!/usr/bin/env python3
"""QA Agent implementation."""

import uuid
from datetime import datetime
from typing import List

from .base_agent import BaseAgent
from ..models import Task, TaskStatus, AgentRole, BugReport, TestResult, Severity
from ..memory import ProjectMemory


class QAAgent(BaseAgent):
    """QA agent responsible for testing and quality assurance."""

    def __init__(self, memory: ProjectMemory):
        super().__init__("QA", AgentRole.QA_TESTER, memory)

    def get_capabilities(self) -> list:
        """Return QA capabilities."""
        return [
            "Unit testing",
            "Integration testing",
            "Bug reporting",
            "Code quality analysis",
            "Test automation",
            "Performance testing"
        ]

    def run_tests(self, task: Task) -> List[TestResult]:
        """Run tests for the implemented functionality."""
        self.log_action("Running tests", task.title)
        
        test_results = []

        # Route to appropriate test methods based on task
        if "HTML" in task.title:
            test_results.extend(self._test_html_file())
        elif "CSS" in task.title:
            test_results.extend(self._test_css_file())
        elif "JavaScript" in task.title:
            test_results.extend(self._test_js_file())
        elif "project structure" in task.title:
            test_results.extend(self._test_project_structure())

        # Report results
        passed_tests = len([t for t in test_results if t.is_passing()])
        total_tests = len(test_results)
        
        self.communicate("ProjectManager", 
                        f"Tests completed: {passed_tests}/{total_tests} passed")
        self.log_action("Test execution completed", 
                       f"{passed_tests}/{total_tests} tests passed")
        
        return test_results

    def _test_project_structure(self) -> List[TestResult]:
        """Test project structure."""
        results = []
        
        if "README.md" in self.memory.project_files:
            results.append(TestResult(
                "readme_exists", "pass", 
                "README.md exists", "README.md"
            ))
        else:
            results.append(TestResult(
                "readme_exists", "fail", 
                "README.md missing", "README.md"
            ))
        
        return results

    def _test_html_file(self) -> List[TestResult]:
        """Test HTML file."""
        results = []
        
        if "index.html" in self.memory.project_files:
            html_content = self.memory.project_files["index.html"]
            
            # Test for required elements
            required_elements = [
                ("todoInput", "Input field"),
                ("addBtn", "Add button"),
                ("todoList", "Todo list"),
                ("totalTasks", "Total tasks counter"),
                ("completedTasks", "Completed tasks counter")
            ]
            
            for element_id, description in required_elements:
                if element_id in html_content:
                    results.append(TestResult(
                        f"html_{element_id}_exists", "pass",
                        f"{description} exists", "index.html"
                    ))
                else:
                    results.append(TestResult(
                        f"html_{element_id}_exists", "fail",
                        f"{description} missing", "index.html"
                    ))
        else:
            results.append(TestResult(
                "html_file_exists", "fail",
                "index.html missing", "index.html"
            ))
        
        return results

    def _test_css_file(self) -> List[TestResult]:
        """Test CSS file."""
        results = []
        
        if "styles.css" in self.memory.project_files:
            css_content = self.memory.project_files["styles.css"]
            
            # Test for required styles
            required_styles = [
                (".container", "Container styling"),
                (".todo-item", "Todo item styling"),
                (".input-section", "Input section styling"),
                (".stats", "Statistics styling")
            ]
            
            for selector, description in required_styles:
                if selector in css_content:
                    results.append(TestResult(
                        f"css_{selector.replace('.', '')}_style", "pass",
                        f"{description} exists", "styles.css"
                    ))
                else:
                    results.append(TestResult(
                        f"css_{selector.replace('.', '')}_style", "fail",
                        f"{description} missing", "styles.css"
                    ))
        else:
            results.append(TestResult(
                "css_file_exists", "fail",
                "styles.css missing", "styles.css"
            ))
        
        return results

    def _test_js_file(self) -> List[TestResult]:
        """Test JavaScript file."""
        results = []
        
        if "script.js" in self.memory.project_files:
            js_content = self.memory.project_files["script.js"]
            
            # Test for required functionality
            required_functions = [
                ("class TodoApp", "TodoApp class"),
                ("addTodo", "Add todo function"),
                ("toggleTodo", "Toggle todo function"),
                ("deleteTodo", "Delete todo function"),
                ("updateStats", "Update statistics function")
            ]
            
            for func_name, description in required_functions:
                if func_name in js_content:
                    results.append(TestResult(
                        f"js_{func_name.replace(' ', '_').lower()}", "pass",
                        f"{description} exists", "script.js"
                    ))
                else:
                    results.append(TestResult(
                        f"js_{func_name.replace(' ', '_').lower()}", "fail",
                        f"{description} missing", "script.js"
                    ))
        else:
            results.append(TestResult(
                "js_file_exists", "fail",
                "script.js missing", "script.js"
            ))
        
        return results

    def create_bug_report(self, test_result: TestResult) -> BugReport:
        """Create a bug report from a failed test."""
        severity = self._determine_bug_severity(test_result)
        
        bug = BugReport(
            id=str(uuid.uuid4()),
            title=f"Test failure: {test_result.test_name}",
            description=test_result.message,
            severity=severity,
            file_path=test_result.file_path,
            line_number=None,
            steps_to_reproduce=[
                "Run tests",
                f"Check {test_result.test_name}",
                "Observe failure"
            ],
            expected_result="Test should pass",
            actual_result=test_result.message,
            created_at=datetime.now().isoformat()
        )
        
        self.memory.add_bug_report(bug)
        self.communicate("Coder", f"Created bug report: {bug.title}")
        self.log_action("Bug report created", bug.title)
        
        return bug

    def _determine_bug_severity(self, test_result: TestResult) -> str:
        """Determine bug severity based on test result."""
        # Critical: Core functionality missing
        if "file_exists" in test_result.test_name:
            return Severity.CRITICAL.value
        
        # High: Important features missing
        if any(keyword in test_result.test_name.lower() 
               for keyword in ["add", "delete", "toggle"]):
            return Severity.HIGH.value
        
        # Medium: UI/styling issues
        if "css" in test_result.test_name.lower():
            return Severity.MEDIUM.value
        
        # Default to medium
        return Severity.MEDIUM.value

    def run_integration_tests(self) -> List[TestResult]:
        """Run integration tests across multiple components."""
        self.log_action("Running integration tests")
        
        results = []
        
        # Test file dependencies
        required_files = ["index.html", "styles.css", "script.js"]
        all_files_exist = all(f in self.memory.project_files for f in required_files)
        
        if all_files_exist:
            results.append(TestResult(
                "integration_all_files", "pass",
                "All required files exist", "project"
            ))
            
            # Test HTML references to CSS and JS
            html_content = self.memory.project_files.get("index.html", "")
            
            if "styles.css" in html_content:
                results.append(TestResult(
                    "integration_css_link", "pass",
                    "CSS file properly linked", "index.html"
                ))
            else:
                results.append(TestResult(
                    "integration_css_link", "fail",
                    "CSS file not linked", "index.html"
                ))
            
            if "script.js" in html_content:
                results.append(TestResult(
                    "integration_js_link", "pass",
                    "JavaScript file properly linked", "index.html"
                ))
            else:
                results.append(TestResult(
                    "integration_js_link", "fail",
                    "JavaScript file not linked", "index.html"
                ))
        else:
            results.append(TestResult(
                "integration_all_files", "fail",
                "Missing required files", "project"
            ))
        
        self.log_action("Integration tests completed", f"{len(results)} tests run")
        return results

    def generate_test_report(self) -> str:
        """Generate a comprehensive test report."""
        # Get all tasks and run tests
        all_test_results = []
        
        for task in self.memory.tasks.values():
            if task.status == TaskStatus.COMPLETED:
                test_results = self.run_tests(task)
                all_test_results.extend(test_results)
        
        # Add integration tests
        integration_results = self.run_integration_tests()
        all_test_results.extend(integration_results)
        
        # Generate report
        total_tests = len(all_test_results)
        passed_tests = len([t for t in all_test_results if t.is_passing()])
        failed_tests = total_tests - passed_tests
        
        report = f"""
=== QA TEST REPORT ===
Total Tests: {total_tests}
Passed: {passed_tests}
Failed: {failed_tests}
Success Rate: {(passed_tests/total_tests*100):.1f}% if total_tests > 0 else 0%

Failed Tests:
"""
        
        for result in all_test_results:
            if result.is_failing():
                report += f"- {result.test_name}: {result.message}\n"
        
        self.log_action("Test report generated")
        return report