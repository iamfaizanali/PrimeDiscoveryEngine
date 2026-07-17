"""Project configuration and build settings."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="prime-discovery-engine",
    version="0.1.0",
    author="Faizan Ali Bilagi",
    author_email="faizan@example.com",
    description="Autonomous Mathematical Discovery Platform for Prime Numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iamfaizanali/PrimeDiscoveryEngine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "sympy>=1.12",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "pyyaml>=6.0",
        "loguru>=0.7.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.990",
            "isort>=5.10.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "prime-discovery=prime_discovery.cli.main:cli",
        ],
    },
)
