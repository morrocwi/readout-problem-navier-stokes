from __future__ import annotations

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("Install observableflow[api] to use the REST API") from exc

import numpy as np
from .core import Sensor, analyze_design
from .optimize import greedy_optimize

app = FastAPI(title="ObservableFlow API", version="0.1.0")


class SensorIn(BaseModel):
    name: str
    cost: float = Field(default=1.0, gt=0)
    noise_std: float = Field(default=1.0, gt=0)


class AnalyzeRequest(BaseModel):
    transitions: list[list[list[float]]]
    measurement_jacobians: list[list[list[float]]]
    sensors: list[SensorIn]
    selected: list[int]
    depth: int = Field(ge=0)
    target_rank: int = Field(gt=0)
    depth_unit_cost: float = Field(default=0.0, ge=0)
    min_sigma: float = Field(default=0.0, ge=0)


class OptimizeRequest(BaseModel):
    transitions: list[list[list[float]]]
    measurement_jacobians: list[list[list[float]]]
    sensors: list[SensorIn]
    target_rank: int = Field(gt=0)
    max_depth: int = Field(ge=0)
    max_sensors: int | None = Field(default=None, gt=0)
    depth_unit_cost: float = Field(default=0.0, ge=0)
    min_sigma: float = Field(default=0.0, ge=0)


def _sensors(items: list[SensorIn]) -> list[Sensor]:
    return [Sensor(name=s.name, cost=s.cost, noise_std=s.noise_std) for s in items]


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "engine": "observableflow", "version": "0.1.0"}


@app.post("/v1/analyze")
def analyze(req: AnalyzeRequest) -> dict:
    try:
        result = analyze_design(
            np.asarray(req.transitions), np.asarray(req.measurement_jacobians), _sensors(req.sensors),
            req.selected, req.depth, target_rank=req.target_rank,
            depth_unit_cost=req.depth_unit_cost, min_sigma=req.min_sigma,
        )
        return result.to_dict()
    except (ValueError, IndexError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/v1/optimize")
def optimize(req: OptimizeRequest) -> dict:
    try:
        result = greedy_optimize(
            np.asarray(req.transitions), np.asarray(req.measurement_jacobians), _sensors(req.sensors),
            target_rank=req.target_rank, max_depth=req.max_depth, max_sensors=req.max_sensors,
            depth_unit_cost=req.depth_unit_cost, min_sigma=req.min_sigma,
        )
        return {"status": "feasible" if result else "infeasible", "design": None if result is None else result.to_dict()}
    except (ValueError, IndexError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
