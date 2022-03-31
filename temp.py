
    def __getitem__(self, pos: Tuple[int, int]) -> int:
        i, j = pos
        return self.__data[i][j]

    def __setitem__(self, pos: Tuple[int, int], value: int):
        i, j = pos
        self.__data[i][j] = value

    def __add__(self, other: Matrix) -> Matrix:
        new = Matrix(self.dim)
        for i in range(self.dim):
            for j in range(self.dim):
                new[i, j] = self[i, j] + other[i, j]
        return new

    def __matmult__(self):
        ...