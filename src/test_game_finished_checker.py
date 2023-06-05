from game_finished_checker import check_if_game_finished


def test_check_if_game_finished_vertical():
    board = [[0, 0, -1, 0, 0, 0, 0],
             [0, 0, -1, 0, 0, 0, 0],
             [0, 0, -1, 0, 0, 0, 0],
             [0, 0, -1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    assert check_if_game_finished(board)


def test_check_if_game_finished_horizontal_beginning_of_row():
    board = [[1, 1, 1, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    assert check_if_game_finished(board)


def test_check_if_game_finished_horizontal_end_of_row():
    board = [[0, 0, 0, 1, 1, 1, 1],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    assert check_if_game_finished(board)


def test_check_if_game_finished_diagonal_right_end():
    board = [[0, 0, 0, 1, -1, -1, -1],
             [0, 0, 0, 0, 1, -1, -1],
             [0, 0, 0, 0, 0, 1, -1],
             [0, 0, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    assert check_if_game_finished(board)


def test_check_if_game_finished_diagonal_right_beg():
    board = [[1, -1, -1, -1, 0, 0, 0],
             [0, 1, -1, -1, 0, 0, 0],
             [0, 0, 1, -1, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    assert check_if_game_finished(board)


def test_check_if_game_finished_diagonal_left_beg():
    board = [[-1, -1, -1, 1, 0, 0, 0],
             [-1, -1, 1, 0, 0, 0, 0],
             [-1, 1, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
    assert check_if_game_finished(board)
