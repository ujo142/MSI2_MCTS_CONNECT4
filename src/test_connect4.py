from connect4 import Connect4


def test_check_if_game_finished_vertical():
    c4 = Connect4()
    c4.board = [[0, 0, -1, 0, 0, 0, 0],
                [0, 0, -1, 0, 0, 0, 0],
                [0, 0, -1, 0, 0, 0, 0],
                [0, 0, -1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
    assert c4.check_if_game_finished(3, 2)


def test_check_if_game_finished_horizontal_beginning_of_row():
    c4 = Connect4()
    c4.board = [[1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
    assert c4.check_if_game_finished(0, 0)
    assert c4.check_if_game_finished(0, 1)
    assert c4.check_if_game_finished(0, 2)
    assert c4.check_if_game_finished(0, 3)


def test_check_if_game_finished_horizontal_end_of_row():
    c4 = Connect4()
    c4.board = [[0, 0, 0, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
    assert c4.check_if_game_finished(0, 3)
    assert c4.check_if_game_finished(0, 4)
    assert c4.check_if_game_finished(0, 5)
    assert c4.check_if_game_finished(0, 6)


def test_check_if_game_finished_diagonal_right_end():
    c4 = Connect4()
    c4.board = [[0, 0, 0, 1, -1, -1, -1],
                [0, 0, 0, 0, 1, -1, -1],
                [0, 0, 0, 0, 0, 1, -1],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
    assert c4.check_if_game_finished(0, 3)
    assert c4.check_if_game_finished(1, 4)
    assert c4.check_if_game_finished(2, 5)
    assert c4.check_if_game_finished(3, 6)


def test_check_if_game_finished_diagonal_right_beg():
    c4 = Connect4()
    c4.board = [[1, -1, -1, -1, 0, 0, 0],
                [0, 1, -1, -1, 0, 0, 0],
                [0, 0, 1, -1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
    c4.print_board()
    assert c4.check_if_game_finished(0, 0)
    assert c4.check_if_game_finished(1, 1)
    assert c4.check_if_game_finished(2, 2)
    assert c4.check_if_game_finished(3, 3)


def test_check_if_game_finished_diagonal_left_beg():
    c4 = Connect4()
    c4.board = [[-1, -1, -1, 1, 0, 0, 0],
                [-1, -1, 1, 0, 0, 0, 0],
                [-1, 1, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]
    c4.print_board()
    assert c4.check_if_game_finished(0, 3)
    assert c4.check_if_game_finished(1, 2)
    assert c4.check_if_game_finished(2, 1)
    assert c4.check_if_game_finished(3, 0)
