from pathlib import Path
import numpy as np

from observableflow.openfoam_benchmark import benchmark_probe_reference_case


def _write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def test_probe_reference_benchmark_holdout(tmp_path):
    A = np.array([[0.92, 0.15], [-0.08, 0.96]])
    x = np.array([1.0, 0.3])
    states = []
    for _ in range(60):
        states.append(x.copy())
        x = A @ x
    X = np.asarray(states)
    h_c = '# Probe 0 (0.02 0.02 0.005)\n# Probe 1 (0.08 0.08 0.005)\n'
    _write(tmp_path/'postProcessing'/'candidates'/'0'/'p', h_c + ''.join(
        f'{k} {v[0]+0.2*v[1]:.16g} {0.1*v[0]+v[1]:.16g}\n' for k,v in enumerate(X)))
    h_r = '# Probe 0 (0.03 0.03 0.005)\n# Probe 1 (0.07 0.07 0.005)\n'
    _write(tmp_path/'postProcessing'/'reference'/'0'/'p', h_r + ''.join(
        f'{k} {v[0]:.16g} {v[1]:.16g}\n' for k,v in enumerate(X)))
    out = benchmark_probe_reference_case(
        tmp_path,
        candidate_object='candidates', reference_object='reference',
        candidate_fields=['p'], reference_fields=['p'], pod_rank=2,
        train_fraction=0.7, max_depth=3, max_sensors=2,
        noise_fraction=1e-4, costs=[1.0, 2.0],
    )
    assert out.temporal_design is not None and out.temporal_design['feasible']
    assert out.holdout_noiseless is not None
    assert out.holdout_noiseless['nrmse'] < 1e-6
    assert out.holdout_noisy is not None


def test_pressure_costs_change_total_cost(tmp_path):
    A = np.array([[0.9, 0.1], [0.0, 0.95]])
    x = np.array([1.0, 0.2])
    X=[]
    for _ in range(40):
        X.append(x.copy()); x=A@x
    X=np.asarray(X)
    h='# Probe 0 (0.02 0.02 0.005)\n# Probe 1 (0.08 0.08 0.005)\n'
    vals=''.join(f'{k} {v[0]:.16g} {v[1]:.16g}\n' for k,v in enumerate(X))
    _write(tmp_path/'postProcessing'/'candidates'/'0'/'p', h+vals)
    _write(tmp_path/'postProcessing'/'reference'/'0'/'p', h+vals)
    out=benchmark_probe_reference_case(
        tmp_path, candidate_object='candidates', reference_object='reference',
        candidate_fields=['p'], reference_fields=['p'], pod_rank=2,
        max_depth=2, max_sensors=2, costs=[3.0,4.0], noise_fraction=1e-5,
    )
    assert out.temporal_design is not None
    assert out.temporal_design['sensor_cost'] >= 3.0
