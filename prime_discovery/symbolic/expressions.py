"""Symbolic expression manipulation and simplification.

Provides utilities for working with symbolic expressions.
"""

from typing import List, Optional, Set, Tuple

import sympy as sp
from sympy import Symbol, simplify, expand, factor


class ExpressionTree:
    """Represents and manipulates expression trees."""

    def __init__(self, expr: sp.Expr):
        """Initialize expression tree.

        Args:
            expr: SymPy expression
        """
        self.expr = expr

    def get_complexity(self) -> int:
        """Get complexity score of expression.

        Returns:
            Complexity (number of operations)
        """
        return len(str(self.expr))

    def simplify(self, rational: bool = True) -> "ExpressionTree":
        """Simplify expression.

        Args:
            rational: Whether to simplify rational expressions

        Returns:
            New ExpressionTree with simplified expression
        """
        simplified = simplify(self.expr)
        return ExpressionTree(simplified)

    def expand_expr(self) -> "ExpressionTree":
        """Expand polynomial expression.

        Returns:
            New ExpressionTree with expanded expression
        """
        expanded = expand(self.expr)
        return ExpressionTree(expanded)

    def factor_expr(self) -> "ExpressionTree":
        """Factor polynomial expression.

        Returns:
            New ExpressionTree with factored expression
        """
        try:
            factored = factor(self.expr)
            return ExpressionTree(factored)
        except:
            return self

    def get_free_symbols(self) -> Set[Symbol]:
        """Get all free symbols in expression.

        Returns:
            Set of symbols
        """
        return self.expr.free_symbols

    def substitute(self, subs_dict: dict) -> "ExpressionTree":
        """Substitute values into expression.

        Args:
            subs_dict: Dictionary of substitutions

        Returns:
            New ExpressionTree with substitutions
        """
        substituted = self.expr.subs(subs_dict)
        return ExpressionTree(substituted)

    def differentiate(self, symbol: Symbol) -> "ExpressionTree":
        """Differentiate expression with respect to symbol.

        Args:
            symbol: Symbol to differentiate with respect to

        Returns:
            New ExpressionTree with derivative
        """
        derivative = sp.diff(self.expr, symbol)
        return ExpressionTree(derivative)

    def integrate(self, symbol: Symbol) -> Optional["ExpressionTree"]:
        """Integrate expression with respect to symbol.

        Args:
            symbol: Symbol to integrate with respect to

        Returns:
            New ExpressionTree with integral or None if integration fails
        """
        try:
            integral = sp.integrate(self.expr, symbol)
            return ExpressionTree(integral)
        except:
            return None

    def is_polynomial(self) -> bool:
        """Check if expression is a polynomial.

        Returns:
            True if expression is polynomial
        """
        return self.expr.is_polynomial()

    def is_rational(self) -> bool:
        """Check if expression is rational.

        Returns:
            True if expression is rational
        """
        return self.expr.is_rational

    def __str__(self) -> str:
        """String representation."""
        return str(self.expr)

    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"ExpressionTree({self.expr})"


class SymbolicRegression:
    """Utilities for symbolic regression."""

    @staticmethod
    def estimate_fitness(
        expr: sp.Expr, y_true: list, y_pred: list
    ) -> Tuple[float, float]:
        """Estimate fitness based on error and complexity.

        Args:
            expr: Expression being evaluated
            y_true: True values
            y_pred: Predicted values

        Returns:
            Tuple of (error_score, complexity_penalty)
        """
        # Error component
        import numpy as np

        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        mse = np.mean((y_true - y_pred) ** 2)
        error_score = 1.0 / (1.0 + mse)

        # Complexity penalty
        complexity = len(str(expr))
        complexity_penalty = complexity / 1000.0  # Normalize to reasonable range

        return error_score, complexity_penalty

    @staticmethod
    def pareto_frontier(
        hypotheses: list, metrics: list
    ) -> Tuple[list, list]:
        """Find Pareto frontier of hypotheses.

        Args:
            hypotheses: List of hypotheses
            metrics: List of metric tuples (error, complexity)

        Returns:
            Tuple of (frontier_hypotheses, frontier_metrics)
        """
        pareto_front = []
        pareto_metrics = []

        for h, m in zip(hypotheses, metrics):
            is_dominated = False
            for h2, m2 in zip(pareto_front, pareto_metrics):
                if m2[0] >= m[0] and m2[1] <= m[1]:
                    is_dominated = True
                    break
            if not is_dominated:
                pareto_front.append(h)
                pareto_metrics.append(m)

        return pareto_front, pareto_metrics
