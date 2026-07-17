"""Genetic algorithm for hypothesis evolution.

Implements genetic operators for hypothesis evolution and optimization.
"""

import random
from typing import List

import sympy as sp
from sympy import symbols

from prime_discovery.engine.generator import HypothesisGenerator
from prime_discovery.engine.hypothesis import Hypothesis


class GeneticAlgorithm:
    """Genetic algorithm for symbolic regression."""

    def __init__(self, mutation_rate: float = 0.1, crossover_rate: float = 0.8):
        """Initialize GA.

        Args:
            mutation_rate: Probability of mutation
            crossover_rate: Probability of crossover
        """
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generator = HypothesisGenerator()

    def breed(
        self, parents: List[Hypothesis], num_offspring: int
    ) -> List[Hypothesis]:
        """Create offspring from parent hypotheses.

        Args:
            parents: Parent hypotheses
            num_offspring: Number of offspring to create

        Returns:
            List of offspring hypotheses
        """
        offspring = []

        for _ in range(num_offspring):
            if random.random() < self.crossover_rate and len(parents) >= 2:
                # Crossover
                parent1, parent2 = random.sample(parents, 2)
                child_expr = self._crossover(parent1.expression, parent2.expression)
            else:
                # Copy parent
                parent = random.choice(parents)
                child_expr = parent.expression

            try:
                child = self.generator.create_hypothesis(
                    child_expr, strategy="ga_breed"
                )
                offspring.append(child)
            except:
                pass

        return offspring

    def mutate(self, hypothesis: Hypothesis) -> Hypothesis:
        """Mutate a hypothesis.

        Args:
            hypothesis: Hypothesis to mutate

        Returns:
            Mutated hypothesis
        """
        if random.random() < self.mutation_rate:
            mutated_expr = self._mutate_expression(hypothesis.expression)
            try:
                return self.generator.create_hypothesis(
                    mutated_expr, strategy="ga_mutate"
                )
            except:
                return hypothesis
        return hypothesis

    def _crossover(self, expr1: sp.Expr, expr2: sp.Expr) -> sp.Expr:
        """Perform crossover between two expressions.

        Args:
            expr1: First expression
            expr2: Second expression

        Returns:
            Offspring expression
        """
        # Simple strategy: randomly select between expressions
        if random.random() < 0.5:
            return expr1
        else:
            return expr2

    def _mutate_expression(self, expr: sp.Expr) -> sp.Expr:
        """Mutate an expression.

        Args:
            expr: Expression to mutate

        Returns:
            Mutated expression
        """
        mutation_type = random.choice(["add_term", "remove_term", "change_op"])

        try:
            if mutation_type == "add_term":
                # Add random term
                x = symbols("x")
                new_term = random.randint(1, 5) * x ** random.randint(0, 2)
                return expr + new_term
            elif mutation_type == "remove_term":
                # Simplify (remove constant if possible)
                return sp.simplify(expr)
            else:
                # Change operation (rough approximation)
                return expr
        except:
            return expr
