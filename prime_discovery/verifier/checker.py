"""Hypothesis verification and validation framework.

Provides methods for checking and validating mathematical hypotheses.
"""

from typing import Any, Dict, Tuple

import numpy as np
import sympy as sp
from sympy import Symbol, symbols

from prime_discovery.engine.hypothesis import Hypothesis, HypothesisStatus


class HypothesisValidator:
    """Validate mathematical hypotheses against data."""

    @staticmethod
    def evaluate_expression(
        expr: sp.Expr,
        X: np.ndarray,
        y: np.ndarray,
        symbols_list: list,
        timeout: float = 5.0,
    ) -> Tuple[float, str]:
        """Evaluate hypothesis expression against data.

        Args:
            expr: SymPy expression to evaluate
            X: Feature matrix (n_samples, n_features)
            y: Target values (n_samples,)
            symbols_list: List of symbols in expression matching feature columns
            timeout: Maximum time to spend evaluating

        Returns:
            Tuple of (metric_value, error_message)
        """
        try:
            # Create evaluation function
            expr_func = sp.lambdify(symbols_list, expr, modules="numpy")

            # Evaluate on data
            predictions = expr_func(*[X[:, i] for i in range(X.shape[1])])

            # Handle array vs scalar predictions
            if isinstance(predictions, (int, float)):
                predictions = np.full_like(y, predictions, dtype=float)
            else:
                predictions = np.asarray(predictions, dtype=float)

            # Calculate mean squared error
            mse = np.mean((predictions - y) ** 2)
            rmse = np.sqrt(mse)

            return rmse, ""
        except Exception as e:
            return float("inf"), str(e)

    @staticmethod
    def calculate_r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate R-squared metric.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            R-squared score (0-1)
        """
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        if ss_tot == 0:
            return 0.0
        return 1.0 - (ss_res / ss_tot)

    @staticmethod
    def validate_hypothesis(
        hypothesis: Hypothesis,
        X_test: np.ndarray,
        y_test: np.ndarray,
        symbols_list: list,
    ) -> Dict[str, Any]:
        """Validate a hypothesis and return metrics.

        Args:
            hypothesis: Hypothesis to validate
            X_test: Test feature matrix
            y_test: Test targets
            symbols_list: List of symbols in hypothesis

        Returns:
            Dictionary with validation metrics
        """
        rmse, error_msg = HypothesisValidator.evaluate_expression(
            hypothesis.expression, X_test, y_test, symbols_list
        )

        if error_msg:
            hypothesis.set_status(HypothesisStatus.FAILED, error_msg)
            return {"valid": False, "error": error_msg, "rmse": float("inf")}

        # Evaluate predictions
        try:
            expr_func = sp.lambdify(symbols_list, hypothesis.expression, modules="numpy")
            y_pred = expr_func(*[X_test[:, i] for i in range(X_test.shape[1])])
            if isinstance(y_pred, (int, float)):
                y_pred = np.full_like(y_test, y_pred, dtype=float)
            else:
                y_pred = np.asarray(y_pred, dtype=float)

            r_squared = HypothesisValidator.calculate_r_squared(y_test, y_pred)
            accuracy = max(0.0, min(1.0, r_squared))

            hypothesis.set_status(HypothesisStatus.VALIDATED)
            hypothesis.set_fitness(1.0 - (rmse / (np.max(y_test) + 1e-8)), accuracy)

            return {
                "valid": True,
                "rmse": rmse,
                "r_squared": r_squared,
                "accuracy": accuracy,
            }
        except Exception as e:
            hypothesis.set_status(HypothesisStatus.FAILED, str(e))
            return {"valid": False, "error": str(e), "rmse": float("inf")}

    @staticmethod
    def check_mathematical_properties(expr: sp.Expr) -> Dict[str, Any]:
        """Check mathematical properties of expression.

        Args:
            expr: SymPy expression

        Returns:
            Dictionary of properties
        """
        return {
            "is_polynomial": expr.is_polynomial(),
            "is_rational": expr.is_rational,
            "is_algebraic": expr.is_algebraic,
            "is_transcendental": expr.is_transcendental,
            "free_symbols": list(expr.free_symbols),
            "complexity": len(str(expr)),
        }
