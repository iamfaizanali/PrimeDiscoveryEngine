"""Tests for dataset and feature extraction modules."""

import numpy as np
import pytest

from prime_discovery.datasets.features import FeatureExtractor
from prime_discovery.datasets.primes import (
    is_prime,
    next_prime,
    prime_factorization,
    sieve_of_eratosthenes,
)


class TestPrimeGeneration:
    """Test prime number generation."""

    def test_sieve_of_eratosthenes(self):
        """Test sieve generates correct primes."""
        primes = sieve_of_eratosthenes(20)
        expected = np.array([2, 3, 5, 7, 11, 13, 17, 19])
        np.testing.assert_array_equal(primes, expected)

    def test_is_prime(self):
        """Test prime checking."""
        assert is_prime(2)
        assert is_prime(3)
        assert is_prime(5)
        assert is_prime(7)
        assert not is_prime(4)
        assert not is_prime(6)
        assert not is_prime(1)
        assert not is_prime(0)

    def test_prime_factorization(self):
        """Test prime factorization."""
        assert prime_factorization(12) == [2, 2, 3]
        assert prime_factorization(15) == [3, 5]
        assert prime_factorization(17) == [17]

    def test_next_prime(self):
        """Test finding next prime."""
        assert next_prime(2) == 3
        assert next_prime(3) == 5
        assert next_prime(10) == 11


class TestFeatureExtraction:
    """Test feature extraction."""

    def test_extract_prime_features(self):
        """Test feature extraction from primes."""
        primes = np.array([2, 3, 5, 7, 11], dtype=np.int64)
        features, names = FeatureExtractor.extract_prime_features(primes)

        assert features.shape[0] == len(primes)
        assert features.shape[1] > 0
        assert len(names) == features.shape[1]

    def test_extract_statistical_features(self):
        """Test statistical feature extraction."""
        primes = np.array([2, 3, 5, 7, 11, 13], dtype=np.int64)
        stats = FeatureExtractor.extract_statistical_features(primes)

        assert "count" in stats
        assert "mean" in stats
        assert stats["count"] == len(primes)
        assert stats["mean"] > 0
