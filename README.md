# FixBot – AI Test Auto-Fix Agent

🤖 An intelligent agent that automatically detects and fixes failing tests using AI-powered analysis.

## Overview

FixBot is a Python-based tool that helps developers automatically diagnose and fix failing tests. It analyzes test failures, identifies the root cause, and suggests or applies fixes to get your tests passing again.

## Features

- 🔍 **Automatic Test Analysis**: Runs tests and intelligently parses failure output
- 🧠 **Smart Failure Classification**: Categorizes failures (assertion, import, type errors, etc.)
- 🔧 **AI-Powered Fix Generation**: Generates contextual fixes based on failure analysis
- 🛡️ **Safe Application**: Dry-run mode by default with backup creation
- 📊 **Detailed Reporting**: Clear explanations of what went wrong and how to fix it
- 🔄 **Iterative Fixing**: Multiple attempts to fix stubborn test failures

## Installation

1. Clone the repository:
```bash
git clone https://github.com/umer-2k1/fixbot-test-agent.git
cd fixbot-test-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make FixBot executable:
```bash
chmod +x fixbot.py
```

## Usage

### Basic Usage

Run FixBot in dry-run mode (shows what would be fixed without making changes):
```bash
python fixbot.py
```

### Apply Fixes

Apply fixes automatically:
```bash
python fixbot.py --apply
```

### Fix Specific Test File

```bash
python fixbot.py tests/test_example.py
```

### Advanced Options

```bash
# Use different test command
python fixbot.py --test-cmd pytest

# Limit fix attempts
python fixbot.py --max-attempts 5

# Get help
python fixbot.py --help
```

## How It Works

FixBot follows a systematic approach to fix failing tests:

1. **Test Execution**: Runs your test suite and captures output
2. **Failure Parsing**: Extracts detailed information about each failure
3. **Failure Analysis**: Classifies the type of failure and identifies likely causes
4. **Fix Generation**: Creates targeted fixes based on the failure analysis
5. **Safe Application**: Applies fixes with backups (in apply mode)
6. **Iteration**: Re-runs tests and repeats if needed

## Architecture

FixBot consists of several modular components:

- **TestRunner**: Executes tests and collects failure information
- **FailureAnalyzer**: Analyzes failures to determine root causes
- **FixGenerator**: Creates fix suggestions using AI-powered heuristics
- **CodePatcher**: Safely applies fixes to source files
- **FixBot**: Main orchestrator that coordinates the entire process

## Example

Try FixBot with the included example:

```bash
# See what FixBot would fix
python fixbot.py examples/test_example.py

# Apply the fixes
python fixbot.py examples/test_example.py --apply

# Verify tests pass
pytest examples/test_example.py
```

## Supported Test Frameworks

Currently supports:
- ✅ pytest

Future support planned for:
- unittest
- nose2
- Jest (JavaScript)
- JUnit (Java)

## Limitations

- Works best with well-structured test files
- Complex failures may require manual intervention
- Currently focused on Python tests
- AI suggestions should always be reviewed before production use

## Development

### Running Tests

Run the FixBot test suite:
```bash
pytest tests/
```

### Project Structure

```
fixbot-test-agent/
├── fixbot.py           # Main FixBot agent
├── requirements.txt    # Python dependencies
├── tests/             # Unit tests for FixBot
│   └── test_fixbot.py
├── examples/          # Example test files
│   └── test_example.py
└── README.md          # This file
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - feel free to use this in your projects!

## Future Enhancements

- [ ] Integration with popular CI/CD platforms
- [ ] Support for more test frameworks
- [ ] Machine learning-based fix suggestions
- [ ] Git integration for automatic commits
- [ ] Web UI for interactive fixing
- [ ] Test coverage analysis
- [ ] Performance regression detection

## Author

Created as a demonstration of AI-powered development tools.

---

**Note**: FixBot is a productivity tool designed to assist developers. Always review AI-generated fixes before applying them to production code.