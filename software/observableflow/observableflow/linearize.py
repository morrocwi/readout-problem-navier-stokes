from __future__ import annotations

from typing import Callable, Sequence
import numpy as np


def finite_difference_jacobian(func: Callable[[np.ndarray], np.ndarray], x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    y0 = np.atleast_1d(np.asarray(func(x), dtype=float))
    J = np.empty((y0.size, x.size), dtype=float)
    for j in range(x.size):
        h = eps * max(1.0, abs(x[j]))
        xp = x.copy(); xm = x.copy()
        xp[j] += h; xm[j] -= h
        yp = np.atleast_1d(np.asarray(func(xp), dtype=float))
        ym = np.atleast_1d(np.asarray(func(xm), dtype=float))
        J[:, j] = (yp - ym) / (2.0 * h)
    return J


def linearize_trajectory(
    step: Callable[[np.ndarray], np.ndarray],
    readers: Sequence[Callable[[np.ndarray], float]],
    x0: np.ndarray,
    depth: int,
    eps: float = 1e-6,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Linearize a discrete nonlinear simulator and scalar readers along one trajectory."""
    x = np.asarray(x0, dtype=float).copy()
    states = [x.copy()]
    transitions = []
    H = np.empty((len(readers), depth + 1, x.size), dtype=float)
    for k in range(depth + 1):
        for i, h in enumerate(readers):
            H[i, k] = finite_difference_jacobian(lambda z, h=h: np.array([h(z)]), x, eps=eps)[0]
        if k < depth:
            A = finite_difference_jacobian(step, x, eps=eps)
            transitions.append(A)
            x = np.asarray(step(x), dtype=float)
            states.append(x.copy())
    return np.asarray(states), np.asarray(transitions), H
