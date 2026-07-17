"""Configuration management for PrimeDiscoveryEngine.

Handles loading and validation of configuration from YAML and environment variables.
"""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatasetConfig(BaseSettings):
    """Configuration for dataset generation and loading."""

    model_config = SettingsConfigDict(env_prefix="DATASET_")

    max_prime: int = Field(default=1000000, description="Maximum prime to generate")
    batch_size: int = Field(default=1024, description="Batch size for processing")
    test_split: float = Field(default=0.2, description="Test data split ratio")
    seed: int = Field(default=42, description="Random seed for reproducibility")


class EngineConfig(BaseSettings):
    """Configuration for the discovery engine."""

    model_config = SettingsConfigDict(env_prefix="ENGINE_")

    max_hypotheses: int = Field(default=1000, description="Maximum hypotheses to maintain")
    hypothesis_timeout: float = Field(default=30.0, description="Timeout per hypothesis in seconds")
    validation_threshold: float = Field(default=0.9, description="Validation accuracy threshold")
    beam_width: int = Field(default=10, description="Beam search width")


class ExperimentConfig(BaseSettings):
    """Configuration for experiment execution."""

    model_config = SettingsConfigDict(env_prefix="EXPERIMENT_")

    max_iterations: int = Field(default=100, description="Maximum iterations per experiment")
    checkpoint_interval: int = Field(default=10, description="Checkpoint every N iterations")
    early_stopping_patience: int = Field(default=20, description="Early stopping patience")
    num_workers: int = Field(default=4, description="Number of worker processes")


class LoggingConfig(BaseSettings):
    """Configuration for logging."""

    model_config = SettingsConfigDict(env_prefix="LOG_")

    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(
        default="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        description="Log message format",
    )
    rotation: str = Field(default="500 MB", description="Log rotation size")
    retention: str = Field(default="7 days", description="Log retention period")


class AppConfig(BaseSettings):
    """Main application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = Field(default="PrimeDiscoveryEngine", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    # Nested configs
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    engine: EngineConfig = Field(default_factory=EngineConfig)
    experiment: ExperimentConfig = Field(default_factory=ExperimentConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    @classmethod
    def from_yaml(cls, path: Path) -> "AppConfig":
        """Load configuration from YAML file.

        Args:
            path: Path to YAML configuration file

        Returns:
            AppConfig instance
        """
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.

        Returns:
            Configuration as dictionary
        """
        return self.model_dump()


def get_config(config_path: Optional[Path] = None) -> AppConfig:
    """Get application configuration.

    Args:
        config_path: Optional path to YAML configuration file

    Returns:
        AppConfig instance
    """
    if config_path and config_path.exists():
        return AppConfig.from_yaml(config_path)
    return AppConfig()


# Singleton instance
_config: Optional[AppConfig] = None


def init_config(config_path: Optional[Path] = None) -> AppConfig:
    """Initialize global configuration.

    Args:
        config_path: Optional path to YAML configuration file

    Returns:
        AppConfig instance
    """
    global _config
    _config = get_config(config_path)
    return _config


def get_app_config() -> AppConfig:
    """Get global application configuration.

    Returns:
        AppConfig instance

    Raises:
        RuntimeError: If configuration not initialized
    """
    if _config is None:
        raise RuntimeError("Configuration not initialized. Call init_config() first.")
    return _config
