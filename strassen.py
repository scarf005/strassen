from __future__ import annotations

from dataclasses import dataclass, field
from pprint import pformat
from typing import Any, Callable, List, Tuple

# 타입 힌트
Array2d = List[List[int]]


@dataclass
class Matrix:
    """
    N x N matrix
    """

    data: Array2d
    dim: int = field(init=False)

    Point = Tuple[int, int]
    SliceMat = Tuple[slice, slice]
    Quadrant = Tuple["Matrix", "Matrix", "Matrix", "Matrix"]
    SevenDivision = Tuple[
        "Matrix",
        "Matrix",
        "Matrix",
        "Matrix",
        "Matrix",
        "Matrix",
        "Matrix",
    ]

    def __post_init__(self):
        self.dim = len(self.data)
        assert self.dim > 0

    def __str__(self):
        longest_row_len = max([len(f"[{row},") for row in self.data])
        return pformat(self.data, width=longest_row_len)

    @classmethod
    def empty(cls, dim: int) -> Matrix:
        return cls(create_array2d(dim))

    def __getitem_pos(self, pos: Point) -> int:
        i, j = pos
        return self.data[i][j]

    def __getitem_slice(self, pos: SliceMat) -> Matrix:
        slice_i, slice_j = pos
        sliced_arr = [row[slice_j] for row in self.data[slice_i]]
        return Matrix(sliced_arr)

    @staticmethod
    def __is_tuple_member_type_of(tup: Tuple[Any, ...], type_: Any) -> bool:
        return all(isinstance(x, type_) for x in tup)

    def __getitem__(self, pos: Point | SliceMat) -> Any:
        if self.__is_tuple_member_type_of(pos, int):
            return self.__getitem_pos(pos)  # type: ignore
        elif self.__is_tuple_member_type_of(pos, slice):
            return self.__getitem_slice(pos)  # type: ignore
        else:
            raise TypeError(f"{pos} is not a valid index")

    def __setitem__(self, pos: Point, value: int):
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
    if A.dim <= threshold:
        return A @ B

    A11, A12, A21, A22 = divide(A)
    B11, B12, B21, B22 = divide(B)
    ops = (
        (A11 + A22, B11 + B22),
        (A21 + A22, B11),
        (A11, B12 - B22),
        (A22, B21 - B11),
        (A11 + A12, B22),
        (A21 - A11, B11 + B12),
        (A12 - A22, B21 + B22),
    )
    seven_division = tuple(strassen(*op) for op in ops)
    return conquer(seven_division)


def divide(A: Matrix) -> Tuple[Matrix, Matrix, Matrix, Matrix]:
    m = A.dim // 2
    return A[:m, :m], A[:m, m:], A[m:, :m], A[m:, m:]


def conquer(M: Matrix.SevenDivision) -> Matrix:
    C11 = M[0] + M[3] - M[4] + M[6]
    C12 = M[2] + M[4]
    C21 = M[1] + M[3]
    C22 = M[0] + M[2] - M[1] + M[5]
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


if __name__ == "__main__":
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
