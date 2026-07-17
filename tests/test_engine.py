"""Tests for discovery engine and genetic algorithm."""

import numpy as np
import pytest
from sympy import symbols

from prime_discovery.config import EngineConfig
from prime_discovery.datasets.loaders import Dataset, DatasetManager
from prime_discovery.engine.discovery import DiscoveryEngine
from prime_discovery.engine.generator import HypothesisGenerator
from prime_discovery.evolution.genetic import GeneticAlgorithm


class TestDiscoveryEngine:
    """Test discovery engine."""

    def test_init(self):
        """Test engine initialization."""
        config = EngineConfig()
        engine = DiscoveryEngine(config)
        assert engine.config == config
        assert engine.hypotheses == {}

    def test_select_elite(self):
        """Test elite selection."""
        engine = DiscoveryEngine()
        gen = HypothesisGenerator()
        x = symbols("x")
        population = [gen.create_hypothesis(x**i) for i in range(1, 6)]
        scores = [0.1, 0.3, 0.5, 0.2, 0.4]
        elite = engine._select_elite(population, scores)
        assert len(elite) > 0
        assert len(elite) <= len(population)

    @pytest.mark.slow
    def test_discover_simple(self):
        """Test basic discovery process."""
        # Create simple dataset
        X_train = np.array([[1], [2], [3], [4]], dtype=float)
        X_test = np.array([[5], [6]], dtype=float)
        y_train = np.array([1, 4, 9, 16], dtype=float)
        y_test = np.array([25, 36], dtype=float)

        dataset = Dataset(
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
        )

        engine = DiscoveryEngine()
        best, stats = engine.discover(
            dataset, num_iterations=5, population_size=20, num_vars=1
        )

        assert len(best) > 0
        assert "best_fitness" in stats


class TestGeneticAlgorithm:
    """Test genetic algorithm."""

    def test_init(self):
        """Test GA initialization."""
        ga = GeneticAlgorithm()
        assert ga.mutation_rate > 0
        assert ga.crossover_rate > 0

    def test_breed(self):
        """Test breeding."""
        ga = GeneticAlgorithm()
        gen = HypothesisGenerator()
        x = symbols("x")
        parents = [gen.create_hypothesis(x**2), gen.create_hypothesis(x + 1)]
        offspring = ga.breed(parents, 5)
        assert len(offspring) <= 5

    def test_mutate(self):
        """Test mutation."""
        ga = GeneticAlgorithm(mutation_rate=1.0)
        gen = HypothesisGenerator()
        x = symbols("x")
        hyp = gen.create_hypothesis(x**2)
        mutated = ga.mutate(hyp)
        assert mutated.hypothesis_id is not None
