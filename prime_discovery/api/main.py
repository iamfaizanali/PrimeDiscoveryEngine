"""REST API for PrimeDiscoveryEngine.

Provides FastAPI endpoints for accessing the discovery engine.
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from prime_discovery.engine.discovery import DiscoveryEngine
from prime_discovery.engine.hypothesis import Hypothesis
from prime_discovery.logging import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="PrimeDiscoveryEngine API",
    description="API for autonomous mathematical discovery",
    version="0.1.0",
)

# Global engine instance
engine = DiscoveryEngine()


class HypothesisResponse(BaseModel):
    """Response model for hypothesis."""

    hypothesis_id: str
    expression: str
    status: str
    fitness: float
    accuracy: Optional[float] = None
    created_at: str
    updated_at: str

    class Config:
        """Pydantic config."""

        from_attributes = True


class DiscoveryRequest(BaseModel):
    """Request model for discovery."""

    num_iterations: int = 50
    population_size: int = 100
    num_vars: int = 1
    max_prime: int = 1000


class DiscoveryResponse(BaseModel):
    """Response model for discovery results."""

    best_hypotheses: List[HypothesisResponse]
    stats: dict


@app.get("/health")
async def health() -> dict:
    """Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "healthy", "engine": "ready"}


@app.get("/hypotheses", response_model=List[HypothesisResponse])
async def get_hypotheses(top_k: int = 10) -> List[HypothesisResponse]:
    """Get best hypotheses.

    Args:
        top_k: Number of top hypotheses

    Returns:
        List of best hypotheses
    """
    best = engine.get_best_hypotheses(top_k)
    return [
        HypothesisResponse(
            hypothesis_id=h.hypothesis_id,
            expression=str(h.expression),
            status=h.status.value,
            fitness=h.fitness,
            accuracy=h.accuracy,
            created_at=h.created_at.isoformat(),
            updated_at=h.updated_at.isoformat(),
        )
        for h in best
    ]


@app.get("/performance")
async def get_performance() -> dict:
    """Get performance metrics.

    Returns:
        Performance history
    """
    return engine.get_performance_history()


@app.post("/discover", response_model=DiscoveryResponse)
async def start_discovery(request: DiscoveryRequest) -> DiscoveryResponse:
    """Start discovery process.

    Args:
        request: Discovery request parameters

    Returns:
        Discovery results
    """
    try:
        from prime_discovery.datasets.loaders import DatasetManager

        # Generate dataset
        manager = DatasetManager()
        dataset = manager.generate_prime_dataset()

        # Run discovery
        best_hyps, stats = engine.discover(
            dataset,
            num_iterations=request.num_iterations,
            population_size=request.population_size,
            num_vars=request.num_vars,
        )

        hypothesis_responses = [
            HypothesisResponse(
                hypothesis_id=h.hypothesis_id,
                expression=str(h.expression),
                status=h.status.value,
                fitness=h.fitness,
                accuracy=h.accuracy,
                created_at=h.created_at.isoformat(),
                updated_at=h.updated_at.isoformat(),
            )
            for h in best_hyps
        ]

        return DiscoveryResponse(best_hypotheses=hypothesis_responses, stats=stats)
    except Exception as e:
        logger.error(f"Discovery failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
