def determinant(m):
    # base case: (1 x 1) matrix
    if len(m) == 1 and len(m[0]) == 1:
        return m[0][0]

    # base case: (2 x 2) matrix
    if len(m) == 2 and len(m[0]) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    # recursive case
    det = 0
    for i in range(len(m[0])):
        submatrix = [row[:i] + row[i + 1:] for row in m[1:]]
        det += ((-1) ** i) * m[0][i] * determinant(submatrix)

    return det