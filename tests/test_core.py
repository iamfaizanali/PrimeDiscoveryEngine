"""Tests for core functionality."""

import pytest


class TestImports:
    """Test that core modules can be imported."""

    def test_import_engine(self):
        """Test importing engine module."""
        from prime_discovery import engine

        assert engine is not None

    def test_import_config(self):
        """Test importing config module."""
        from prime_discovery.config import AppConfig, get_config

        assert AppConfig is not None
        assert get_config is not None

    def test_import_logging(self):
        """Test importing logging module."""
        from prime_discovery.logging import LoggerSetup, get_logger

        assert LoggerSetup is not None
        assert get_logger is not None
