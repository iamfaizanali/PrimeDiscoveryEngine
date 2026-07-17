"""Feature extraction for mathematical sequences and primes.

Provides various feature extraction methods for representing numbers and sequences.
"""

from typing import Dict, List, Optional

import numpy as np
from prime_discovery.datasets.primes import (
    euler_totient,
    prime_factorization,
    prime_gap,
)


class FeatureExtractor:
    """Extract features from prime numbers and sequences."""

    @staticmethod
    def extract_prime_features(primes: np.ndarray) -> np.ndarray:
        """Extract mathematical features from a sequence of primes.

        Features include:
        - Index (position in prime sequence)
        - Value (the prime itself)
        - Gap to next prime
        - Gap to previous prime
        - Digit sum
        - Digit count
        - Prime signature (encoding of prime factors)

        Args:
            primes: Array of prime numbers

        Returns:
            Array of shape (len(primes), num_features) with extracted features
        """
        n = len(primes)
        features = []

        for i, p in enumerate(primes):
            feature_dict = {
                "index": i,
                "value": p,
                "log_value": np.log(p + 1),
                "digit_sum": sum(int(d) for d in str(p)),
                "digit_count": len(str(p)),
                "euler_totient": euler_totient(p),
                "bit_length": p.bit_length(),
                "binary_weight": bin(p).count("1"),
            }

            # Gap to next prime
            if i < n - 1:
                feature_dict["gap_next"] = primes[i + 1] - p
            else:
                feature_dict["gap_next"] = 0

            # Gap to previous prime
            if i > 0:
                feature_dict["gap_prev"] = p - primes[i - 1]
            else:
                feature_dict["gap_prev"] = 0

            features.append(feature_dict)

        # Convert to numpy array
        feature_names = list(features[0].keys())
        feature_array = np.array([list(f.values()) for f in features], dtype=np.float32)

        return feature_array, feature_names

    @staticmethod
    def extract_statistical_features(primes: np.ndarray) -> Dict[str, float]:
        """Extract statistical features from prime sequence.

        Args:
            primes: Array of prime numbers

        Returns:
            Dictionary of statistical features
        """
        if len(primes) == 0:
            return {}

        gaps = np.diff(primes)

        return {
            "count": len(primes),
            "min": float(primes.min()),
            "max": float(primes.max()),
            "mean": float(primes.mean()),
            "median": float(np.median(primes)),
            "std": float(primes.std()),
            "variance": float(primes.var()),
            "gap_mean": float(gaps.mean()),
            "gap_std": float(gaps.std()),
            "gap_min": float(gaps.min()),
            "gap_max": float(gaps.max()),
        }

    @staticmethod
    def extract_distribution_features(
        primes: np.ndarray, bins: int = 100
    ) -> Dict[str, np.ndarray]:
        """Extract distribution features (histogram-based).

        Args:
            primes: Array of prime numbers
            bins: Number of bins for histogram

        Returns:
            Dictionary with distribution features
        """
        hist, bin_edges = np.histogram(primes, bins=bins)
        hist = hist / hist.sum()  # Normalize to probability distribution

        return {
            "histogram": hist,
            "bin_edges": bin_edges,
            "entropy": -np.sum(hist[hist > 0] * np.log2(hist[hist > 0] + 1e-10)),
        }
