import numpy as np
from observableflow import Sensor, pareto_optimize

A = np.array([[[1.0, 0.0], [0.0, 2.0]]])
H = np.array([
    [[1.0, 1.0], [1.0, 1.0]],
    [[1.0, 0.0], [1.0, 0.0]],
    [[0.0, 1.0], [0.0, 1.0]],
])
sensors = [Sensor("dynamic", 1.0), Sensor("x1", 1.0), Sensor("x2", 1.0)]

for design in pareto_optimize(A, H, sensors, target_rank=2, max_depth=1, max_sensors=2, depth_unit_cost=0.5):
    print(design.to_dict())
