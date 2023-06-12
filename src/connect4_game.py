import logging
import multiprocessing
import os
import pickle as pkl
import time
from datetime import datetime
from itertools import count
from pathlib import Path
from random import shuffle

import pandas as pd
import numpy as np
from tqdm import tqdm

from config import Config
from connect4_board import Connect4Board
from MCTS import MCTS
from MCTS_puct import MCTS_PUCT
from MCTS_rave import MCTS_RAVE


# Has to be separate file than Connect4Board for pickle
from heuristics import CentralHeuristic, PotentialSeriesHeuristic


def play_game():
    tree = load_tree(f"MCTS_10m_6_7_100.pkl")
    board = Connect4Board.create_empty_board(6, 7)
    while True:
        row = int(input("Enter row: "))
        board = board.make_move(row)
        print(board.board)
        if board.terminal:
            break

        for _ in range(100):
            tree.playout(board)
        board: Connect4Board = tree.choose(board)
        print()
        print(board.board)
        if board.terminal:
            break
    print("Game ended:")
    print(board.board)


def self_play(tree: MCTS, config, filename):
    start_time = datetime.now()
    loop_condition = count() if config.time else tqdm(range(config.n_self_play))
    time_exit = False
    games_moves = []
    for game_idx in loop_condition:
        board = Connect4Board.create_empty_board(config.height, config.width)
        game_moves = 0
        while True:
            for _ in range(config.n_rollouts):  # rollout = single game simulation iteration
                tree.playout(board)
            board = tree.choose(board)  # wybierz ruch
            game_moves += 1
            # print(board.board)
            if board.terminal:
                break

            if config.time and (datetime.now() - start_time).total_seconds() / 60 > config.time:
                time_exit = True
                print(f"Breaking because of elapsed more than {config.time}.")
                break
        print(f"{game_idx} game ended.")
        games_moves.append(game_moves)
        if time_exit:
            break

    # Stats
    avg_game_moves = sum(games_moves[:-1]) / game_idx if game_idx > 0 else 0
    logging.info(f"Elapsed {(datetime.now() - start_time).total_seconds()}")
    logging.info(
        f"Total games played: {game_idx}, total_moves: {sum(games_moves)}, avg_game_moves: {avg_game_moves}")

    with open(config.save_dir / f'{filename}.pkl', "wb") as f:
        pkl.dump(tree, f)


def play_2_models(tree1: MCTS, tree2: MCTS, player_order):
    trees = [tree1, tree2]
    total_moves = []
    moves = 0
    board = Connect4Board.create_empty_board(6, 7)
    while True:
        start = time.process_time()
        board = trees[player_order[0]].make_move(board)  # make move with 1
        moves += 1
        if board.terminal: break
        board = trees[player_order[1]].make_move(board)  # make move with 0
        moves += 1
        if board.terminal: break
    total_moves.append(moves)
    if board.winner is not None:  # if board.winner == 1 then first player won
        return player_order[abs(board.winner - 1)]
    else:
        return -1


def load_tree(filename: str):
    save_pkl = Path(__file__).parent / "pickles" / filename
    with open(save_pkl, 'rb') as f:
        tree = pkl.load(f)
    return tree


def compete_2_models(config, tree1, tree2):
    if not os.path.exists(config.stats_path):
        os.mkdir(config.stats_path)

    rng = np.random.default_rng(config.seed)
    winnings = {0: 0, 1: 0, -1: 0} # 0 - tree1, 1 - tree2, -1 - draw
    player_order = [0, 1]
    tree1_moves, tree2_moves = [], []
    tree1_playouts, tree2_playouts = [], []
    for i in tqdm(range(config.n_games)):
        print(f"For i={i}")
        tree1.reset(rng.integers(1000000))
        tree2.reset(rng.integers(1000000))
        result = play_2_models(tree1, tree2, player_order)

        tree1_moves.append(tree1.total_moves)
        tree2_moves.append(tree2.total_moves)
        tree1_playouts.append(tree1.total_playouts)
        tree2_playouts.append(tree2.total_playouts)
        player_order.reverse()
        winnings[result] += 1

    results = {"Tree": [tree1.name, tree2.name], "Wins": [winnings[0], winnings[1]], "Draws": [winnings[-1], winnings[-1]], "Losses": [winnings[1], winnings[0]],
               "Avg_moves": [np.mean(tree1_moves), np.mean(tree2_moves)], "Avg_playouts": [np.mean(tree1_playouts), np.mean(tree2_playouts)],
               "Avg_playouts_per_move": [np.mean(tree1_playouts) / np.mean(tree1_moves), np.mean(tree2_playouts) / np.mean(tree2_moves)]}
    pd.DataFrame(results).to_csv(os.path.join(config.stats_path, f"{tree1.name}_vs_{tree2.name}_c{config.pretty_string()}.csv"), index=False, float_format="%.2f")





if __name__ == "__main__":
    config = Config()
    trees = [MCTS(config, 0, heuristic=PotentialSeriesHeuristic()), MCTS_RAVE(config, 0, heuristic=PotentialSeriesHeuristic()),  MCTS_PUCT(config, 0, heuristic=PotentialSeriesHeuristic()), MCTS(config, 0, heuristic=CentralHeuristic()), MCTS_RAVE(config, 0, heuristic=CentralHeuristic()),  MCTS_PUCT(config, 0, heuristic=CentralHeuristic()), MCTS(config, 0), MCTS_RAVE(config, 0),  MCTS_PUCT(config, 0)]
    all_pairs = []
    for i in range(len(trees)):
        for j in range(i+1, len(trees)):
            all_pairs.append((i, j))
    processes = []
    for pair in all_pairs[24:]:
        process = multiprocessing.Process(target=compete_2_models, args=(config,trees[pair[0]],trees[pair[1]]))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
        process.close()
