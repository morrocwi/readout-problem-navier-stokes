from __future__ import annotations

import argparse
import json
from pathlib import Path

from .openfoam import (
    fit_openfoam_case,
    generate_probes_function_object,
    load_probes,
)


def _loc(value: str) -> tuple[float, float, float]:
    parts = [x.strip() for x in value.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("location must be x,y,z")
    return tuple(float(x) for x in parts)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="observableflow-openfoam")
    sub = p.add_subparsers(dest="cmd", required=True)

    ins = sub.add_parser("inspect-probes", help="inspect OpenFOAM probes output")
    ins.add_argument("case")
    ins.add_argument("--object", default="probes")
    ins.add_argument("--field", action="append", dest="fields")

    gen = sub.add_parser(
        "generate-probes", help="generate a controlDict probes block"
    )
    gen.add_argument("--field", action="append", required=True, dest="fields")
    gen.add_argument(
        "--location", action="append", required=True, type=_loc, dest="locations"
    )
    gen.add_argument("--name", default="observableFlowProbes")
    gen.add_argument("--output")

    opt = sub.add_parser(
        "optimize", help="fit POD/LTI bridge and optimize probe channels"
    )
    opt.add_argument("case")
    opt.add_argument("--probe-object", default="probes")
    opt.add_argument("--field", action="append", dest="fields")
    opt.add_argument("--snapshot-object", required=True)
    opt.add_argument("--snapshot-file", required=True)
    opt.add_argument("--snapshot-skip-columns", type=int, default=0)
    opt.add_argument("--pod-rank", type=int, required=True)
    opt.add_argument("--max-depth", type=int, default=10)
    opt.add_argument("--max-sensors", type=int)
    opt.add_argument("--depth-unit-cost", type=float, default=0.0)
    opt.add_argument("--min-sigma", type=float, default=0.0)
    opt.add_argument("--ridge", type=float, default=0.0)
    opt.add_argument("--method", choices=["greedy", "pareto"], default="greedy")

    a = p.parse_args(argv)
    if a.cmd == "inspect-probes":
        ds = load_probes(a.case, object_name=a.object, fields=a.fields)
        print(
            json.dumps(
                {
                    "samples": ds.n_samples,
                    "channels": ds.n_channels,
                    "time_start": float(ds.times[0]),
                    "time_end": float(ds.times[-1]),
                    "channel_names": ds.channel_names,
                    "fields": ds.fields,
                },
                indent=2,
            )
        )
        return 0

    if a.cmd == "generate-probes":
        text = generate_probes_function_object(
            a.locations, a.fields, name=a.name
        )
        if a.output:
            Path(a.output).write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 0

    if a.cmd == "optimize":
        model, pod = fit_openfoam_case(
            a.case,
            probe_object=a.probe_object,
            probe_fields=a.fields,
            snapshot_object=a.snapshot_object,
            snapshot_filename=a.snapshot_file,
            snapshot_skip_columns=a.snapshot_skip_columns,
            pod_rank=a.pod_rank,
            ridge=a.ridge,
        )
        result = model.optimize(
            target_rank=a.pod_rank,
            max_depth=a.max_depth,
            max_sensors=a.max_sensors,
            depth_unit_cost=a.depth_unit_cost,
            min_sigma=a.min_sigma,
            method=a.method,
        )
        payload = {
            "pod_explained_energy": float(pod.explained_energy_ratio.sum()),
            "state_rmse": model.state_rmse,
            "measurement_rmse": model.measurement_rmse,
            "result": (
                [r.to_dict() for r in result]
                if isinstance(result, list)
                else (None if result is None else result.to_dict())
            ),
        }
        print(json.dumps(payload, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
