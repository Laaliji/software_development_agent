# Software Development Agent System

A collaborative multi-agent system for software development featuring specialized agents for Project Management, Development, and Quality Assurance.

## 🏗️ Architecture

The system follows a modular architecture with clear separation of concerns:

```
software_dev_agents/
├── models/              # Data models and business logic
│   ├── enums.py        # TaskStatus, AgentRole, Priority, Severity
│   ├── task.py         # Task class with methods
│   └── bug_report.py   # BugReport with workflow methods
├── memory/             # Shared state management
│   └── project_memory.py  # Centralized memory system
├── agents/             # Individual agent implementations
│   ├── base_agent.py   # Abstract base class
│   ├── project_manager.py
│   ├── coder_agent.py
│   └── qa_agent.py
├── orchestrator/       # Coordination layer
│   └── dev_team.py     # Main workflow orchestrator
└── utils/              # Shared utilities
    ├── file_utils.py   # File operations
    └── logger.py       # Logging system
```

## 🤖 Agents

### Project Manager Agent
- **Role**: Planning and coordination
- **Capabilities**:
  - Project planning and task creation
  - Task assignment and prioritization
  - Progress tracking and reporting
  - Resource coordination

### Coder Agent
- **Role**: Implementation and development
- **Capabilities**:
  - Code implementation
  - Bug fixing and refactoring
  - Documentation writing
  - Architecture design

### QA Agent
- **Role**: Testing and quality assurance
- **Capabilities**:
  - Unit and integration testing
  - Bug reporting and tracking
  - Code quality analysis
  - Test automation

## 🚀 Features

- **Modular Architecture**: Clean separation of concerns with well-defined interfaces
- **Collaborative Workflow**: Agents communicate and coordinate through shared memory
- **Comprehensive Testing**: Automated testing with detailed reporting
- **Bug Tracking**: Automatic bug detection and reporting system
- **Progress Monitoring**: Real-time project progress tracking
- **File Management**: Organized project file generation and management
- **Logging System**: Comprehensive logging for debugging and monitoring

## 📋 Usage

### Basic Usage

```python
from software_dev_agents import SoftwareDevTeam

# Create the development team
dev_team = SoftwareDevTeam()

# Define project requirements
requirements = """
Create a simple Todo List web application with:
- Add/delete/toggle todo items
- Modern responsive design
- Pure HTML/CSS/JavaScript
"""

# Start development process
dev_team.develop_project(requirements)
```

### Running the Demo

```bash
python main.py
```

This will create a complete todo application with:
- `index.html` - Main application structure
- `styles.css` - Modern CSS styling
- `script.js` - Interactive functionality
- `README.md` - Project documentation
- `project_summary.json` - Development process summary

## 🔄 Development Workflow

1. **Planning Phase**
   - Project Manager analyzes requirements
   - Creates and prioritizes tasks
   - Assigns tasks to appropriate agents

2. **Development Loop**
   - Coder implements assigned tasks
   - QA tests implementations
   - Bug reports created for failures
   - Progress tracked and reported

3. **Quality Assurance**
   - Comprehensive testing of all components
   - Integration testing across files
   - Bug tracking and resolution

4. **Final Report**
   - Project completion summary
   - Test results and statistics
   - Generated files documentation

## 📊 Project Tracking

The system provides comprehensive project tracking:

- **Task Status**: Pending, In Progress, Completed, Failed, Blocked
- **Bug Severity**: Critical, High, Medium, Low
- **Progress Metrics**: Completion percentage, test pass rates
- **Communication Log**: All agent interactions recorded

## 🛠️ Extensibility

The modular design makes it easy to:

- **Add New Agents**: Extend `BaseAgent` class
- **Custom Task Types**: Add new task categories and handlers
- **Enhanced Testing**: Implement additional test types
- **Integration**: Connect with external tools and services

## 📁 Generated Output

The system creates a `generated_project/` directory containing:

- All generated source files
- Project documentation
- Test reports and summaries
- Development process logs

## 🔧 Configuration

### Logging Levels
```python
from software_dev_agents.utils import AgentLogger

logger = AgentLogger(log_level="DEBUG")  # INFO, WARNING, ERROR
```

### Custom Project Directory
```python
from software_dev_agents.utils import save_project_file

save_project_file("index.html", content, project_dir="my_project")
```

## 🤝 Contributing

The system is designed for easy extension:

1. **New Agent Types**: Implement `BaseAgent` interface
2. **Enhanced Models**: Extend existing data models
3. **Additional Utilities**: Add to utils package
4. **Custom Workflows**: Modify orchestrator logic

## 📝 Example Output

When you run the system, it generates a complete web application:

```
generated_project/
├── index.html          # Todo app interface
├── styles.css          # Modern styling
├── script.js           # Interactive functionality
├── README.md           # Project documentation
└── project_summary.json # Development summary
```

## 🎯 Benefits

- **Automated Development**: Reduces manual coding effort
- **Quality Assurance**: Built-in testing and bug tracking
- **Documentation**: Automatic documentation generation
- **Scalability**: Easy to extend with new capabilities
- **Transparency**: Complete audit trail of development process

## 🔮 Future Enhancements

- AI-powered requirement analysis
- Advanced code generation techniques
- Integration with version control systems
- Real-time collaboration features
- Performance optimization analysis
- Security vulnerability scanning

---

*Built with ❤️ by the AI Software Development Team*