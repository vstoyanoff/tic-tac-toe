from typing import List
import pickle
import numpy as np


class Player:
    def __init__(
        self,
        name: str,
        is_human: bool = False,
        random_action_rate: float = 0.3,
        learning_rate: float = 0.2,
        decay_gamma: float = 0.9,
        policy_file=None,
    ):
        self.name = name
        self.is_human = is_human
        self.moves = []
        self.moves_value = {}
        self.random_action_rate = random_action_rate
        self.learning_rate = learning_rate
        self.decay_gamma = decay_gamma

        if policy_file:
            self.load_policy(policy_file)

    def set_symbol(self, symbol):
        self.symbol = symbol

    def get_symbol(self) -> int:
        return self.symbol

    def _get_board_value(self, board: np.ndarray) -> str:
        return str(board.reshape(3 * 3))

    def record_board_value(self, board: np.ndarray):
        self.moves.append(self._get_board_value(board))

    def reset(self):
        self.moves = []

    def _get_free_cell(self, cells: np.ndarray, symbol: int):
        idx = None
        if np.count_nonzero(cells == symbol) == 2 and np.count_nonzero(cells == 0) == 1:
            idx = np.where(cells == 0)[0][0]
        return idx

    def _determine_move(self, board):
        opponent_symbol = -self.symbol
        opponent_cells = np.argwhere(board == opponent_symbol)
        cell = None

        # If the opponent hasn't played or has played 1 move
        if len(opponent_cells) < 2:
            return None

        # Iterate through rows and cols
        # and check if there is a possible winning move
        # or there is a possibility that the opponent will win
        for i in range(3):
            row = board[i, :]
            col = board[:, i]

            # check if the opponent can win
            if self._get_free_cell(row, opponent_symbol) is not None:
                cell = [i, self._get_free_cell(row, opponent_symbol)]

            if self._get_free_cell(col, opponent_symbol) is not None:
                cell = [self._get_free_cell(col, opponent_symbol), i]

            # check if the player can win
            if self._get_free_cell(row, self.symbol) is not None:
                cell = [i, self._get_free_cell(row, self.symbol)]

            if self._get_free_cell(col, self.symbol) is not None:
                cell = [self._get_free_cell(col, self.symbol), i]

        # Check the diagonals as well
        diag_1_idx = [(0, 0), (1, 1), (2, 2)]
        diag_2_idx = [(0, 2), (1, 1), (2, 0)]
        diag_1 = [board[i] for i in diag_1_idx]
        diag_2 = [board[i] for i in diag_2_idx]
        diag_1 = np.array(diag_1)
        diag_2 = np.array(diag_2)

        d1_l = self._get_free_cell(diag_1, opponent_symbol)
        d2_l = self._get_free_cell(diag_2, opponent_symbol)
        d1_w = self._get_free_cell(diag_1, self.symbol)
        d2_w = self._get_free_cell(diag_2, self.symbol)

        if d1_l is not None:
            cell = diag_1_idx[d1_l]

        if d2_l is not None:
            cell = diag_2_idx[d2_l]

        if d1_w is not None:
            cell = diag_1_idx[d1_w]

        if d2_w is not None:
            cell = diag_2_idx[d2_w]

        return cell

    def _choose_algorithmic(
        self, board: np.ndarray, is_training: bool = False
    ) -> List[int]:
        empty_cells = np.argwhere(board == 0)
        # random action
        if np.random.uniform(0, 1) <= self.random_action_rate and is_training:
            idx = np.random.choice(len(empty_cells))
            action = empty_cells[idx]
        else:  # get the most valuable action
            max_value = float("-inf")
            for cell in empty_cells:
                board_copy = board.copy()
                board_copy[cell[0], cell[1]] = self.symbol
                board_copy_value = self._get_board_value(board_copy)
                value = self.moves_value.get(board_copy_value) or 0
                if value >= max_value:
                    max_value = value
                    action = cell

        return action

    def choose(self, board: np.ndarray, is_training: bool = False) -> List[int]:
        if self._determine_move(board):
            return self._determine_move(board)
        else:
            return self._choose_algorithmic(board, is_training)

    def compute_moves_values(self, reward):
        for move in reversed(self.moves):
            if self.moves_value.get(move) is None:
                self.moves_value[move] = 0
            self.moves_value[move] += self.learning_rate * (
                self.decay_gamma * reward - self.moves_value[move]
            )
            reward = self.moves_value[move]
        self.moves = []

    def save_policy(self):
        file = open(f"policy_{self.name}", "wb")
        pickle.dump(self.moves_value, file)
        file.close()

    def load_policy(self, file):
        try:
            file = open(file, "rb")
            self.moves_value = pickle.load(file)
            file.close()
        except Exception:
            print(
                "Could not load the specified policy file. Proceeding with clean policy states"
            )
            pass
