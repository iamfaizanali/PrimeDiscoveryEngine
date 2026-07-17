# Contributing Guidelines

Thank you for your interest in contributing to PrimeDiscoveryEngine! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Virtual environment tool (venv, conda, or similar)

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/PrimeDiscoveryEngine.git
   cd PrimeDiscoveryEngine
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Creating a Branch

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b bugfix/your-bug-fix-name
```

Branch naming conventions:
- `feature/` for new features
- `bugfix/` for bug fixes
- `docs/` for documentation updates
- `test/` for test additions

### Making Changes

1. Make your changes
2. Follow the coding standards (see below)
3. Write or update tests as needed
4. Update documentation if applicable

### Code Standards

#### Style Guide

We follow PEP 8 with some modifications:

- Line length: 100 characters (not 79)
- Use type hints for function signatures
- Use docstrings for all public functions and classes

#### Formatting

Use the provided tools to format your code:

```bash
# Format with Black
black prime_discovery/ tests/

# Sort imports with isort
isort prime_discovery/ tests/

# Check code quality
flake8 prime_discovery/ tests/

# Type checking
mypy prime_discovery/
```

#### Documentation

All public functions and classes must have docstrings:

```python
def my_function(param1: str, param2: int) -> bool:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something is wrong
    """
    pass
```

### Testing

Write tests for your changes:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_core.py -v

# Run with coverage
pytest tests/ --cov=prime_discovery --cov-report=html
```

Test coverage should be at least 80% for new code.

### Committing Changes

Write clear, descriptive commit messages:

```bash
git commit -m "Brief description of changes

Optional longer description explaining the why and what of the changes.
Reference any related issues: Fixes #123"
```

Commit message guidelines:
- Use imperative mood ("Add feature" not "Added feature")
- First line should be 50 characters or less
- Reference issues and pull requests liberally after the first line
- Separate subjects from body with a blank line

### Pushing and Creating Pull Requests

1. Push your branch:
   ```bash
   git push origin your-branch-name
   ```

2. Create a Pull Request on GitHub:
   - Use a clear, descriptive title
   - Reference related issues using GitHub's syntax (#issue-number)
   - Fill out the PR template completely
   - Ensure CI/CD checks pass

## Pull Request Process

1. **Update tests**: Add tests for any new functionality
2. **Update documentation**: Update README and docstrings as needed
3. **Update CHANGELOG**: Add entries for significant changes
4. **Ensure CI passes**: All automated checks must pass
5. **Request review**: Ask for review from maintainers
6. **Respond to feedback**: Address review comments promptly
7. **Merge**: Once approved, your PR will be merged

## Reporting Issues

### Bug Reports

When reporting a bug, please include:

1. Python version and OS
2. Exact steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Error traceback (if applicable)
6. Minimal code example

### Feature Requests

When proposing a feature:

1. Use a descriptive title
2. Provide a detailed description
3. Explain the use case and benefits
4. Provide code examples or mockups if applicable
5. Discuss any potential implementation challenges

## Documentation

### Building Documentation Locally

```bash
pip install -e ".[docs]"
cd docs
make html
```

Documentation will be built to `docs/_build/html/`.

### Documentation Style

- Use clear, concise language
- Include code examples
- Link to relevant sections
- Keep examples minimal and focused

## Community

- **Discussions**: Use GitHub Discussions for questions and ideas
- **Issues**: Use GitHub Issues for bugs and feature requests
- **Chat**: Join our community discussions for real-time interaction

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to:
- Open a GitHub discussion
- Check existing documentation
- Ask in a GitHub issue

Thank you for contributing! 🎉
