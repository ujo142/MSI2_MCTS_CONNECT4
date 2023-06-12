import math
from collections import defaultdict

import numpy as np
import time

class MCTS:
    def __init__(self, config, rng_seed, exploration_weight=math.sqrt(2), heuristic=None):
        self.exploration_weight = exploration_weight
        self.name = f"MCTS" if heuristic is None else f"MCTS_{heuristic.name}"

        self.Q = defaultdict(int)
        self.N = defaultdict(int)
        self.children = dict()
        self.heuristic = heuristic
        self.rng = np.random.default_rng(rng_seed)
        self.max_playouts = config.max_rollouts
        self.time_rollouts = config.time_rollouts
        self.total_playouts = 0
        self.total_moves = 0

    def reset(self, rng_seed):
        self.Q.clear()
        self.N.clear()
        self.children.clear()
        self.total_playouts = 0
        self.total_moves = 0
        self.rng = np.random.default_rng(rng_seed)
    def make_move(self, node):
        self.total_moves += 1
        start = time.process_time()
        for _ in range(self.max_playouts):
            self.playout(node)
            self.total_playouts += 1
            if (time.process_time() - start) > self.time_rollouts:
                break
        return self.choose(node)

    def get_stats(self):
        return f"Total moves: {self.total_moves}, total playouts: {self.total_playouts}, playouts per move: {self.total_playouts / self.total_moves}"

    def choose(self, node):
        assert not node.terminal, f"Choose was called on terminal node {node}"

        if node not in self.children:
            return node.make_random_move(self.rng)

        def score(n):
            if self.N[n] == 0:
                return -math.inf
            heuristic_value = self.heuristic.evaluate(n.board) if self.heuristic is not None else 0
            return (self.Q[n] + heuristic_value) / self.N[n]

        return max(self.children[node], key=score)

    def playout(self, node):
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backprop(path, reward)


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
            node = self._uct_select(node)

    def _expand(self, node):
        if node in self.children:
            return
        self.children[node] = node.find_children()

    def _simulate(self, node):
        invert_reward = True
        while True:
            if node.terminal:
                reward = node.reward()
                reward = 1 - reward if invert_reward else reward
                return reward
            node = node.make_random_move(self.rng)
            invert_reward = not invert_reward

    def _backprop(self, path, reward):
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward

    def _uct_select(self, node):
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])
        def uct(n):
            heuristic_val = self.heuristic.evaluate(n.board) if self.heuristic is not None else 0
            return (self.Q[n] + heuristic_val) / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)


