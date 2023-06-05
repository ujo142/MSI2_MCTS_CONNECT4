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
        self.unexpanded_moves = get_available_moves(_board)
        self.column_val = col
        self.results = {}  # Dictionary to store MC-RAVE results

    def visits(self):
        return self.no_visits

    def uct(self):
        if self.visits() == 0:
            return np.infty
        return (self.value / self.no_visits) + (1.414 * (np.sqrt(np.log(self.parent.no_visits) / self.no_visits)))

    def expand(self, move, state):
        child = Node(col=move, _parent=self, _board=state)
        self.unexpanded_moves.remove(move)
        self.children.append(child)
        return child

    def update_mc_rave_results(self, move, result):
        if move not in self.results:
            self.results[move] = {"value": 0, "no_visits": 0}
        self.results[move]["value"] += result
        self.results[move]["no_visits"] += 1


class MCTS_MC_RAVE:
    def __init__(self):
        from time import time
        self.start_time = time()
        self.player_id = COMPUTER

    def check_time(self):
        from time import time
        return (time() - self.start_time) < 5

    def monte_carlo_tree_search(self, root: Node):
        while self.check_time():
            leaf = self.traverse(root, deepcopy(root.board))
            simulation_result = self.rollout(leaf)
            self.backpropagate(leaf, simulation_result)
        chosen_node = self.best_child(root)
        return chosen_node.column_val

    def traverse(self, node: Node, mcts_board):
        while node.children != [] and node.unexpanded_moves == [] and self.check_time():
            node = self.best_uct(node)

        if node.unexpanded_moves != []:
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
            move = self.pick_random(available_moves)
            mcts_board = make_move(mcts_board, move, player=player)
            result = self.get_mc_rave_result(node, move)
            if result is None:
                result = self.simulate(mcts_board)
                self.update_mc_rave_results(node, move, result)
        return self.result(mcts_board)

    def backpropagate(self, node: Node, result):
        if node.is_root:
            return
       
        node.value += result
        node.no_visits += 1
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

    def update_mc_rave_results(self, node, move, result):
        node.update_mc_rave_results(move, result)

    def get_mc_rave_result(self, node, move):
        if move in node.results:
            return node.results[move]["value"] / node.results[move]["no_visits"]
        return None

    def non_terminal(self, board):
        return not check_if_game_finished(board) and len(get_available_moves(board)) > 0

    def update_stats(self, node, result):
        node.value += result
        node.no_visits += 1
        
    def simulate(self, board):
        while not check_if_game_finished(board):
            available_moves = get_available_moves(board)
            move = self.pick_random(available_moves)
            board = make_move(board, move, player=-self.player_id)
        return get_result(board)


    def result(self, board):
        return get_result(board)
