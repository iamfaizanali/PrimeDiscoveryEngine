"""Prime number generation and mathematical utilities.

Provides efficient prime number generation and related mathematical operations.
"""

from typing import List, Set

import numpy as np


def sieve_of_eratosthenes(limit: int) -> np.ndarray:
    """Generate all primes up to limit using Sieve of Eratosthenes.

    Args:
        limit: Upper limit for prime generation

    Returns:
        Array of prime numbers
    """
    if limit < 2:
        return np.array([], dtype=np.int64)

    sieve = np.ones(limit + 1, dtype=bool)
    sieve[0:2] = False

    for i in range(2, int(np.sqrt(limit)) + 1):
        if sieve[i]:
            sieve[i * i :: i] = False

    return np.where(sieve)[0].astype(np.int64)


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    Args:
        n: Number to check

    Returns:
        True if n is prime, False otherwise
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(np.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_factorization(n: int) -> List[int]:
    """Get prime factorization of a number.

    Args:
        n: Number to factorize

    Returns:
        List of prime factors
    """
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def next_prime(n: int) -> int:
    """Find the next prime after n.

    Args:
        n: Starting number

    Returns:
        Next prime number
    """
    candidate = n + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate


def prime_gap(p1: int, p2: int) -> int:
    """Calculate gap between two consecutive primes.

    Args:
        p1: First prime
        p2: Second prime (should be next prime after p1)

    Returns:
        Gap between primes
    """
    return p2 - p1


def euler_totient(n: int) -> int:
    """Calculate Euler's totient function φ(n).

    Args:
        n: Input number

    Returns:
        φ(n) - count of integers ≤ n coprime to n
    """
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result
