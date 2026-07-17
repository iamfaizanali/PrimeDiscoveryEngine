# PrimeDiscoveryEngine

**An Autonomous Mathematical Discovery Engine for exploring hidden structure in prime numbers**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linter-ruff-orange.svg)](https://docs.astral.sh/ruff/)

## Vision

PrimeDiscoveryEngine is **not another prime number generator**. It's an AI research platform designed to autonomously discover hidden mathematical structure and generate novel hypotheses about prime numbers and other mathematical phenomena.

The engine is built to:

- **Generate hypotheses** from mathematical data
- **Discover hidden structure** in numerical sequences
- **Invent symbolic equations** through symbolic regression
- **Evolve hypotheses** through iterative refinement
- **Reject weak ideas** through rigorous validation
- **Validate strong ideas** with mathematical verification
- **Discover latent representations** of prime numbers

## Research Targets

### Phase 1 (Current)
- Prime number structure and properties
- Feature extraction and representation learning
- Hypothesis generation framework

### Phase 2+
- Goldbach's conjecture
- Twin prime conjecture
- Collatz conjecture
- Riemann hypothesis related experiments
- Integer sequences and patterns
- Graph theory applications
- General mathematical discovery framework

## Architecture

```
PrimeDiscoveryEngine/
├── docs/                    # Documentation and research notes
├── engine/                  # Core discovery engine
│   ├── hypothesis.py       # Hypothesis representation
│   ├── generator.py        # Hypothesis generation
│   └── validator.py        # Hypothesis validation
├── agents/                 # AI agents for discovery
│   ├── explorer.py         # Exploration strategies
│   ├── reasoner.py         # Symbolic reasoning
│   └── evaluator.py        # Performance evaluation
├── symbolic/               # Symbolic mathematics
│   ├── expressions.py      # Symbolic expression trees
│   ├── regression.py       # Symbolic regression integration
│   └── simplifier.py       # Expression simplification
├── evolution/              # Evolutionary algorithms
│   ├── population.py       # Population management
│   ├── operators.py        # Genetic operators
│   └── selection.py        # Selection mechanisms
├── datasets/               # Dataset management
│   ├── generators.py       # Data generation
│   ├── loaders.py          # Data loading
│   └── preprocessors.py    # Data preprocessing
├── experiments/            # Experiment runners
│   ├── runner.py           # Experiment execution
│   ├── tracker.py          # Results tracking
│   └── reporter.py         # Report generation
├── verifier/               # Mathematical verification
│   ├── checker.py          # Hypothesis checking
│   ├── prover.py           # Formal verification
│   └── stats.py            # Statistical validation
├── dashboard/              # React + TypeScript frontend
├── api/                    # FastAPI REST API
├── cli/                    # Command-line interface
├── configs/                # Configuration files
├── notebooks/              # Jupyter notebooks for exploration
├── tests/                  # Comprehensive test suite
├── scripts/                # Utility scripts
├── pyproject.toml          # Poetry configuration
├── .pre-commit-config.yaml # Pre-commit hooks
└── .github/
    └── workflows/          # GitHub Actions CI/CD
```

## Tech Stack

- **Core ML/AI**: PyTorch, JAX, SymPy
- **Symbolic Regression**: PySR integration
- **Scientific Computing**: NumPy, SciPy
- **Data Processing**: Polars, DuckDB
- **Distributed Computing**: Ray
- **API**: FastAPI, Uvicorn
- **Frontend**: React, TypeScript
- **DevOps**: Docker, GitHub Actions
- **Testing**: pytest
- **Code Quality**: Black, Ruff, MyPy, pre-commit

## Installation

### Prerequisites
- Python 3.12+
- Poetry 1.7+

### Setup

```bash
# Clone the repository
git clone https://github.com/iamfaizanali/PrimeDiscoveryEngine.git
cd PrimeDiscoveryEngine

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell

# Install pre-commit hooks
pre-commit install
```

## Quick Start

```bash
# Run tests
pytest

# Run with verbose output
pytest -v

# Run specific test module
pytest tests/test_core.py

# Generate coverage report
pytest --cov=prime_discovery tests/

# Run the CLI
python -m prime_discovery --help

# Start the API server
python -m prime_discovery.api.server

# Run experiments
python -m prime_discovery.experiments.runner --config configs/experiment.yaml
```

## Project Structure Explanation

### `engine/`
Core discovery engine responsible for hypothesis generation, validation, and management. This is the heart of the autonomous discovery process.

### `agents/`
AI agents implementing different discovery strategies: explorers (search space traversal), reasoners (symbolic manipulation), and evaluators (performance assessment).

### `symbolic/`
Symbolic mathematics module handling expression representation, symbolic regression integration, and mathematical simplification.

### `evolution/`
Evolutionary algorithms for hypothesis population management, genetic operations, and natural selection of mathematical expressions.

### `datasets/`
Dataset management including prime number generation, feature extraction, data loading, and preprocessing pipelines.

### `experiments/`
Experiment infrastructure for running discovery tasks, tracking results, and generating reports. This enables reproducible research.

### `verifier/`
Mathematical verification module for rigorous validation of hypotheses, formal proof checking, and statistical analysis.

### `api/`
FastAPI-based REST API for remote interaction with the discovery engine, enabling integration with the dashboard and external systems.

### `cli/`
Command-line interface for local interaction with the engine, making it accessible for researchers and developers.

### `configs/`
YAML configuration files for experiments, data generation, and system settings. Enables reproducible configurations.

### `notebooks/`
Jupyter notebooks for interactive exploration, visualization, and hypothesis testing during research.

## Development

### Code Style

This project uses:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking
- **Pre-commit** hooks for automated checks

Code is automatically checked via pre-commit hooks before each commit.

```bash
# Manual code formatting
black prime_discovery tests

# Manual linting
ruff check prime_discovery tests

# Manual type checking
mypy prime_discovery
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=prime_discovery

# Run specific markers
pytest -m "unit"
pytest -m "integration"
pytest -m "not slow"
```

Test markers:
- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Long-running tests

## Configuration

Configuration is managed through YAML files in `configs/`:

- `experiment.yaml` - Experiment parameters
- `dataset.yaml` - Data generation settings
- `discovery.yaml` - Discovery engine settings
- `evaluation.yaml` - Evaluation criteria

Environment variables can override YAML settings via `.env` files.

## Documentation

Full documentation is available in `docs/`:

- `ARCHITECTURE.md` - Detailed system architecture
- `API.md` - API reference
- `CONTRIBUTING.md` - Contribution guidelines
- `RESEARCH.md` - Research methodology

Build docs locally:

```bash
cd docs
sphinx-build -b html . _build
```

## Contributing

Contributions are welcome! Please read `docs/CONTRIBUTING.md` first.

## License

MIT License - see LICENSE file for details

## Citation

If you use PrimeDiscoveryEngine in your research, please cite:

```bibtex
@software{primediscoveryengine2024,
  author = {Faizan Ali},
  title = {PrimeDiscoveryEngine: Autonomous Mathematical Discovery},
  year = {2024},
  url = {https://github.com/iamfaizanali/PrimeDiscoveryEngine}
}
```

## Roadmap

- [x] Project foundation and architecture
- [x] Dependency management (Poetry)
- [ ] Core engine implementation
- [ ] Dataset generation and management
- [ ] Feature extraction pipeline
- [ ] Hypothesis generation framework
- [ ] Evaluation and validation system
- [ ] Symbolic regression integration
- [ ] Evolutionary algorithms
- [ ] REST API
- [ ] CLI tools
- [ ] Web dashboard
- [ ] Experiment tracking
- [ ] Research papers and publications

## Contact

For questions, suggestions, or collaboration opportunities, please open an issue or contact the maintainer.

---

**Status**: Early Development (Alpha)  
**Last Updated**: 2024  
**Maintainer**: [@iamfaizanali](https://github.com/iamfaizanali)
