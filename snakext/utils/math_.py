import numpy as np
import numpy.typing as npt
from typing import Any
import math


def vec_2d_add(vec_1: tuple[float, float],
               vec_2: tuple[float, float]) -> tuple[float, float]:
    return (vec_1[0] + vec_2[0], vec_1[1] + vec_2[1])


def vec_2d_multiply(vec_1: tuple[float, float],
                    vec_2: tuple[float, float]) -> tuple[float, float]:
    return (vec_1[0] * vec_2[0], vec_1[1] * vec_2[1])


def arr_2d(rows: int, cols: int,
           dtype: type) -> np.ndarray[tuple[int, int], np.dtype[np.object_]]:
    return np.empty((rows, cols), dtype=dtype)


def fill_arr_2d(
    arr: npt.NDArray[Any],
    source_list: list[Any],
    rows: int,
    cols: int,
) -> npt.NDArray[Any]:
    for i in range(0, rows * cols):
        (y_pos, x_pos) = arr_2d_index(i, cols)
        arr[y_pos, x_pos] = source_list[i]
    return arr


def arr_2d_index(idx: int, cols: int) -> tuple[int, int]:
    x_pos = idx % cols
    y_pos = math.floor(idx / cols)
    return (y_pos, x_pos)
