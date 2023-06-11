import logging
import pickle as pkl
from datetime import datetime
from itertools import count
from pathlib import Path
from random import shuffle

import numpy as np
from tqdm import tqdm

from config import SelfPlayConfig
from connect4_board import Connect4Board
from MCTS import MCTS
from src.MCTS_rave import MCTS_RAVE


# Has to be separate file than Connect4Board for pickle
from src.heuristics import CentralHeuristic, PotentialSeriesHeuristic


def play_game():
    tree = load_tree(f"MCTS_1m_6_7_100.pkl")
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


def self_play(tree: MCTS, config: SelfPlayConfig, filename):
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


def play_2_models(tree1: MCTS, tree2: MCTS, n_games: int = 100):
    start_time = datetime.now()
    player_order = [0, 1]
    trees = [tree1, tree2]
    winnings = {0: 0, 1: 0, -1: 0}  # 0 tree1, 1 tree2, -1 draw
    total_moves = []
    for _ in tqdm(range(n_games)):
        moves = 0
        board = Connect4Board.create_empty_board(6, 7)
        shuffle(player_order)
        while True:
            board = trees[player_order[0]].choose(board)  # make move with 1
            moves += 1
            if board.terminal: break
            board = trees[player_order[1]].choose(board)  # make move with 0
            moves += 1
            if board.terminal: break
        total_moves.append(moves)
        if board.winner is not None:  # if board.winner == 1 then first player won
            winnings[player_order[abs(board.winner - 1)]] += 1
        else:
            winnings[-1] += 1
    end_time = datetime.now()

    winning_perc = {k: v / n_games for k, v in winnings.items()}
    print(winning_perc)
    print(winnings)
    print(
        f"Average {np.average(total_moves)}, std: {np.std(total_moves)}, min: {np.min(total_moves)}, max:{np.max(total_moves)}")
    print(f"Elapsed {(end_time - start_time).total_seconds()}")


def load_tree(filename: str):
    save_pkl = Path(__file__).parent / "pickles" / filename
    with open(save_pkl, 'rb') as f:
        tree = pkl.load(f)
    return tree


def compete_2_models():
    ## Two trees play
    for i in [1]:
        print(f"For i={i}")
        tree1 = load_tree(f"MCTS_RAVE_{i}m_6_7_100.pkl")
        tree2 = load_tree(f"MCTS_RAVE_central_{i}m_6_7_100.pkl")
        # tree2 = load_tree(f"mcts_rave_{i}m_6_7_100.pkl")
        play_2_models(tree1, tree2, 20000)


def train_one_tree():
    config = SelfPlayConfig()
    tree = MCTS_RAVE()  # MCTS # MCTS_AMAF() # MCTS_RAVE()

    filenames = f'{tree.name}_{config.pretty_string()}'
    config.log_dir.mkdir(exist_ok=True)
    config.save_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.FileHandler(config.log_dir / f'{filenames}.log'),
            logging.StreamHandler()
        ]
    )

    self_play(tree, config, filenames)


if __name__ == "__main__":
    #train_one_tree()
    compete_2_models()
    #play_game()
