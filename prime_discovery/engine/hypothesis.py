"""Core hypothesis representation and management.

Defines the structure of mathematical hypotheses and operations on them.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import sympy as sp
from sympy import Symbol, sympify


class HypothesisStatus(str, Enum):
    """Status of a hypothesis."""

    PENDING = "pending"
    EVALUATING = "evaluating"
    VALIDATED = "validated"
    REJECTED = "rejected"
    FAILED = "failed"


@dataclass
class Hypothesis:
    """Represents a mathematical hypothesis about prime number structure.

    Attributes:
        expression: SymPy symbolic expression
        hypothesis_id: Unique identifier
        status: Current status of hypothesis
        fitness: Numerical fitness score (0-1)
        accuracy: Validation accuracy if tested
        error_message: Error message if failed
        created_at: Creation timestamp
        updated_at: Last update timestamp
        metadata: Additional metadata dictionary
    """

    expression: sp.Expr
    hypothesis_id: str
    status: HypothesisStatus = HypothesisStatus.PENDING
    fitness: float = 0.0
    accuracy: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(cls, expr_str: str, hypothesis_id: str, **metadata) -> "Hypothesis":
        """Create a hypothesis from a string expression.

        Args:
            expr_str: String representation of mathematical expression
            hypothesis_id: Unique identifier
            **metadata: Additional metadata

        Returns:
            Hypothesis instance
        """
        try:
            expr = sympify(expr_str)
            return cls(
                expression=expr,
                hypothesis_id=hypothesis_id,
                metadata=metadata,
            )
        except Exception as e:
            raise ValueError(f"Invalid expression: {expr_str}") from e

    def set_status(self, status: HypothesisStatus, error_msg: Optional[str] = None) -> None:
        """Update hypothesis status.

        Args:
            status: New status
            error_msg: Optional error message
        """
        self.status = status
        self.error_message = error_msg
        self.updated_at = datetime.now()

    def set_fitness(self, fitness: float, accuracy: Optional[float] = None) -> None:
        """Update fitness score.

        Args:
            fitness: Fitness score (0-1)
            accuracy: Validation accuracy if available
        """
        self.fitness = max(0.0, min(1.0, fitness))
        if accuracy is not None:
            self.accuracy = max(0.0, min(1.0, accuracy))
        self.updated_at = datetime.now()

    def get_free_symbols(self) -> set:
        """Get all free symbols in the expression.

        Returns:
            Set of SymPy symbols
        """
        return self.expression.free_symbols

    def substitute(self, subs_dict: Dict[Symbol, Any]) -> sp.Expr:
        """Substitute values into the expression.

        Args:
            subs_dict: Dictionary of symbol to value mappings

        Returns:
            Expression with substitutions applied
        """
        return self.expression.subs(subs_dict)

    def simplify(self) -> "Hypothesis":
        """Create a simplified copy of this hypothesis.

        Returns:
            New Hypothesis with simplified expression
        """
        simplified_expr = sp.simplify(self.expression)
        return Hypothesis(
            expression=simplified_expr,
            hypothesis_id=f"{self.hypothesis_id}_simplified",
            status=self.status,
            fitness=self.fitness,
            accuracy=self.accuracy,
            metadata=self.metadata.copy(),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert hypothesis to dictionary representation.

        Returns:
            Dictionary representation
        """
        return {
            "hypothesis_id": self.hypothesis_id,
            "expression": str(self.expression),
            "status": self.status.value,
            "fitness": self.fitness,
            "accuracy": self.accuracy,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }

    def __str__(self) -> str:
        """String representation."""
        return (
            f"Hypothesis({self.hypothesis_id}, "
            f"expr={str(self.expression)[:50]}, "
            f"fitness={self.fitness:.3f}, "
            f"status={self.status.value})"
        )

    def __repr__(self) -> str:
        """Detailed string representation."""
        return self.__str__()
