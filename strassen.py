from __future__ import annotations

from dataclasses import dataclass, field
from pprint import pformat, pprint
from typing import Callable, List, Tuple

# 타입 힌트
Array2d = List[List[int]]


@dataclass
class Matrix:
    """
    N x N matrix
    """

    data: Array2d
    dim: int = field(init=False)

    def __post_init__(self):
        self.dim = len(self.data)
        assert self.dim > 0

    def __str__(self):
        longest_row_len = max([len(f"[{row},") for row in self.data])
        return pformat(self.data, width=longest_row_len)


def create_array2d(dimension: int) -> Array2d:
    return [[0] * dimension for _ in range(dimension)]


def strassen(A: Array2d, B: Array2d) -> Array2d:
    n = len(A)
    if n <= threshold:
        return matrixmult(A, B)
    A11, A12, A21, A22 = divide(A)
    B11, B12, B21, B22 = divide(B)
    M1 = strassen(madd(A11, A22), madd(B11, B22))
    M2 = strassen(madd(A21, A22), B11)
    M3 = strassen(A11, msub(B12, B22))
    M4 = strassen(A22, msub(B21, B11))
    M5 = strassen(madd(A11, A12), B22)
    M6 = strassen(msub(A21, A11), madd(B11, B12))
    M7 = strassen(msub(A12, A22), madd(B21, B22))
    return conquer(M1, M2, M3, M4, M5, M6, M7)


def divide(A) -> Tuple[Array2d, Array2d, Array2d, Array2d]:
    n = len(A)
    m = n // 2
    A11, A12, A21, A22 = [create_array2d(m) for _ in range(4)]
    for i in range(m):
        for j in range(m):
            A11[i][j] = A[i][j]
            A12[i][j] = A[i][j + m]
            A21[i][j] = A[i + m][j]
            A22[i][j] = A[i + m][j + m]
    return A11, A12, A21, A22


def conquer(M1, M2, M3, M4, M5, M6, M7) -> Array2d:
    C11 = madd(msub(madd(M1, M4), M5), M7)
    C12 = madd(M3, M5)
    C21 = madd(M2, M4)
    C22 = madd(msub(madd(M1, M3), M2), M6)
    m = len(C11)
    n = 2 * m
    # print(2 * m, 2 * m)
    C = create_array2d(n)
    for i in range(m):
        for j in range(m):
            C[i][j] = C11[i][j]
            C[i][j + m] = C12[i][j]
            C[i + m][j] = C21[i][j]
            C[i + m][j + m] = C22[i][j]
    return C


def matrix_map(
    A: Array2d, B: Array2d, func: Callable[[int, int], int]
) -> Array2d:
    new = create_array2d(len(A))
    n = len(A)
    for i in range(n):
        for j in range(n):
            new[i][j] = func(A[i][j], B[i][j])
    return new


def madd(A: Array2d, B: Array2d) -> Array2d:
    return matrix_map(A, B, lambda x, y: x + y)


def msub(A: Array2d, B: Array2d) -> Array2d:
    return matrix_map(A, B, lambda x, y: x - y)


def matrixmult(A: Array2d, B: Array2d) -> Array2d:  # 1.4 Matrix Multiplication
    n = len(A)
    C = create_array2d(n)
    for i in range(n):
        for j in range(n):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
    return C


A = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 1, 2, 3],
    [4, 5, 6, 7],
]
B = [
    [8, 9, 1, 2],
    [3, 4, 5, 6],
    [7, 8, 9, 1],
    [2, 3, 4, 5],
]

threshold = 2
print(f"{threshold =}")
pprint(A, width=40)
pprint(B, width=40)
# pprint(madd(A, B), width=40)
print("===")
Amat = Matrix(A)
Bmat = Matrix(B)
print(Amat)
print(Bmat)
# print(Amat + Bmat)
# C = strassen(A, B)
# for i, elem in enumerate(C):
#     print(f"C[{i}] = {elem}")
