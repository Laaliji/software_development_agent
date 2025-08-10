#!/usr/bin/env python3
"""Coder Agent implementation."""

from typing import List

from .base_agent import BaseAgent
from ..models import Task, TaskStatus, AgentRole, BugReport
from ..memory import ProjectMemory


class CoderAgent(BaseAgent):
    """Coder agent responsible for implementing features and fixing bugs."""

    def __init__(self, memory: ProjectMemory):
        super().__init__("Coder", AgentRole.CODER, memory)

    def get_capabilities(self) -> list:
        """Return coder capabilities."""
        return [
            "Code implementation",
            "Bug fixing", 
            "Code refactoring",
            "Documentation writing",
            "Architecture design"
        ]

    def implement_task(self, task: Task) -> bool:
        """Implement the given task."""
        self.log_action("Starting task implementation", task.title)
        
        try:
            # Route to appropriate implementation method
            if "HTML structure" in task.title:
                self._create_html_file()
            elif "CSS styling" in task.title:
                self._create_css_file()
            elif "JavaScript functionality" in task.title:
                self._create_js_file()
            elif "project structure" in task.title:
                self._setup_project_structure()
            else:
                self.log_error(f"Unknown task type: {task.title}")
                return False

            task.mark_completed(f"Implemented {task.title}")
            self.communicate("ProjectManager", f"Completed task: {task.title}")
            self.log_action("Task completed successfully", task.title)
            return True

        except Exception as e:
            task.mark_failed(str(e))
            self.communicate("ProjectManager", f"Failed task {task.title}: {str(e)}")
            self.log_error(f"Task implementation failed: {task.title}", str(e))
            return False

    def _setup_project_structure(self):
        """Create basic project structure."""
        readme_content = """# Todo Application

A simple todo application built by AI agents.

## Files
- index.html - Main HTML structure
- styles.css - CSS styling  
- script.js - JavaScript functionality
- tests.js - Unit tests

## Usage
Open index.html in a web browser.

## Features
- Add new todo items
- Mark items as completed
- Delete items
- Show task statistics
- Responsive design
"""
        self.memory.save_file("README.md", readme_content)
        self.log_action("Project structure created", "README.md generated")

    def _create_html_file(self):
        """Create the main HTML file."""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>My Todo List</h1>
        
        <div class="input-section">
            <input type="text" id="todoInput" placeholder="Add a new task...">
            <button id="addBtn">Add</button>
        </div>
        
        <ul id="todoList"></ul>
        
        <div class="stats">
            <span id="totalTasks">Total: 0</span>
            <span id="completedTasks">Completed: 0</span>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""
        self.memory.save_file("index.html", html_content)
        self.log_action("HTML file created", "index.html with todo structure")

    def _create_css_file(self):
        """Create CSS styling."""
        css_content = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    padding: 20px;
}

.container {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    border-radius: 10px;
    padding: 30px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
}

.input-section {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

#todoInput {
    flex: 1;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

#addBtn {
    padding: 12px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}

#addBtn:hover {
    background-color: #45a049;
}

#todoList {
    list-style: none;
    margin-bottom: 20px;
}

.todo-item {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #eee;
    transition: background-color 0.3s;
}

.todo-item:hover {
    background-color: #f9f9f9;
}

.todo-item.completed {
    opacity: 0.6;
    text-decoration: line-through;
}

.todo-checkbox {
    margin-right: 15px;
}

.todo-text {
    flex: 1;
    font-size: 16px;
}

.delete-btn {
    background-color: #ff4444;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 3px;
    cursor: pointer;
}

.delete-btn:hover {
    background-color: #cc0000;
}

.stats {
    display: flex;
    justify-content: space-between;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 5px;
    font-weight: bold;
}"""
        self.memory.save_file("styles.css", css_content)
        self.log_action("CSS file created", "styles.css with modern styling")

    def _create_js_file(self):
        """Create JavaScript functionality."""
        js_content = """class TodoApp {
    constructor() {
        this.todos = [];
        this.nextId = 1;
        this.init();
    }

    init() {
        this.todoInput = document.getElementById('todoInput');
        this.addBtn = document.getElementById('addBtn');
        this.todoList = document.getElementById('todoList');
        this.totalTasks = document.getElementById('totalTasks');
        this.completedTasks = document.getElementById('completedTasks');

        this.addBtn.addEventListener('click', () => this.addTodo());
        this.todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTodo();
        });

        this.updateStats();
    }

    addTodo() {
        const text = this.todoInput.value.trim();
        if (!text) return;

        const todo = {
            id: this.nextId++,
            text: text,
            completed: false
        };

        this.todos.push(todo);
        this.todoInput.value = '';
        this.renderTodos();
        this.updateStats();
    }

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.renderTodos();
            this.updateStats();
        }
    }

    deleteTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        this.renderTodos();
        this.updateStats();
    }

    renderTodos() {
        this.todoList.innerHTML = '';
        
        this.todos.forEach(todo => {
            const li = document.createElement('li');
            li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
            
            li.innerHTML = `
                <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}>
                <span class="todo-text">${todo.text}</span>
                <button class="delete-btn">Delete</button>
            `;

            const checkbox = li.querySelector('.todo-checkbox');
            const deleteBtn = li.querySelector('.delete-btn');

            checkbox.addEventListener('change', () => this.toggleTodo(todo.id));
            deleteBtn.addEventListener('click', () => this.deleteTodo(todo.id));

            this.todoList.appendChild(li);
        });
    }

    updateStats() {
        const total = this.todos.length;
        const completed = this.todos.filter(t => t.completed).length;
        
        this.totalTasks.textContent = `Total: ${total}`;
        this.completedTasks.textContent = `Completed: ${completed}`;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp();
});"""
        self.memory.save_file("script.js", js_content)
        self.log_action("JavaScript file created", "script.js with todo functionality")

    def fix_bug(self, bug_report: BugReport) -> bool:
        """Fix a reported bug."""
        self.log_action("Starting bug fix", bug_report.title)
        
        try:
            # In a real implementation, this would analyze the bug and apply fixes
            # For demo purposes, we'll simulate a successful fix
            bug_report.mark_fixed(f"Fixed by {self.name}")
            
            self.communicate("QA", f"Fixed bug: {bug_report.title}")
            self.log_action("Bug fixed successfully", bug_report.title)
            return True
            
        except Exception as e:
            self.log_error(f"Bug fix failed: {bug_report.title}", str(e))
            return False

    def refactor_code(self, filename: str, reason: str) -> bool:
        """Refactor existing code for better quality."""
        self.log_action("Starting code refactoring", f"{filename} - {reason}")
        
        # In a real implementation, this would perform actual refactoring
        # For now, just log the action
        self.log_action("Code refactoring completed", filename)
        return True