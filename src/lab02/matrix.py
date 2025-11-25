def transpose(mat: list[list[float | int]]) -> list[list]:
    if len(mat) > 1:
        for lines in range(1, len(mat)):
            if len(mat[0]) != len(mat[lines]):
                ans = "ValueError"
            else:
                ans = [list(row) for row in zip(*mat)]
    else:
        ans = [list(row) for row in zip(*mat)]
    return ans


print(transpose([[1, 2], [3]]))


def row_sums(mat: list[list[float | int]]) -> list[float]:
    ans = []
    if len(mat) > 1:
        for lines in range(1, len(mat)):
            if len(mat[0]) != len(mat[lines]):
                ans = "ValueError"
            else:
                for lines in range(len(mat)):
                    ans.append(sum(mat[lines]))
    return ans


print(row_sums([[-1, 1], [10, -10]]))


def col_sums(mat: list[list[float | int]]) -> list[float]:
    ans = []
    for lines in range(len(mat)):
        if len(mat[0]) != len(mat[lines]):
            raise "ValueError"
            break
    for colums in range(len(mat[0])):
        sum = 0
        for lines in range(len(mat)):
            sum += mat[lines][colums]
        ans.append(sum)
    return ans


print(col_sums([[1, 2, 3], [4, 5, 6]]))
