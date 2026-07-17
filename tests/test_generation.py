"""Tests for hypothesis generation and symbolic expression modules."""

import pytest
import sympy as sp
from sympy import symbols

from prime_discovery.engine.generator import HypothesisGenerator
from prime_discovery.symbolic.expressions import ExpressionTree, SymbolicRegression


class TestHypothesisGenerator:
    """Test hypothesis generation."""

    def test_init(self):
        """Test generator initialization."""
        gen = HypothesisGenerator(seed=42)
        assert gen.seed == 42
        assert gen.hypothesis_counter == 0

    def test_generate_random_expression(self):
        """Test random expression generation."""
        gen = HypothesisGenerator()
        expr = gen.generate_random_expression(num_vars=1, max_depth=2)
        assert isinstance(expr, sp.Expr)

    def test_generate_polynomial(self):
        """Test polynomial generation."""
        gen = HypothesisGenerator()
        expr = gen.generate_polynomial(num_vars=1, max_degree=2)
        assert isinstance(expr, sp.Expr)
        assert expr.is_polynomial()

    def test_generate_rational_function(self):
        """Test rational function generation."""
        gen = HypothesisGenerator()
        expr = gen.generate_rational_function(num_vars=1)
        assert isinstance(expr, sp.Expr)

    def test_generate_from_template(self):
        """Test template-based generation."""
        gen = HypothesisGenerator()
        expr = gen.generate_from_template("x0**2 + 2*x0 + 1")
        assert expr is not None
        assert isinstance(expr, sp.Expr)

    def test_create_hypothesis(self):
        """Test hypothesis creation."""
        gen = HypothesisGenerator()
        x = symbols("x")
        expr = x**2 + 1
        hyp = gen.create_hypothesis(expr, strategy="test")
        assert hyp.hypothesis_id.startswith("hyp_test")
        assert hyp.metadata["strategy"] == "test"

    def test_generate_batch(self):
        """Test batch generation."""
        gen = HypothesisGenerator()
        batch = gen.generate_batch(5, strategy="polynomial")
        assert len(batch) <= 5


class TestExpressionTree:
    """Test expression tree operations."""

    def test_complexity(self):
        """Test complexity calculation."""
        x = symbols("x")
        expr = x**2 + 1
        tree = ExpressionTree(expr)
        assert tree.get_complexity() > 0

    def test_simplify(self):
        """Test simplification."""
        x = symbols("x")
        expr = x**2 - 1
        tree = ExpressionTree(expr)
        simplified = tree.simplify()
        assert simplified.expr is not None

    def test_expand_expr(self):
        """Test expansion."""
        x = symbols("x")
        expr = (x + 1) ** 2
        tree = ExpressionTree(expr)
        expanded = tree.expand_expr()
        assert "x**2" in str(expanded.expr)

    def test_get_free_symbols(self):
        """Test getting free symbols."""
        x, y = symbols("x y")
        expr = x**2 + y
        tree = ExpressionTree(expr)
        symbols_set = tree.get_free_symbols()
        assert len(symbols_set) == 2

    def test_is_polynomial(self):
        """Test polynomial check."""
        x = symbols("x")
        expr = x**2 + 1
        tree = ExpressionTree(expr)
        assert tree.is_polynomial()

    def test_differentiate(self):
        """Test differentiation."""
        x = symbols("x")
        expr = x**2
        tree = ExpressionTree(expr)
        deriv = tree.differentiate(x)
        assert "2*x" in str(deriv.expr)
