from pathlib import Path
import numpy as np

from observableflow.openfoam import (
    fit_lti_probe_model,
    fit_openfoam_case,
    generate_probes_function_object,
    load_numeric_snapshots,
    load_probes,
    pod_reduce_snapshots,
)


def _write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_load_probes_scalar_vector_and_restart(tmp_path):
    root = tmp_path / "postProcessing" / "probes"
    header = "# Probe 0 (0 0 0)\n# Probe 1 (1 0 0)\n# Time\n"
    _write(root / "0" / "p", header + "0 10 20\n1 11 21\n")
    _write(
        root / "0" / "U",
        header + "0 (1 0 0) (0 1 0)\n1 (2 0 0) (0 2 0)\n",
    )
    _write(root / "1" / "p", header + "1 111 121\n2 12 22\n")
    _write(
        root / "1" / "U",
        header + "1 (3 0 0) (0 3 0)\n2 (4 0 0) (0 4 0)\n",
    )
    ds = load_probes(tmp_path, fields=["p", "U"])
    assert np.allclose(ds.times, [0, 1, 2])
    assert ds.values.shape == (3, 8)
    assert ds.values[1, 0] == 111  # later restart segment wins
    assert ds.channel_names[:2] == ("p[p0]", "p[p1]")
    assert ds.channel_names[2:5] == ("U[p0].x", "U[p0].y", "U[p0].z")
    assert ds.channel_locations[0] == (0.0, 0.0, 0.0)


def test_numeric_snapshots_pod_and_fit(tmp_path):
    rows = [
        (0, "0 1 0\n1 0 1\n"),
        (1, "0 2 0\n1 0 1\n"),
        (2, "0 3 0\n1 0 1\n"),
        (3, "0 4 0\n1 0 1\n"),
    ]
    for t, row in rows:
        _write(
            tmp_path / "postProcessing" / "stateLine" / str(t) / "U.xy",
            "# x a b\n" + row,
        )
    snap = load_numeric_snapshots(
        tmp_path, object_name="stateLine", filename="U.xy", skip_columns=1
    )
    assert snap.values.shape == (4, 4)
    pod = pod_reduce_snapshots(snap.values, rank=2)
    assert pod.coordinates.shape == (4, 2)

    root = tmp_path / "postProcessing" / "probes" / "0"
    header = "# Probe 0 (0 0 0)\n# Probe 1 (1 0 0)\n"
    _write(root / "p", header + "0 1 0\n1 2 1\n2 3 1\n3 4 1\n")
    probes = load_probes(tmp_path, fields=["p"])
    X = np.array([[1.0, 0.0], [2.0, 1.0], [3.0, 1.0], [4.0, 1.0]])
    model = fit_lti_probe_model(X, probes)
    assert model.C.shape == (2, 2)
    result = model.optimize(
        target_rank=2, max_depth=1, max_sensors=2, method="pareto"
    )
    assert result and any(r.feasible for r in result)


def test_generate_probes_block():
    text = generate_probes_function_object(
        [(0, 0, 0), (1.5, 2, 3)], ["p", "U"]
    )
    assert "type                probes;" in text
    assert "fields              (p U);" in text
    assert "(1.5 2 3)" in text


def test_end_to_end_openfoam_case(tmp_path):
    A = np.array([[0.9, 0.2], [-0.1, 0.95]])
    x = np.array([1.0, 0.25])
    states = []
    for _ in range(10):
        states.append(x.copy())
        x = A @ x
    X = np.asarray(states)

    root = tmp_path / "postProcessing" / "probes" / "0"
    header = "# Probe 0 (0 0 0)\n# Probe 1 (1 0 0)\n"
    _write(
        root / "p",
        header
        + "".join(
            f"{k} {v[0]:.16g} {v[1]:.16g}\n" for k, v in enumerate(X)
        ),
    )

    for k, v in enumerate(X):
        row = (
            f"0 {v[0]:.16g} {v[1]:.16g}\n"
            f"1 {v[0] + v[1]:.16g} {2 * v[1]:.16g}\n"
        )
        _write(
            tmp_path / "postProcessing" / "stateSample" / str(k) / "state.raw",
            row,
        )

    model, pod = fit_openfoam_case(
        tmp_path,
        probe_fields=["p"],
        snapshot_object="stateSample",
        snapshot_filename="state.raw",
        snapshot_skip_columns=1,
        pod_rank=2,
    )
    assert model.state_series.shape == (10, 2)
    assert float(pod.explained_energy_ratio.sum()) > 0.999999
    out = model.optimize(
        target_rank=2, max_depth=2, max_sensors=2, method="greedy"
    )
    assert out is not None and out.feasible and out.rank == 2
