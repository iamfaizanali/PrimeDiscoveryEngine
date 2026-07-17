"""Evaluation metrics and performance tracking.

Provides metrics for evaluating hypothesis quality and discovery process.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np


@dataclass
class EvaluationMetrics:
    """Container for evaluation metrics.

    Attributes:
        rmse: Root Mean Squared Error
        mae: Mean Absolute Error
        r_squared: R-squared coefficient
        accuracy: Overall accuracy
        precision: Precision metric
        recall: Recall metric
        f1_score: F1 score
        mape: Mean Absolute Percentage Error
    """

    rmse: float = 0.0
    mae: float = 0.0
    r_squared: float = 0.0
    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    mape: float = 0.0
    custom: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, float]:
        """Convert metrics to dictionary.

        Returns:
            Dictionary of metric values
        """
        return {
            "rmse": self.rmse,
            "mae": self.mae,
            "r_squared": self.r_squared,
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "mape": self.mape,
            **self.custom,
        }


class MetricsCalculator:
    """Calculate evaluation metrics."""

    @staticmethod
    def calculate_rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Root Mean Squared Error.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            RMSE
        """
        return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))

    @staticmethod
    def calculate_mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Mean Absolute Error.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            MAE
        """
        return float(np.mean(np.abs(y_true - y_pred)))

    @staticmethod
    def calculate_r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate R-squared.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            R-squared (0-1)
        """
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        if ss_tot == 0:
            return 0.0
        return float(1.0 - (ss_res / ss_tot))

    @staticmethod
    def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate Mean Absolute Percentage Error.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            MAPE (as percentage)
        """
        mask = y_true != 0
        if not np.any(mask):
            return 0.0
        return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)

    @staticmethod
    def calculate_all_metrics(
        y_true: np.ndarray, y_pred: np.ndarray
    ) -> "EvaluationMetrics":
        """Calculate all standard metrics.

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            EvaluationMetrics instance
        """
        # Ensure valid predictions
        y_pred = np.nan_to_num(y_pred, nan=0.0, posinf=0.0, neginf=0.0)

        rmse = MetricsCalculator.calculate_rmse(y_true, y_pred)
        mae = MetricsCalculator.calculate_mae(y_true, y_pred)
        r_squared = MetricsCalculator.calculate_r_squared(y_true, y_pred)
        mape = MetricsCalculator.calculate_mape(y_true, y_pred)

        # Clip R-squared to [0, 1]
        accuracy = max(0.0, min(1.0, r_squared))

        return EvaluationMetrics(
            rmse=rmse,
            mae=mae,
            r_squared=r_squared,
            accuracy=accuracy,
            mape=mape,
        )


class PerformanceTracker:
    """Track performance metrics over time."""

    def __init__(self):
        """Initialize performance tracker."""
        self.history: List[Dict] = []

    def record_metrics(
        self,
        iteration: int,
        metrics: EvaluationMetrics,
        hypothesis_id: Optional[str] = None,
    ) -> None:
        """Record metrics for an iteration.

        Args:
            iteration: Iteration number
            metrics: EvaluationMetrics instance
            hypothesis_id: Optional hypothesis identifier
        """
        record = {
            "iteration": iteration,
            "hypothesis_id": hypothesis_id,
            **metrics.to_dict(),
        }
        self.history.append(record)

    def get_best_metrics(self, metric_name: str = "accuracy") -> Optional[Dict]:
        """Get best recorded metrics by given metric.

        Args:
            metric_name: Name of metric to optimize

        Returns:
            Best record or None if empty
        """
        if not self.history:
            return None
        return max(self.history, key=lambda x: x.get(metric_name, 0.0))

    def get_average_metrics(self) -> EvaluationMetrics:
        """Get average metrics across all records.

        Returns:
            EvaluationMetrics with average values
        """
        if not self.history:
            return EvaluationMetrics()

        avg_dict = {}
        for key in self.history[0].keys():
            if key not in ["iteration", "hypothesis_id"]:
                values = [r.get(key, 0.0) for r in self.history]
                avg_dict[key] = float(np.mean(values))

        return EvaluationMetrics(**avg_dict)

    def get_history(self) -> List[Dict]:
        """Get complete history.

        Returns:
            List of all recorded metrics
        """
        return self.history.copy()
