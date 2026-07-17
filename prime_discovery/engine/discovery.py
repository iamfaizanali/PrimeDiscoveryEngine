"""Core discovery engine orchestrating the hypothesis discovery process.

Manages hypothesis generation, validation, and evolution.
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
from prime_discovery.config import EngineConfig
from prime_discovery.datasets.loaders import Dataset
from prime_discovery.engine.generator import HypothesisGenerator
from prime_discovery.engine.hypothesis import Hypothesis, HypothesisStatus
from prime_discovery.evolution.genetic import GeneticAlgorithm
from prime_discovery.logging import get_logger
from prime_discovery.verifier.checker import HypothesisValidator
from prime_discovery.verifier.metrics import MetricsCalculator, PerformanceTracker

logger = get_logger(__name__)


class DiscoveryEngine:
    """Main engine for mathematical hypothesis discovery."""

    def __init__(self, config: Optional[EngineConfig] = None):
        """Initialize discovery engine.

        Args:
            config: EngineConfig instance
        """
        self.config = config or EngineConfig()
        self.generator = HypothesisGenerator()
        self.validator = HypothesisValidator()
        self.ga = GeneticAlgorithm()
        self.performance_tracker = PerformanceTracker()

        self.hypotheses: Dict[str, Hypothesis] = {}
        self.best_hypotheses: List[Hypothesis] = []

    def discover(
        self,
        dataset: Dataset,
        num_iterations: int = 50,
        population_size: int = 100,
        num_vars: int = 1,
    ) -> Tuple[List[Hypothesis], Dict]:
        """Run discovery process.

        Args:
            dataset: Dataset with train/test split
            num_iterations: Number of discovery iterations
            population_size: Population size for genetic algorithm
            num_vars: Number of variables in expressions

        Returns:
            Tuple of (best_hypotheses, discovery_stats)
        """
        logger.info(
            f"Starting discovery with {population_size} population "
            f"over {num_iterations} iterations"
        )

        # Initial hypothesis generation
        logger.debug("Generating initial population")
        population = self.generator.generate_batch(
            population_size, strategy="random", num_vars=num_vars
        )

        self.hypotheses = {h.hypothesis_id: h for h in population}

        # Main discovery loop
        for iteration in range(num_iterations):
            logger.debug(f"Iteration {iteration + 1}/{num_iterations}")

            # Evaluate population
            scores = self._evaluate_population(
                population, dataset.X_test, dataset.y_test, num_vars
            )

            # Select best candidates
            elite = self._select_elite(population, scores)

            # Genetic operations
            offspring = self.ga.breed(elite, population_size - len(elite))

            # Mutation
            mutated = [self.ga.mutate(h) for h in offspring]

            # Update population
            population = elite + mutated

            # Track performance
            best_score = max(scores) if scores else 0.0
            self.performance_tracker.record_metrics(
                iteration, MetricsCalculator.calculate_all_metrics(
                    dataset.y_test, np.ones_like(dataset.y_test) * best_score
                )
            )

            logger.debug(f"Best fitness: {best_score:.4f}")

        # Extract best hypotheses
        self.best_hypotheses = sorted(
            population, key=lambda h: h.fitness, reverse=True
        )[: self.config.beam_width]

        stats = {
            "num_iterations": num_iterations,
            "population_size": population_size,
            "best_fitness": self.best_hypotheses[0].fitness if self.best_hypotheses else 0.0,
            "num_best_hypotheses": len(self.best_hypotheses),
        }

        logger.info(f"Discovery complete. Best fitness: {stats['best_fitness']:.4f}")
        return self.best_hypotheses, stats

    def _evaluate_population(
        self,
        population: List[Hypothesis],
        X_test: np.ndarray,
        y_test: np.ndarray,
        num_vars: int,
    ) -> List[float]:
        """Evaluate fitness of population.

        Args:
            population: List of hypotheses
            X_test: Test features
            y_test: Test targets
            num_vars: Number of variables

        Returns:
            List of fitness scores
        """
        scores = []
        for hypothesis in population:
            try:
                from sympy import symbols

                symbols_list = symbols(f"x0:{num_vars}")
                if num_vars == 1:
                    symbols_list = [symbols_list]

                result = self.validator.validate_hypothesis(
                    hypothesis, X_test, y_test, symbols_list
                )

                if result["valid"]:
                    scores.append(hypothesis.fitness)
                else:
                    hypothesis.set_status(HypothesisStatus.FAILED, result.get("error"))
                    scores.append(0.0)
            except Exception as e:
                logger.warning(f"Error evaluating hypothesis {hypothesis.hypothesis_id}: {e}")
                hypothesis.set_status(HypothesisStatus.FAILED, str(e))
                scores.append(0.0)

        return scores

    def _select_elite(
        self, population: List[Hypothesis], scores: List[float]
    ) -> List[Hypothesis]:
        """Select elite hypotheses.

        Args:
            population: List of hypotheses
            scores: Fitness scores

        Returns:
            Elite hypotheses
        """
        elite_size = max(1, len(population) // 10)  # Top 10%
        sorted_pop = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)
        return [h for h, _ in sorted_pop[:elite_size]]

    def get_best_hypotheses(self, top_k: int = 10) -> List[Hypothesis]:
        """Get best hypotheses discovered.

        Args:
            top_k: Number of top hypotheses to return

        Returns:
            List of best hypotheses
        """
        return self.best_hypotheses[:top_k]

    def get_performance_history(self) -> Dict:
        """Get performance tracking history.

        Returns:
            Performance history
        """
        return {"history": self.performance_tracker.get_history()}
