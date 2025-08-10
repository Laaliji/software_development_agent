#!/usr/bin/env python3
"""Main entry point for the Software Development Agent System."""

from software_dev_agents import SoftwareDevTeam


def main():
    """Demo the software development team."""
    print("🤖 AI Software Development Team Demo")
    print("=" * 50)

    # Create the development team
    dev_team = SoftwareDevTeam()

    # Define project requirements
    requirements = """Create a simple Todo List web application with the following features:
- Add new todo items
- Mark items as completed
- Delete items  
- Show total and completed task counts
- Modern, responsive design
- Pure HTML/CSS/JavaScript (no frameworks)
"""

    # Start development
    dev_team.develop_project(requirements)


if __name__ == "__main__":
    main()