import numpy as np

class Gobblet:
    def __init__(self):
        self.board = np.zeros((9, 2), dtype=int)
        self.reserve = {
            1: [2, 2, 2],
            -1: [2, 2, 2]
        }
        self.current_player = 1

    def reset(self):
        self.board = np.zeros((9, 2), dtype=int)
        self.reserve = {1: [2, 2, 2], -1: [2, 2, 2]}
        self.current_player = 1
        return self.get_state()

    def get_state(self):
        return self.board.flatten()

    def get_valid_actions(self):
        valid = []
        player = self.current_player
        color = 1 if player == 1 else 2
        for cell in range(9):
            top_size = self.board[cell, 0]
            for size in [1, 2, 3]:
                if self.reserve[player][size - 1] > 0:
                    if top_size < size:
                        valid.append(cell * 3 + (size - 1))
        return valid

    def step(self, action):
        cell = action // 3
        size = action % 3 + 1
        player = self.current_player
        color = 1 if player == 1 else 2

        if self.board[cell, 0] >= size or self.reserve[player][size - 1] <= 0:
            raise ValueError(f"Invalid move. State: {self.board.T},"
                             f"Cell: {cell}, Size: {size}, "
                             f"Valid Actions: {self.get_valid_actions()}, "
                             f"Action: {action}, Player: {self.current_player}")

        self.board[cell] = [size, color]
        self.reserve[player][size - 1] -= 1

        done, winner = self.check_winner()
        reward = 0
        if done:
            if winner == player:
                reward = 1
            elif winner == -player:
                reward = -1
            else:
                reward = 0.5

        self.current_player *= -1
        return self.get_state(), reward, done

    def check_winner(self):
        b = self.board
        colors = b[:, 1]
        lines = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for line in lines:
            c0, c1, c2 = colors[line[0]], colors[line[1]], colors[line[2]]
            if c0 != 0 and c0 == c1 == c2:
                winner = 1 if c0 == 1 else -1
                return True, winner

        total_used = sum(2 - r for r in self.reserve[1]) + sum(2 - r for r in self.reserve[-1])
        if total_used == 12:
            return True, 0

        return False, None