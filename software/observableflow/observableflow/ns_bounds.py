from __future__ import annotations

import math


def cubic_galerkin_dimension(N: int) -> int:
    if N < 1:
        raise ValueError("N must be >= 1")
    return 2 * ((2 * N + 1) ** 3 - 1)


def shell_values(N: int) -> tuple[int, ...]:
    if N < 1:
        raise ValueError("N must be >= 1")
    values = {
        i*i + j*j + k*k
        for i in range(-N, N + 1)
        for j in range(-N, N + 1)
        for k in range(-N, N + 1)
        if (i, j, k) != (0, 0, 0)
    }
    return tuple(sorted(values))


def shell_count(N: int) -> int:
    return len(shell_values(N))


def scalar_min_depth(N: int, symmetry_dim: int = 3) -> int:
    return cubic_galerkin_dimension(N) - symmetry_dim - 1


def shell_min_depth(N: int, symmetry_dim: int = 3) -> int:
    d = cubic_galerkin_dimension(N)
    m = shell_count(N)
    return math.ceil((d - symmetry_dim - m) / (m - 1))


def summary(N: int) -> dict:
    d = cubic_galerkin_dimension(N)
    m = shell_count(N)
    return {
        "N": N,
        "real_state_dimension": d,
        "translation_ceiling": d - 3,
        "shell_count": m,
        "shells": list(shell_values(N)),
        "scalar_min_depth": scalar_min_depth(N),
        "shell_min_depth": shell_min_depth(N),
    }
