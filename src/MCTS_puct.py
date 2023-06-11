import math
from collections import defaultdict

from src.MCTS import MCTS


class MCTS_PUCT(MCTS):
    def __init__(self, exploration_weight=1, bias_weight=1, heuristic=None):
        super().__init__(exploration_weight, heuristic)
        self.bias_weight = bias_weight
        self.name = "MCTS_PUCT"
        if heuristic is not None:
            self.name += "_" + heuristic.name
        self.N_bias = defaultdict(int)  # Licznik wzmocnienia

    def _backprop(self, path, reward):
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            self.N_bias[node] += 1  # Zwiększenie licznika wzmocnienia
            reward = 1 - reward

    def _uct_select(self, node):
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            heuristic_val = self.heuristic.evaluate(n.board) if self.heuristic is not None else 0
            return ((self.Q[n] + heuristic_val) / self.N[n]) + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]) - self.bias_weight/self.N_bias[n] * max(1, math.sqrt(log_N_vertex) / self.N[n])
            

        return max(self.children[node], key=uct)
