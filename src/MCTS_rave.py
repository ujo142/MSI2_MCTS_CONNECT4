import math
from collections import defaultdict

from src.MCTS import MCTS


class MCTS_RAVE(MCTS):
    def __init__(self, exploration_w = 1, rave_v=10):
        super().__init__(exploration_w)
        self.name = "MCTS_RAVE"
        self.AMAF_Q = defaultdict(int)
        self.RAVE_V = rave_v

    def playout(self, node):
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward, simulated_path = self._simulate(leaf)
        self._backprop(path, simulated_path, reward)

    def _select(self, node):
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._rave_select(node)

    def _simulate(self, node):
        invert_reward = True
        simulated_path = []
        while True:
            if node.terminal:
                reward = node.reward()
                reward = 1 - reward if invert_reward else reward
                return reward, simulated_path
            node = node.make_random_move()
            simulated_path.append(node)
            invert_reward = not invert_reward

    def _backprop(self, path, simulated_path, reward):
        for node in reversed(simulated_path):
            if node in self.children:
                self.N[node] += 1
                self.AMAF_Q[node] += reward
                reward = 1 - reward

        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward

    def _rave_select(self, node):
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        def rave_score(n):
            node_alfa = max(0, (self.RAVE_V - self.N[n]) / self.RAVE_V)
            return node_alfa * self.AMAF_Q.get(n, 0) + (1 - node_alfa) * uct(n)

        return max(self.children[node], key=rave_score)

