"""Command-line interface for PrimeDiscoveryEngine.

Provides CLI commands for interacting with the discovery engine.
"""

import click
from pathlib import Path

from prime_discovery.config import init_config
from prime_discovery.datasets.loaders import DatasetManager
from prime_discovery.engine.discovery import DiscoveryEngine
from prime_discovery.logging import LoggerSetup


@click.group()
def cli():
    """PrimeDiscoveryEngine CLI."""
    pass


@cli.command()
@click.option("--max-prime", default=1000, help="Maximum prime to generate")
@click.option("--iterations", default=50, help="Number of discovery iterations")
@click.option("--population", default=100, help="Population size")
@click.option("--num-vars", default=1, help="Number of variables")
@click.option("--output", default="results.txt", help="Output file path")
def discover(max_prime: int, iterations: int, population: int, num_vars: int, output: str):
    """Run discovery process.

    Args:
        max_prime: Maximum prime for dataset
        iterations: Number of iterations
        population: Population size
        num_vars: Number of variables
        output: Output file path
    """
    # Setup logging
    LoggerSetup.setup(level="INFO")
    logger = LoggerSetup.get_logger()

    logger.info("Starting discovery process")

    try:
        # Generate dataset
        manager = DatasetManager()
        dataset = manager.generate_prime_dataset()

        # Run discovery
        engine = DiscoveryEngine()
        best_hyps, stats = engine.discover(
            dataset,
            num_iterations=iterations,
            population_size=population,
            num_vars=num_vars,
        )

        # Write results
        with open(output, "w") as f:
            f.write("PrimeDiscoveryEngine Results\n")
            f.write("=" * 50 + "\n\n")

            f.write(f"Statistics:\n")
            for key, value in stats.items():
                f.write(f"  {key}: {value}\n")
            f.write("\n")

            f.write(f"Best {len(best_hyps)} Hypotheses:\n")
            f.write("-" * 50 + "\n")
            for i, hyp in enumerate(best_hyps, 1):
                f.write(f"\n{i}. {hyp.hypothesis_id}\n")
                f.write(f"   Expression: {hyp.expression}\n")
                f.write(f"   Fitness: {hyp.fitness:.4f}\n")
                f.write(f"   Status: {hyp.status.value}\n")
                if hyp.accuracy is not None:
                    f.write(f"   Accuracy: {hyp.accuracy:.4f}\n")

        logger.info(f"Results written to {output}")
        click.echo(f"Discovery complete! Results saved to {output}")
    except Exception as e:
        logger.error(f"Discovery failed: {e}")
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.option("--config-path", default=None, help="Path to config file")
def init(config_path: Optional[str]):
    """Initialize configuration.

    Args:
        config_path: Path to configuration file
    """
    path = Path(config_path) if config_path else None
    config = init_config(path)
    click.echo("Configuration initialized")
    click.echo(config.model_dump_json(indent=2))


@cli.command()
@click.option("--max-prime", default=1000, help="Maximum prime to generate")
def generate_data(max_prime: int):
    """Generate and save dataset.

    Args:
        max_prime: Maximum prime for dataset
    """
    LoggerSetup.setup(level="INFO")
    logger = LoggerSetup.get_logger()

    logger.info(f"Generating dataset with max_prime={max_prime}")

    try:
        from prime_discovery.config import DatasetConfig

        config = DatasetConfig(max_prime=max_prime)
        manager = DatasetManager(config)
        dataset = manager.generate_prime_dataset()

        output_dir = Path(f"data_prime_{max_prime}")
        manager.save_dataset(dataset, output_dir)

        click.echo(f"Dataset saved to {output_dir}")
        click.echo(f"Training samples: {dataset.train_size}")
        click.echo(f"Test samples: {dataset.test_size}")
        click.echo(f"Features: {dataset.num_features}")
    except Exception as e:
        logger.error(f"Dataset generation failed: {e}")
        click.echo(f"Error: {e}", err=True)


if __name__ == "__main__":
    cli()
