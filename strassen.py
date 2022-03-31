from __future__ import annotations

from dataclasses import dataclass, field
from pprint import pformat
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

    @classmethod
    def empty(cls, dim: int) -> Matrix:
        return cls(create_array2d(dim))

    def __getitem__(self, pos: Tuple[int, int]) -> int:
        i, j = pos
        return self.data[i][j]

    def __setitem__(self, pos: Tuple[int, int], value: int):
        i, j = pos
        self.data[i][j] = value

    def __add__(self, other: Matrix) -> Matrix:
        new = Matrix.empty(self.dim)
        for i in range(self.dim):
            for j in range(self.dim):
                new[i, j] = self[i, j] + other[i, j]
        return new

    def __sub__(self, other: Matrix) -> Matrix:
        new = Matrix.empty(self.dim)
        for i in range(self.dim):
            for j in range(self.dim):
                new[i, j] = self[i, j] - other[i, j]
        return new

    def __matmul__(self, other: Matrix) -> Matrix:
        new = Matrix.empty(self.dim)
        for i in range(self.dim):
            for j in range(self.dim):
                new[i, j] = sum(
                    self[i, k] * other[k, j] for k in range(self.dim)
                )
        return new


def create_array2d(dimension: int) -> Array2d:
    return [[0] * dimension for _ in range(dimension)]


def strassen(A: Matrix, B: Matrix) -> Matrix:
    n = A.dim
    if n <= threshold:
        return A @ B
    A11, A12, A21, A22 = divide(A)
    B11, B12, B21, B22 = divide(B)
    M1 = strassen(A11 + A22, B11 + B22)
    M2 = strassen(A21 + A22, B11)
    M3 = strassen(A11, B12 - B22)
    M4 = strassen(A22, B21 - B11)
    M5 = strassen(A11 + A12, B22)
    M6 = strassen(A21 - A11, B11 + B12)
    M7 = strassen(A12 - A22, B21 + B22)
    return conquer(M1, M2, M3, M4, M5, M6, M7)


def divide(A: Matrix) -> Tuple[Matrix, Matrix, Matrix, Matrix]:
    n = A.dim
    m = n // 2
    A11, A12, A21, A22 = [Matrix.empty(m) for _ in range(4)]
    for i in range(m):
        for j in range(m):
            A11[i, j] = A[i, j]
            A12[i, j] = A[i, j + m]
            A21[i, j] = A[i + m, j]
            A22[i, j] = A[i + m, j + m]
    return A11, A12, A21, A22


def conquer(
    M1: Matrix,
    M2: Matrix,
    M3: Matrix,
    M4: Matrix,
    M5: Matrix,
    M6: Matrix,
    M7: Matrix,
) -> Matrix:
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 + M3 - M2 + M6
    m = C11.dim
    n = 2 * m
    # print(2 * m, 2 * m)
    C = Matrix.empty(n)
    for i in range(m):
        for j in range(m):
            C[i, j] = C11[i, j]
            C[i, j + m] = C12[i, j]
            C[i + m, j] = C21[i, j]
            C[i + m, j + m] = C22[i, j]
    return C


A = Matrix(
    [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 1, 2, 3],
        [4, 5, 6, 7],
    ]
)
B = Matrix(
    [
        [8, 9, 1, 2],
        [3, 4, 5, 6],
        [7, 8, 9, 1],
        [2, 3, 4, 5],
    ]
)

threshold = 2
print(f"{threshold = }")
print(strassen(A, B))
