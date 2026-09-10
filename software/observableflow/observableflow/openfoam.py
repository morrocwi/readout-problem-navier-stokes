"""OpenFOAM adapter for ObservableFlow.

The adapter targets the standard postProcessing layout produced by OpenFOAM
function objects, especially ``probes`` and tabular sampled-set/surface output.
It intentionally does not parse native volField binary files. The bridge is:

OpenFOAM postProcessing -> probe/snapshot arrays -> optional POD -> fitted local
linear observable model -> ObservableFlow sensor/depth optimizer.

The fitted model is an engineering approximation. It is separate from the exact
finite-field Navier--Stokes certificates in the parent repository.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import re
import numpy as np

from .core import Sensor, AnalysisResult
from .optimize import greedy_optimize, pareto_optimize

_FLOAT = re.compile(r"(?i)[+-]?(?:(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|nan|inf)")
_PROBE = re.compile(r"^\s*#\s*Probe\s+(\d+)\s*\(([^)]*)\)", re.IGNORECASE)


@dataclass(frozen=True)
class ProbeDataset:
    times: np.ndarray
    values: np.ndarray
    channel_names: tuple[str, ...]
    channel_locations: tuple[tuple[float, float, float] | None, ...]
    fields: tuple[str, ...]
    source_files: tuple[str, ...]

    @property
    def n_samples(self) -> int:
        return int(self.values.shape[0])

    @property
    def n_channels(self) -> int:
        return int(self.values.shape[1])


@dataclass(frozen=True)
class SnapshotDataset:
    times: np.ndarray
    values: np.ndarray
    source_files: tuple[str, ...]


@dataclass(frozen=True)
class PODReduction:
    coordinates: np.ndarray
    basis: np.ndarray
    mean: np.ndarray
    singular_values: np.ndarray
    explained_energy_ratio: np.ndarray


@dataclass(frozen=True)
class OpenFOAMObservableModel:
    times: np.ndarray
    state_series: np.ndarray
    probe_dataset: ProbeDataset
    transitions: np.ndarray
    measurement_jacobians: np.ndarray
    sensors: tuple[Sensor, ...]
    A: np.ndarray
    C: np.ndarray
    state_rmse: float
    measurement_rmse: float

    def optimize(
        self,
        *,
        target_rank: int | None = None,
        max_depth: int = 10,
        max_sensors: int | None = None,
        depth_unit_cost: float = 0.0,
        min_sigma: float = 0.0,
        method: str = "greedy",
        max_combinations: int = 200_000,
        rtol: float = 1e-10,
    ) -> AnalysisResult | list[AnalysisResult] | None:
        target = self.state_series.shape[1] if target_rank is None else int(target_rank)
        kwargs = dict(
            target_rank=target,
            max_depth=max_depth,
            max_sensors=max_sensors,
            depth_unit_cost=depth_unit_cost,
            min_sigma=min_sigma,
            rtol=rtol,
        )
        if method == "greedy":
            return greedy_optimize(
                self.transitions, self.measurement_jacobians, self.sensors, **kwargs
            )
        if method == "pareto":
            return pareto_optimize(
                self.transitions,
                self.measurement_jacobians,
                self.sensors,
                max_combinations=max_combinations,
                **kwargs,
            )
        raise ValueError("method must be 'greedy' or 'pareto'")


def _split_top_level_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    buf: list[str] = []
    depth = 0
    for ch in text.strip():
        if ch.isspace() and depth == 0:
            if buf:
                tokens.append("".join(buf))
                buf = []
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                raise ValueError(f"unbalanced ')' in OpenFOAM row: {text!r}")
        buf.append(ch)
    if depth != 0:
        raise ValueError(f"unbalanced parentheses in OpenFOAM row: {text!r}")
    if buf:
        tokens.append("".join(buf))
    return tokens


def _numbers(token: str) -> list[float]:
    vals = [float(x) for x in _FLOAT.findall(token)]
    if not vals:
        raise ValueError(f"cannot parse numeric OpenFOAM value: {token!r}")
    return vals


def _component_labels(width: int) -> tuple[str, ...]:
    if width == 1:
        return ("",)
    if width == 3:
        return ("x", "y", "z")
    if width == 6:
        return ("xx", "xy", "xz", "yy", "yz", "zz")
    if width == 9:
        return ("xx", "xy", "xz", "yx", "yy", "yz", "zx", "zy", "zz")
    return tuple(str(i) for i in range(width))


def _read_probe_segment(
    path: Path, field_name: str
) -> tuple[
    np.ndarray,
    np.ndarray,
    tuple[str, ...],
    tuple[tuple[float, float, float] | None, ...],
]:
    locations: dict[int, tuple[float, float, float]] = {}
    rows: list[list[float]] = []
    times: list[float] = []
    probe_count: int | None = None
    width: int | None = None

    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            m = _PROBE.match(raw)
            if m:
                xyz = _numbers(m.group(2))
                if len(xyz) >= 3:
                    locations[int(m.group(1))] = (xyz[0], xyz[1], xyz[2])
                continue
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            tokens = _split_top_level_tokens(line)
            if len(tokens) < 2:
                continue
            try:
                t = float(tokens[0])
            except ValueError:
                continue
            value_tokens = tokens[1:]
            if probe_count is None:
                probe_count = len(value_tokens)
            elif len(value_tokens) != probe_count:
                raise ValueError(
                    f"inconsistent probe count in {path}: expected {probe_count}, "
                    f"got {len(value_tokens)}"
                )
            flattened: list[float] = []
            for tok in value_tokens:
                vals = _numbers(tok)
                if width is None:
                    width = len(vals)
                if len(vals) != width:
                    raise ValueError(
                        f"mixed value widths in {path}: expected {width}, got {len(vals)}"
                    )
                flattened.extend(vals)
            times.append(t)
            rows.append(flattened)

    if not rows or probe_count is None or width is None:
        raise ValueError(f"no probe data found in {path}")

    labels = _component_labels(width)
    names: list[str] = []
    channel_locations: list[tuple[float, float, float] | None] = []
    for p in range(probe_count):
        loc = locations.get(p)
        for label in labels:
            suffix = f".{label}" if label else ""
            names.append(f"{field_name}[p{p}]{suffix}")
            channel_locations.append(loc)
    return (
        np.asarray(times, dtype=float),
        np.asarray(rows, dtype=float),
        tuple(names),
        tuple(channel_locations),
    )


def _numeric_time_dirs(root: Path) -> list[Path]:
    out: list[tuple[float, Path]] = []
    if not root.exists():
        return []
    for p in root.iterdir():
        if not p.is_dir():
            continue
        try:
            t = float(p.name)
        except ValueError:
            continue
        out.append((t, p))
    out.sort(key=lambda x: x[0])
    return [p for _, p in out]


def load_probes(
    case_dir: str | Path,
    *,
    object_name: str = "probes",
    fields: Sequence[str] | None = None,
) -> ProbeDataset:
    """Load OpenFOAM ``probes`` function-object output.

    Expected layout: ``CASE/postProcessing/<object_name>/<start-time>/<field>``.
    Restart segments are merged by physical time; later segments overwrite
    duplicate times. Scalar, vector and flattened tensor values are supported.
    """
    root = Path(case_dir) / "postProcessing" / object_name
    segments = _numeric_time_dirs(root)
    if not segments:
        raise FileNotFoundError(f"no numeric postProcessing segments under {root}")

    if fields is None:
        discovered: set[str] = set()
        for seg in segments:
            discovered.update(
                p.name for p in seg.iterdir() if p.is_file() and not p.name.startswith(".")
            )
        field_order = tuple(sorted(discovered))
    else:
        field_order = tuple(str(f) for f in fields)
    if not field_order:
        raise ValueError("no OpenFOAM probe fields selected")

    field_maps: list[dict[float, np.ndarray]] = []
    field_names: list[tuple[str, ...]] = []
    field_locations: list[tuple[tuple[float, float, float] | None, ...]] = []
    sources: list[str] = []

    for field in field_order:
        by_time: dict[float, np.ndarray] = {}
        names: tuple[str, ...] | None = None
        locs: tuple[tuple[float, float, float] | None, ...] | None = None
        found = False
        for seg in segments:
            path = seg / field
            if not path.is_file():
                continue
            found = True
            t, v, n, l = _read_probe_segment(path, field)
            if names is None:
                names, locs = n, l
            elif n != names or l != locs:
                raise ValueError(
                    f"probe channel layout changed across restart segments for field {field}"
                )
            for ti, vi in zip(t, v):
                by_time[float(ti)] = np.asarray(vi, dtype=float)
            sources.append(str(path))
        if not found or names is None or locs is None:
            raise FileNotFoundError(f"field {field!r} not found under {root}")
        field_maps.append(by_time)
        field_names.append(names)
        field_locations.append(locs)

    common = set(field_maps[0])
    for m in field_maps[1:]:
        common.intersection_update(m)
    if not common:
        raise ValueError("selected probe fields have no common physical times")
    times = np.asarray(sorted(common), dtype=float)
    blocks = [np.vstack([m[float(t)] for t in times]) for m in field_maps]
    values = np.hstack(blocks)
    if not np.all(np.isfinite(values)):
        raise ValueError(
            "probe output contains NaN/Inf; clean or exclude invalid probes before optimization"
        )
    names = tuple(x for group in field_names for x in group)
    locs = tuple(x for group in field_locations for x in group)
    return ProbeDataset(times, values, names, locs, field_order, tuple(sources))


def generate_probes_function_object(
    locations: Sequence[Sequence[float]],
    fields: Sequence[str],
    *,
    name: str = "observableFlowProbes",
    write_control: str = "timeStep",
    write_interval: int | float = 1,
    interpolation_scheme: str = "cellPoint",
    fixed_locations: bool = True,
    library: str = "sampling",
) -> str:
    """Generate a probes function-object block for inclusion in controlDict."""
    locs = [tuple(float(x) for x in loc) for loc in locations]
    if not locs or any(len(loc) != 3 for loc in locs):
        raise ValueError("locations must contain one or more xyz triples")
    fs = tuple(str(f) for f in fields)
    if not fs:
        raise ValueError("at least one field is required")
    loc_text = "\n".join(
        f"        ({x:.16g} {y:.16g} {z:.16g})" for x, y, z in locs
    )
    fixed = "true" if fixed_locations else "false"
    return f"""{name}
{{
    type                probes;
    libs                ({library});
    writeControl        {write_control};
    writeInterval       {write_interval};
    fixedLocations      {fixed};
    interpolationScheme {interpolation_scheme};
    fields              ({' '.join(fs)});
    probeLocations
    (
{loc_text}
    );
}}
"""


def load_numeric_snapshots(
    case_dir: str | Path,
    *,
    object_name: str,
    filename: str,
    skip_columns: int = 0,
) -> SnapshotDataset:
    """Load one tabular sampled file per OpenFOAM time directory and flatten it.

    This targets ASCII/CSV-like output from sampled sets/surfaces or custom
    function objects. ``skip_columns`` removes coordinate columns on each row
    before flattening. Native OpenFOAM binary volFields are intentionally out of
    scope for this adapter version.
    """
    if skip_columns < 0:
        raise ValueError("skip_columns must be non-negative")
    root = Path(case_dir) / "postProcessing" / object_name
    times: list[float] = []
    snapshots: list[list[float]] = []
    sources: list[str] = []
    width: int | None = None
    for seg in _numeric_time_dirs(root):
        path = seg / filename
        if not path.is_file():
            continue
        flat: list[float] = []
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                vals = [float(x) for x in _FLOAT.findall(line)]
                if len(vals) <= skip_columns:
                    continue
                flat.extend(vals[skip_columns:])
        if not flat:
            continue
        if width is None:
            width = len(flat)
        elif len(flat) != width:
            raise ValueError(
                f"snapshot width changed at {path}: expected {width}, got {len(flat)}"
            )
        times.append(float(seg.name))
        snapshots.append(flat)
        sources.append(str(path))
    if not snapshots:
        raise FileNotFoundError(f"no snapshots named {filename!r} found under {root}")
    arr = np.asarray(snapshots, dtype=float)
    if not np.all(np.isfinite(arr)):
        raise ValueError("snapshot output contains NaN/Inf")
    return SnapshotDataset(np.asarray(times), arr, tuple(sources))


def pod_reduce_snapshots(
    snapshots: np.ndarray,
    rank: int,
    *,
    center: bool = True,
) -> PODReduction:
    X = np.asarray(snapshots, dtype=float)
    if X.ndim != 2:
        raise ValueError("snapshots must have shape (time, spatial_features)")
    r = int(rank)
    if r < 1 or r > min(X.shape):
        raise ValueError("rank must satisfy 1 <= rank <= min(snapshot shape)")
    mean = X.mean(axis=0) if center else np.zeros(X.shape[1])
    Xc = X - mean
    _, s, vt = np.linalg.svd(Xc, full_matrices=False)
    basis = vt[:r].T
    coordinates = Xc @ basis
    energy = s * s
    denom = float(np.sum(energy))
    ratio = energy[:r] / denom if denom > 0 else np.zeros(r)
    return PODReduction(coordinates, basis, mean, s[:r], ratio)


def _linear_map_with_intercept(
    X: np.ndarray, Y: np.ndarray, ridge: float
) -> tuple[np.ndarray, np.ndarray]:
    """Fit Y ~= X B + b. Return B and b."""
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    Z = np.column_stack((X, np.ones(len(X))))
    if ridge <= 0:
        beta = np.linalg.lstsq(Z, Y, rcond=None)[0]
    else:
        reg = np.eye(Z.shape[1]) * float(ridge)
        reg[-1, -1] = 0.0
        beta = np.linalg.solve(Z.T @ Z + reg, Z.T @ Y)
    return beta[:-1], beta[-1]


def fit_lti_probe_model(
    state_series: np.ndarray,
    probes: ProbeDataset,
    *,
    costs: Sequence[float] | None = None,
    noise_std: Sequence[float] | None = None,
    ridge: float = 0.0,
) -> OpenFOAMObservableModel:
    """Fit an affine LTI ROM Jacobian bridge from aligned states and probes.

    ``state_series`` contains reduced CFD state coordinates at the same times as
    ``probes``. Affine offsets are fitted but do not affect observability; the
    returned A and C are the state/measurement Jacobians used by ObservableFlow.
    """
    X = np.asarray(state_series, dtype=float)
    Y = np.asarray(probes.values, dtype=float)
    if not np.all(np.isfinite(X)) or not np.all(np.isfinite(Y)):
        raise ValueError("state/probe series must be finite")
    if X.ndim != 2 or X.shape[0] != Y.shape[0]:
        raise ValueError(
            "state_series must have shape (probe_times, state_dimension)"
        )
    if len(X) < 3:
        raise ValueError("at least three aligned time samples are required")
    if ridge < 0:
        raise ValueError("ridge must be non-negative")

    Bd, bd = _linear_map_with_intercept(X[:-1], X[1:], ridge)
    A = Bd.T
    Bm, bm = _linear_map_with_intercept(X, Y, ridge)
    C = Bm.T
    state_pred = X[:-1] @ Bd + bd
    y_pred = X @ Bm + bm
    state_rmse = float(np.sqrt(np.mean((state_pred - X[1:]) ** 2)))
    measurement_rmse = float(np.sqrt(np.mean((y_pred - Y) ** 2)))

    m = Y.shape[1]
    c = np.ones(m) if costs is None else np.asarray(costs, dtype=float)
    ns = np.ones(m) if noise_std is None else np.asarray(noise_std, dtype=float)
    if c.shape != (m,) or np.any(c < 0):
        raise ValueError(
            "costs must be non-negative with one value per probe channel"
        )
    if ns.shape != (m,) or np.any(ns <= 0):
        raise ValueError(
            "noise_std must be positive with one value per probe channel"
        )
    sensors = tuple(
        Sensor(name, float(cost), float(noise))
        for name, cost, noise in zip(probes.channel_names, c, ns)
    )
    transitions = np.repeat(A[None, :, :], len(X) - 1, axis=0)
    H = np.repeat(C[:, None, :], len(X), axis=1)
    return OpenFOAMObservableModel(
        probes.times.copy(),
        X.copy(),
        probes,
        transitions,
        H,
        sensors,
        A,
        C,
        state_rmse,
        measurement_rmse,
    )


def _align_times(
    a: np.ndarray, b: np.ndarray, atol: float = 1e-10
) -> tuple[np.ndarray, np.ndarray]:
    ia: list[int] = []
    ib: list[int] = []
    j = 0
    for i, t in enumerate(np.asarray(a, dtype=float)):
        while j < len(b) and b[j] < t - atol:
            j += 1
        if j < len(b) and abs(float(b[j]) - float(t)) <= atol:
            ia.append(i)
            ib.append(j)
    if not ia:
        raise ValueError("probe and snapshot series have no aligned times")
    return np.asarray(ia, dtype=int), np.asarray(ib, dtype=int)


def fit_openfoam_case(
    case_dir: str | Path,
    *,
    probe_object: str = "probes",
    probe_fields: Sequence[str] | None = None,
    snapshot_object: str,
    snapshot_filename: str,
    snapshot_skip_columns: int = 0,
    pod_rank: int,
    costs: Sequence[float] | None = None,
    noise_std: Sequence[float] | None = None,
    ridge: float = 0.0,
    time_atol: float = 1e-10,
) -> tuple[OpenFOAMObservableModel, PODReduction]:
    """End-to-end OpenFOAM postProcessing -> POD -> observable LTI ROM bridge."""
    probes = load_probes(
        case_dir, object_name=probe_object, fields=probe_fields
    )
    snapshots = load_numeric_snapshots(
        case_dir,
        object_name=snapshot_object,
        filename=snapshot_filename,
        skip_columns=snapshot_skip_columns,
    )
    ip, isnap = _align_times(probes.times, snapshots.times, atol=time_atol)
    aligned_probes = ProbeDataset(
        probes.times[ip],
        probes.values[ip],
        probes.channel_names,
        probes.channel_locations,
        probes.fields,
        probes.source_files,
    )
    reduction = pod_reduce_snapshots(snapshots.values[isnap], pod_rank)
    model = fit_lti_probe_model(
        reduction.coordinates,
        aligned_probes,
        costs=costs,
        noise_std=noise_std,
        ridge=ridge,
    )
    return model, reduction
