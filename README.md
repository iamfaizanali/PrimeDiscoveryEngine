# PrimeDiscoveryEngine

**An Autonomous Mathematical Discovery Platform for Prime Numbers**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

PrimeDiscoveryEngine is a sophisticated AI research platform designed to autonomously discover hidden mathematical structure, with an initial focus on prime number theory. The system combines symbolic regression, genetic algorithms, and machine learning to explore and validate novel mathematical hypotheses.

## Features

- **Autonomous Hypothesis Generation**: Generates symbolic mathematical expressions using multiple strategies (random, polynomial, rational functions)
- **Genetic Algorithms**: Evolves hypotheses through crossover, mutation, and selection mechanisms
- **Symbolic Verification**: Validates hypotheses using symbolic computation and statistical analysis
- **Prime Number Analytics**: Specialized tools for prime number generation and feature extraction
- **REST API**: FastAPI-based API for remote access and experimentation
- **CLI Tools**: Command-line interface for running experiments and managing datasets
- **Comprehensive Logging**: Structured logging using loguru for debugging and monitoring

## Quick Start

### Installation

```bash
git clone https://github.com/iamfaizanali/PrimeDiscoveryEngine.git
cd PrimeDiscoveryEngine
pip install -e .
```

### Basic Usage

#### Command Line

```bash
# Run discovery process
prime-discovery discover --iterations 50 --population 100 --output results.txt

# Generate dataset
prime-discovery generate-data --max-prime 10000
```

#### Python API

```python
from prime_discovery.datasets.loaders import DatasetManager
from prime_discovery.engine.discovery import DiscoveryEngine

# Generate dataset
manager = DatasetManager()
dataset = manager.generate_prime_dataset()

# Run discovery
engine = DiscoveryEngine()
best_hypotheses, stats = engine.discover(
    dataset,
    num_iterations=50,
    population_size=100,
    num_vars=1
)

# Print results
for hyp in best_hypotheses:
    print(f"Expression: {hyp.expression}")
    print(f"Fitness: {hyp.fitness:.4f}")
```

#### REST API

```bash
# Start API server
python -m prime_discovery.api.main

# Health check
curl http://localhost:8000/health

# Get best hypotheses
curl http://localhost:8000/hypotheses?top_k=10

# Start discovery
curl -X POST http://localhost:8000/discover \
  -H "Content-Type: application/json" \
  -d '{"num_iterations": 50, "population_size": 100}'
```

## Project Structure

```
prime_discovery/
├── config.py              # Configuration management
├── logging.py             # Logging utilities
├── api/                   # FastAPI REST endpoints
├── cli/                   # Command-line interface
├── datasets/              # Data generation and loading
│   ├── primes.py         # Prime number utilities
│   ├── features.py       # Feature extraction
│   └── loaders.py        # Dataset management
├── engine/                # Core discovery engine
│   ├── hypothesis.py     # Hypothesis representation
│   ├── generator.py      # Hypothesis generation
│   └── discovery.py      # Main discovery orchestration
├── evolution/             # Evolutionary algorithms
│   └── genetic.py        # Genetic algorithm implementation
├── symbolic/              # Symbolic mathematics
│   └── expressions.py    # Expression manipulation
└── verifier/              # Validation framework
    ├── checker.py        # Hypothesis validation
    └── metrics.py        # Evaluation metrics
```

## Configuration

Configuration can be set via environment variables or YAML files:

```yaml
# config.yaml
app_name: "PrimeDiscoveryEngine"
debug: false

dataset:
  max_prime: 1000000
  batch_size: 1024
  test_split: 0.2
  seed: 42

engine:
  max_hypotheses: 1000
  hypothesis_timeout: 30.0
  validation_threshold: 0.9
  beam_width: 10

experiment:
  max_iterations: 100
  checkpoint_interval: 10
  early_stopping_patience: 20
  num_workers: 4

logging:
  level: INFO
  rotation: "500 MB"
  retention: "7 days"
```

## Development

### Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=prime_discovery --cov-report=html
```

### Code Quality

```bash
# Format code
black prime_discovery/ tests/

# Lint
flake8 prime_discovery/ tests/

# Type checking
mypy prime_discovery/

# Sort imports
isort prime_discovery/ tests/
```

## Architecture

### Discovery Process

1. **Initialization**: Generate initial population of random mathematical expressions
2. **Evaluation**: Test each hypothesis against dataset and compute fitness scores
3. **Selection**: Select elite hypotheses based on performance
4. **Evolution**: Apply genetic operators (crossover, mutation)
5. **Validation**: Validate best hypotheses using statistical tests
6. **Iteration**: Repeat until convergence or max iterations reached

### Key Components

- **HypothesisGenerator**: Creates symbolic expressions using multiple strategies
- **GeneticAlgorithm**: Evolves expressions through mutation and crossover
- **HypothesisValidator**: Tests expressions against data and validates results
- **DiscoveryEngine**: Orchestrates the overall discovery process
- **DatasetManager**: Generates and manages datasets of prime numbers

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- SymPy: https://www.sympy.org/
- Genetic Algorithms: https://en.wikipedia.org/wiki/Genetic_algorithm
- Symbolic Regression: https://en.wikipedia.org/wiki/Symbolic_regression
- Prime Number Theory: https://en.wikipedia.org/wiki/Prime_number

## Author

**Faizan Ali Bilagi** - [GitHub](https://github.com/iamfaizanali)

## Acknowledgments

- Inspired by research in automated machine learning and symbolic reasoning
- Thanks to the open-source community for excellent libraries like SymPy, NumPy, and scikit-learn
