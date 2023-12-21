from helper import determinant

def test_determinant_2x2():
    assert determinant([[3, 4], [2, 5]]) == 7

def test_determinant_3x3():
    assert determinant([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 0

def test_determinant_4x4():
    assert determinant([[9, 3, -1, 5], [4, 2, -4, 6],
                       [3, 2, -5, 4], [-1, 2, 3, 4]]) == 272

def test_determinant_empty_matrix():
    assert determinant([]) == 0