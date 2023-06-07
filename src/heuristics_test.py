import unittest

import numpy as np

from src.heuristics import CentralHeuristic, PotentialSeriesHeuristic

BOARD_SIZE = (6, 7)

class TestCentralHeuristic(unittest.TestCase):
    heuristic = CentralHeuristic()

    def test_full_board(self):
        board = [[0, 0, 0, 1, 0, 1, 0],
                 [1, 1, 0, 0, 1, 1, 0],
                 [1, 0, 1, 1, 0, 0, 0],
                 [0, 1, 0, 1, 0, 1, 1],
                 [0, 1, 0, 1, 0, 1, 0],
                 [0, 1, 1, 0, 1, 1, 1]]
        self.assertEqual(self.heuristic.evaluate(board, 0), 10)
        self.assertEqual(self.heuristic.evaluate(board, 1), 8)

    def test_empty_board(self):
        board = np.full(BOARD_SIZE, 2)
        self.assertEqual(self.heuristic.evaluate(board, 0), 0)
        self.assertEqual(self.heuristic.evaluate(board, 1), 0)

    def test_full_one_board(self):
        board = np.full(BOARD_SIZE, 1)
        self.assertEqual(self.heuristic.evaluate(board, 0), 0)
        self.assertEqual(self.heuristic.evaluate(board, 1), 18)

    def test_full_zero_board(self):
        board = np.full(BOARD_SIZE, 0)
        self.assertEqual(self.heuristic.evaluate(board, 0), 18)
        self.assertEqual(self.heuristic.evaluate(board, 1), 0)


class TestPotentialSeriesHeurisitc(unittest.TestCase):
    heuristic = PotentialSeriesHeuristic()
    def test_full_board(self):
        board = np.array([[0, 0, 0, 1, 0, 1, 0],
                         [1, 1, 0, 0, 1, 1, 0],
                         [1, 0, 1, 1, 0, 0, 0],
                         [0, 1, 0, 1, 0, 1, 1],
                         [0, 1, 0, 1, 0, 1, 0],
                         [0, 1, 1, 0, 1, 1, 1]])
        self.assertEqual(self.heuristic.evaluate(board, 0), 0)
        self.assertEqual(self.heuristic.evaluate(board, 1), 0)

    def test_empty_board(self):
        board = np.full(BOARD_SIZE, 2)
        self.assertEqual(self.heuristic.evaluate(board, 0), 69)
        self.assertEqual(self.heuristic.evaluate(board, 1), 69)

if __name__ == '__main__':
    unittest.main()
