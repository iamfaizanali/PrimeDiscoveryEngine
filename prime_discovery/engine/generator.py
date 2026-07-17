"""Hypothesis generation from data and symbolic expressions.

Generates novel hypotheses through various strategies including random,
evolutionary, and data-driven approaches.
"""

import random
from typing import List, Optional

import numpy as np
import sympy as sp
from sympy import Symbol, symbols

from prime_discovery.engine.hypothesis import Hypothesis, HypothesisStatus


class HypothesisGenerator:
    """Generate mathematical hypotheses."""

    # Basic operations for expression building
    BINARY_OPS = [sp.Add, sp.Mul, sp.Pow]
    UNARY_OPS = [sp.sin, sp.cos, sp.log, sp.exp, sp.sqrt]
    CONSTANTS = [0, 1, 2, 3, 5, 7, 11, 13]  # Include small primes

    def __init__(self, seed: int = 42):
        """Initialize hypothesis generator.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
        self.hypothesis_counter = 0

    def generate_random_expression(
        self, num_vars: int = 1, max_depth: int = 3, max_complexity: int = 20
    ) -> sp.Expr:
        """Generate a random symbolic expression.

        Args:
            num_vars: Number of variables in expression
            max_depth: Maximum expression tree depth
            max_complexity: Maximum expression complexity (node count)

        Returns:
            SymPy expression
        """
        symbols_list = symbols(f"x0:{num_vars}")
        if num_vars == 1:
            symbols_list = [symbols_list]

        def build_expr(depth: int, complexity_budget: int) -> sp.Expr:
            if depth == 0 or complexity_budget <= 1:
                # Base case: variable or constant
                if random.random() < 0.5:
                    return random.choice(symbols_list)
                else:
                    return sp.Integer(random.choice(self.CONSTANTS))

            complexity_budget -= 1
            op_type = random.choice(["binary", "unary", "var", "const"])

            if op_type == "binary" and complexity_budget >= 2:
                op = random.choice(self.BINARY_OPS)
                left = build_expr(depth - 1, complexity_budget // 2)
                right = build_expr(depth - 1, complexity_budget // 2)
                try:
                    return op(left, right)
                except:
                    return left
            elif op_type == "unary" and complexity_budget >= 1:
                op = random.choice(self.UNARY_OPS)
                arg = build_expr(depth - 1, complexity_budget - 1)
                try:
                    return op(arg)
                except:
                    return arg
            else:
                # Fallback to variable or constant
                if random.random() < 0.5:
                    return random.choice(symbols_list)
                else:
                    return sp.Integer(random.choice(self.CONSTANTS))

        return build_expr(max_depth, max_complexity)

    def generate_polynomial(
        self, num_vars: int = 1, max_degree: int = 3, max_coeffs: int = 5
    ) -> sp.Expr:
        """Generate a random polynomial.

        Args:
            num_vars: Number of variables
            max_degree: Maximum degree of polynomial
            max_coeffs: Maximum number of terms

        Returns:
            SymPy polynomial expression
        """
        symbols_list = symbols(f"x0:{num_vars}")
        if num_vars == 1:
            symbols_list = [symbols_list]

        terms = []
        for _ in range(random.randint(1, max_coeffs)):
            coeff = random.randint(1, 10)
            # Random monomial
            monomial = sp.Integer(coeff)
            for symbol in symbols_list:
                degree = random.randint(0, max_degree)
                monomial *= symbol**degree
            terms.append(monomial)

        return sum(terms)

    def generate_rational_function(
        self, num_vars: int = 1, max_degree: int = 2
    ) -> sp.Expr:
        """Generate a random rational function.

        Args:
            num_vars: Number of variables
            max_degree: Maximum degree of numerator and denominator

        Returns:
            SymPy rational function
        """
        numerator = self.generate_polynomial(num_vars, max_degree)
        denominator = self.generate_polynomial(num_vars, max_degree - 1)

        # Ensure non-zero denominator at origin
        if denominator == 0:
            denominator = sp.Integer(1)

        return numerator / denominator

    def generate_from_template(
        self, template: str, num_vars: int = 1
    ) -> Optional[sp.Expr]:
        """Generate hypothesis from template string.

        Args:
            template: Template string with variable placeholders (x0, x1, ...)
            num_vars: Number of variables to substitute

        Returns:
            SymPy expression or None if invalid
        """
        try:
            expr = sp.sympify(template)
            return expr
        except:
            return None

    def create_hypothesis(
        self,
        expr: sp.Expr,
        strategy: str = "random",
        metadata: Optional[dict] = None,
    ) -> Hypothesis:
        """Create a Hypothesis from an expression.

        Args:
            expr: SymPy expression
            strategy: Generation strategy used
            metadata: Additional metadata

        Returns:
            Hypothesis instance
        """
        self.hypothesis_counter += 1
        hyp_id = f"hyp_{strategy}_{self.hypothesis_counter}"

        meta = metadata or {}
        meta["strategy"] = strategy
        meta["generated_at"] = None  # Will be set by hypothesis

        return Hypothesis(
            expression=expr,
            hypothesis_id=hyp_id,
            status=HypothesisStatus.PENDING,
            metadata=meta,
        )

    def generate_batch(
        self,
        num_hypotheses: int,
        strategy: str = "random",
        num_vars: int = 1,
        **kwargs,
    ) -> List[Hypothesis]:
        """Generate a batch of hypotheses.

        Args:
            num_hypotheses: Number of hypotheses to generate
            strategy: Generation strategy ("random", "polynomial", "rational")
            num_vars: Number of variables per hypothesis
            **kwargs: Additional arguments for generation strategy

        Returns:
            List of Hypothesis instances
        """
        hypotheses = []

        for _ in range(num_hypotheses):
            if strategy == "random":
                expr = self.generate_random_expression(num_vars, **kwargs)
            elif strategy == "polynomial":
                expr = self.generate_polynomial(num_vars, **kwargs)
            elif strategy == "rational":
                expr = self.generate_rational_function(num_vars, **kwargs)
            else:
                expr = self.generate_random_expression(num_vars, **kwargs)

            try:
                hypothesis = self.create_hypothesis(expr, strategy)
                hypotheses.append(hypothesis)
            except:
                pass  # Skip invalid expressions

        return hypotheses
