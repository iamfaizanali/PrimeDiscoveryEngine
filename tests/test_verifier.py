"""Tests for verification and validation modules."""

import numpy as np
import pytest
import sympy as sp
from sympy import symbols

from prime_discovery.engine.hypothesis import Hypothesis
from prime_discovery.verifier.checker import HypothesisValidator
from prime_discovery.verifier.metrics import EvaluationMetrics, MetricsCalculator


class TestHypothesisValidator:
    """Test hypothesis validation."""

    def test_evaluate_expression(self):
        """Test expression evaluation."""
        x = symbols("x")
        expr = x**2

        X = np.array([[1], [2], [3], [4]], dtype=float)
        y = np.array([1, 4, 9, 16], dtype=float)
        symbols_list = [x]

        rmse, error = HypothesisValidator.evaluate_expression(expr, X, y, symbols_list)

        assert error == ""
        assert rmse < 0.1

    def test_calculate_r_squared(self):
        """Test R-squared calculation."""
        y_true = np.array([1, 2, 3, 4, 5], dtype=float)
        y_pred = np.array([1, 2, 3, 4, 5], dtype=float)

        r2 = HypothesisValidator.calculate_r_squared(y_true, y_pred)
        assert r2 == pytest.approx(1.0)

    def test_check_mathematical_properties(self):
        """Test mathematical property checking."""
        x = symbols("x")
        expr = x**2 + 2 * x + 1

        props = HypothesisValidator.check_mathematical_properties(expr)

        assert "is_polynomial" in props
        assert "free_symbols" in props
        assert props["is_polynomial"] is True


class TestMetricsCalculator:
    """Test metrics calculation."""

    def test_rmse(self):
        """Test RMSE calculation."""
        y_true = np.array([1, 2, 3, 4])
        y_pred = np.array([1, 2, 3, 4])

        rmse = MetricsCalculator.calculate_rmse(y_true, y_pred)
        assert rmse == pytest.approx(0.0)

    def test_mae(self):
        """Test MAE calculation."""
        y_true = np.array([1, 2, 3, 4])
        y_pred = np.array([2, 3, 4, 5])

        mae = MetricsCalculator.calculate_mae(y_true, y_pred)
        assert mae == pytest.approx(1.0)

    def test_r_squared(self):
        """Test R-squared calculation."""
        y_true = np.array([1, 2, 3, 4, 5], dtype=float)
        y_pred = np.array([1, 2, 3, 4, 5], dtype=float)

        r2 = MetricsCalculator.calculate_r_squared(y_true, y_pred)
        assert r2 == pytest.approx(1.0)

    def test_calculate_all_metrics(self):
        """Test calculating all metrics at once."""
        y_true = np.array([1, 2, 3, 4], dtype=float)
        y_pred = np.array([1.1, 2.1, 2.9, 3.9], dtype=float)

        metrics = MetricsCalculator.calculate_all_metrics(y_true, y_pred)

        assert hasattr(metrics, "rmse")
        assert hasattr(metrics, "mae")
        assert hasattr(metrics, "r_squared")
        assert metrics.rmse > 0
        assert metrics.mae > 0
