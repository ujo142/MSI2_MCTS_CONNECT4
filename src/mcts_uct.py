import random
from copy import deepcopy

import numpy as np

from game_finished_checker import check_if_game_finished, get_available_moves, make_move, COMPUTER, get_result


class Node:
    def __init__(self, _board, _parent, col, player=COMPUTER):
        self.children = []
        self.board = deepcopy(_board)
        self.parent = _parent
        self.value = 0
        self.no_visits = 0
        self.is_root = _parent is None
        self.player = player
        # to add function chcecking legal moves from this state
        self.unexpanded_moves = get_available_moves(_board)
        self.column_val = col  # this node was produced by a move in this column

    def visits(self):
        return self.no_visits

    def uct(self):
        if self.visits() == 0:
            return np.infty
        # in numpy log(x) means ln(x)
        return (self.value / self.no_visits) + (np.sqrt(2) * (np.sqrt(np.log(self.parent.no_visits) / self.no_visits)))

    def expand(self, move, state):
        child = Node(col=move, _parent=self, _board=state)
        self.unexpanded_moves.remove(move)
        self.children.append(child)
        return child


class MCTS:
    def __init__(self):
        from time import time
        self.start_time = time()
        self.player_id = COMPUTER

    def check_time(self):
        from time import time
        return (time() - self.start_time) < 5

    def monte_carlo_tree_search(self, root: Node):
        while self.check_time():
            # selection + expansion
            leaf = self.traverse(root, deepcopy(root.board))
            # simulation
            simulation_result = self.rollout(leaf)
            # backpropagation
            self.backpropagate(leaf, simulation_result)
        chosen_node = self.best_child(root)
        return chosen_node.column_val

    def traverse(self, node: Node, mcts_board):
        while node.children != [] and node.unexpanded_moves == [] and self.check_time():
            # selection: select best child
            node = self.best_uct(node)

        if node.unexpanded_moves != []:
            # then expansion: add one new child node
            move = self.pick_random(node.unexpanded_moves)
            mcts_board = make_move(deepcopy(mcts_board), move, self.player_id)
            node = node.expand(move=move, state=mcts_board)
        return node

    def rollout(self, node):
        mcts_board = deepcopy(node.board)
        player = node.player
        while self.non_terminal(mcts_board) and self.check_time():
            available_moves = get_available_moves(mcts_board)
            player *= -1
            mcts_board = make_move(mcts_board, available_moves[random.choice(range(len(available_moves)))],
                                   player=player)
        return self.result(mcts_board)

    def backpropagate(self, node: Node, result):
        if node.is_root:
            return
        node.stats = self.update_stats(node, result)
        self.backpropagate(node.parent, result)

    def best_child(self, node: Node):
        return max(node.children, key=Node.uct)

    def get_random_move(self, board):
        l = get_available_moves(board)
        return self.pick_random(l)

    def pick_random(self, children):
        return children[random.choice(range(len(children)))]

    def best_uct(self, node: Node):
        if len(node.children) == 0:
            return None
        return max(node.children, key=Node.uct)

    def update_stats(self, node, result):
        node.value += result
        node.no_visits += 1

    def non_terminal(self, board):
        return not check_if_game_finished(board) and len(get_available_moves(board)) > 0

    def result(self, board):
        return get_result(board)
