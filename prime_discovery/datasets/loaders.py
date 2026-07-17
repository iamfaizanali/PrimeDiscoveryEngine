"""Dataset management and loading utilities.

Handles creation, loading, and preprocessing of datasets.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

import numpy as np

from prime_discovery.config import DatasetConfig
from prime_discovery.datasets.features import FeatureExtractor
from prime_discovery.datasets.primes import sieve_of_eratosthenes


@dataclass
class Dataset:
    """Container for dataset with train/test split.

    Attributes:
        X_train: Training features
        X_test: Testing features
        y_train: Training labels/targets
        y_test: Testing labels/targets
        feature_names: Names of features
        metadata: Additional metadata
    """

    X_train: np.ndarray
    X_test: np.ndarray
    y_train: Optional[np.ndarray] = None
    y_test: Optional[np.ndarray] = None
    feature_names: Optional[list] = None
    metadata: Optional[dict] = None

    @property
    def train_size(self) -> int:
        """Get training set size."""
        return len(self.X_train)

    @property
    def test_size(self) -> int:
        """Get test set size."""
        return len(self.X_test)

    @property
    def num_features(self) -> int:
        """Get number of features."""
        return self.X_train.shape[1] if len(self.X_train.shape) > 1 else 1


class DatasetManager:
    """Manage dataset creation and loading."""

    def __init__(self, config: Optional[DatasetConfig] = None):
        """Initialize dataset manager.

        Args:
            config: DatasetConfig instance
        """
        self.config = config or DatasetConfig()
        self.feature_extractor = FeatureExtractor()

    def generate_prime_dataset(self) -> Dataset:
        """Generate dataset of primes with extracted features.

        Returns:
            Dataset with prime features and train/test split
        """
        # Generate primes
        primes = sieve_of_eratosthenes(self.config.max_prime)

        # Extract features
        features, feature_names = self.feature_extractor.extract_prime_features(primes)

        # Train/test split
        split_idx = int(len(features) * (1 - self.config.test_split))

        X_train = features[:split_idx]
        X_test = features[split_idx:]

        # Use primes as targets (regression target)
        y_train = primes[:split_idx]
        y_test = primes[split_idx:]

        dataset = Dataset(
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            feature_names=feature_names,
            metadata={
                "max_prime": int(self.config.max_prime),
                "num_primes": len(primes),
                "seed": self.config.seed,
            },
        )

        return dataset

    def save_dataset(self, dataset: Dataset, path: Path) -> None:
        """Save dataset to disk.

        Args:
            dataset: Dataset to save
            path: Path to save directory
        """
        path.mkdir(parents=True, exist_ok=True)

        np.save(path / "X_train.npy", dataset.X_train)
        np.save(path / "X_test.npy", dataset.X_test)

        if dataset.y_train is not None:
            np.save(path / "y_train.npy", dataset.y_train)
        if dataset.y_test is not None:
            np.save(path / "y_test.npy", dataset.y_test)

        # Save metadata
        import json

        metadata = {
            "feature_names": dataset.feature_names,
            "metadata": dataset.metadata,
        }
        with open(path / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

    def load_dataset(self, path: Path) -> Dataset:
        """Load dataset from disk.

        Args:
            path: Path to dataset directory

        Returns:
            Loaded Dataset
        """
        import json

        X_train = np.load(path / "X_train.npy")
        X_test = np.load(path / "X_test.npy")

        y_train = None
        y_test = None
        if (path / "y_train.npy").exists():
            y_train = np.load(path / "y_train.npy")
        if (path / "y_test.npy").exists():
            y_test = np.load(path / "y_test.npy")

        with open(path / "metadata.json") as f:
            metadata_dict = json.load(f)

        return Dataset(
            X_train=X_train,
            X_test=X_test,
            y_train=y_train,
            y_test=y_test,
            feature_names=metadata_dict.get("feature_names"),
            metadata=metadata_dict.get("metadata"),
        )
