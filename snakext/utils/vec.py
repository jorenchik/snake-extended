""" This module contains simple vector (tuple operations). """


def vec_2d_add(vec_1: tuple[float, float],
               vec_2: tuple[float, float]) -> tuple[float, float]:
                    return (vec_1[0] + vec_2[0], vec_1[1] + vec_2[1])


def vec_2d_multiply(vec_1: tuple[float, float], vec_2: tuple[
                    float, float]) -> tuple[float, float]:
                    return (vec_1[0] * vec_2[0], vec_1[1] * vec_2[1])

