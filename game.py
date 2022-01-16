import random
import numpy as np

from player import Player

ROWS = {1: "A", 2: "B", 3: "C"}


class Game:
    def __init__(self, player_1: Player, player_2: Player):
        self.board = np.zeros((3, 3))
        self.player_1 = player_1
        self.player_2 = player_2
        # assign first player randomly
        random_player = random.choice([-1, 1])
        player_1.set_symbol(random_player)
        player_2.set_symbol(-random_player)

    def _get_symbol(self, cell: int):
        if cell == 1:
            return "X"
        if cell == -1:
            return "O"
        return None

    def _draw_board(self):
        if self.board.shape != (3, 3):
            raise Exception("The shape needs to be exactly 3x3")

        color_start = "\033[1m"
        color_end = "\033[0m"

        # Top part
        print("    1   2   3 ")
        print("  +---+---+---+")

        for i in range(3):
            print(f"{ROWS[i + 1]} |", end="")

            for j in range(3):
                cell = self._get_symbol(self.board[i, j]) or " "

                # Coloring
                if cell == "X":
                    color_start += "\033[94m"
                elif cell == "O":
                    color_start += "\033[93m"

                print(f"{color_start} {cell} {color_end}|", end="")

            print("\n  +---+---+---+")

    def _reset(self):
        self.board = np.zeros((3, 3))

    def _check_winner(self):
        cells = self.board
        winner = None

        # Check rows and columns
        for i in range(3):
            if np.all(cells[i, :] == cells[i, 0]) and cells[i, 0] != 0:
                winner = cells[i, 0]
            if np.all(cells[:, i] == cells[0, i]) and cells[0, i] != 0:
                winner = cells[0, i]

        # Check diagonals
        if cells[0, 0] == cells[1, 1] == cells[2, 2] != 0:
            winner = cells[0, 0]

        if cells[0, 2] == cells[1, 1] == cells[2, 0] != 0:
            winner = cells[0, 2]

        # tie game
        if np.all(cells) and winner is None:
            winner = 0

        # Rewards
        if winner is not None:
            if winner == 0:
                p1_reward = 0.3
                p2_reward = 0.1
            elif winner == self.player_1.get_symbol():
                p1_reward = 1
                p2_reward = 0
            elif winner == self.player_2.get_symbol():
                p1_reward = 0
                p2_reward = 1
            self.player_1.compute_moves_values(p1_reward)
            self.player_2.compute_moves_values(p2_reward)

        return winner

    def _play_move(self, cell, player: Player):
        symbol = player.get_symbol()

        if isinstance(cell[0], str):
            row = int(list(ROWS.values()).index(cell[0]))
        else:
            row = cell[0]
        col = cell[1]

        if player.is_human:
            col -= 1

        if self.board[row, col] != 0:
            raise Exception("This cell is already taken")

        self.board[row, col] = symbol

    def train(self, rounds: int = 100):
        for i in range(rounds):
            if i % 100 == 0:
                print(f"Rounds {i}")
            while self._check_winner() is None:
                player_1_move = self.player_1.choose(self.board, is_training=True)
                self._play_move(player_1_move, self.player_1)
                self.player_1.record_board_value(self.board)

                if self._check_winner() is not None:
                    self._reset()
                    break

                player_2_move = self.player_2.choose(self.board, is_training=True)
                self._play_move(player_2_move, self.player_2)
                self.player_2.record_board_value(self.board)

                if self._check_winner() is not None:
                    self._reset()
                    break
        # Save the states values after the training ends
        self.player_1.save_policy()
        self.player_2.save_policy()

    def play(self):
        print("Starting new game")
        player_on_move = (
            self.player_1 if self.player_1.get_symbol() == 1 else self.player_2
        )
        symbol_on_move = player_on_move.get_symbol()

        while self._check_winner() is None:
            if player_on_move.is_human:
                self._draw_board()
                cell = input(f"{player_on_move.name} - Select cell: ")
            else:
                cell = player_on_move.choose(self.board)

            try:
                self._play_move((cell[0], int(cell[1])), player_on_move)
                player_on_move = (
                    self.player_1
                    if self.player_1.get_symbol() != symbol_on_move
                    else self.player_2
                )
                symbol_on_move = -symbol_on_move
            except Exception as e:
                print(e)
                continue

        self._draw_board()
        self._reset()
