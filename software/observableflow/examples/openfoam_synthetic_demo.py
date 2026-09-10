"""Self-contained OpenFOAM-like adapter demo; no OpenFOAM installation required."""

from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np

from observableflow.openfoam import fit_lti_probe_model, load_probes


with TemporaryDirectory() as td:
    case = Path(td)
    out = case / "postProcessing" / "probes" / "0"
    out.mkdir(parents=True)

    A = np.array([[1.0, 1.0], [0.0, 1.0]])
    x = np.array([0.2, 0.1])
    xs = []
    for _ in range(8):
        xs.append(x.copy())
        x = A @ x
    X = np.asarray(xs)

    header = "# Probe 0 (0 0 0)\n# Probe 1 (1 0 0)\n"
    rows = "".join(
        f"{k} {v[0]:.16g} {v[1]:.16g}\n" for k, v in enumerate(X)
    )
    (out / "p").write_text(header + rows, encoding="utf-8")

    ds = load_probes(case, fields=["p"])
    model = fit_lti_probe_model(
        X, ds, costs=[1.0, 1.0], noise_std=[0.1, 0.1]
    )
    frontier = model.optimize(
        target_rank=2,
        max_depth=2,
        max_sensors=2,
        depth_unit_cost=0.5,
        method="pareto",
    )

    print("channels:", ds.channel_names)
    print("state_rmse:", model.state_rmse)
    print("measurement_rmse:", model.measurement_rmse)
    for result in frontier:
        print(result.to_dict())
