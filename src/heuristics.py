from abc import ABC, abstractmethod

import numpy as np


class Heuristic(ABC):
    @abstractmethod
    def evaluate(self, board, player):
        pass

class CentralHeuristic(Heuristic):
    def evaluate(self, board, player):
        central_columns = [2, 3, 4]
        score = 0
        for row in range(6):
            for col in range(7):
                if col in central_columns and board[row][col] == player:
                    score += 1
        return score


class PotentialSeriesHeuristic(Heuristic):
    def evaluate(self, board, player):
        potential_series = 0
        rows = 6
        cols = 7

        def player_or_empty(subboard):
            return not np.any(subboard == (1 - player))

        # Sprawdzanie serii w poziomie
        for row in range(rows):
            for col in range(cols - 3):
                subboard = board[row, col:col+4]
                if player_or_empty(subboard):
                    potential_series += 1
        pass
        # Sprawdzanie serii w pionie
        for row in range(rows - 3):
            for col in range(cols):
                subboard = board[row:row+4, col]
                if player_or_empty(subboard):
                    potential_series += 1

        # Sprawdzanie serii po skosie '/'
        for row in range(rows - 3):
            for col in range(cols - 3):
                subboard = np.array([board[row][col], board[row+1][col+1], board[row+2][col+2], board[row+3][col+3]])
                if player_or_empty(subboard):
                    potential_series += 1

        for row in range(rows - 3):
            for col in range(3, cols):
                subboard = np.array([board[row][col], board[row + 1][col - 1], board[row + 2][col - 2], board[row + 3][col - 3]])
                if player_or_empty(subboard):
                    potential_series += 1

        return potential_series

