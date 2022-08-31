import numpy as np

class AI:
    def test(self):
        print("test")

    def minimax_search(self, game, state):
        move = max(game.actions(state), key=lambda a: self.min_value(game, game.result(game, a)))
        value = self.min_value(game, game.result(game, move))
        print(f"minimax_search: value: {value} move: {move}")
        return move

    def max_value(self, game, state):
        if game.is_terminal(state):
            return game.utility(state)
        else:
            v = -np.inf
            for a in game.actions(state):
                v = max(v, self.min_value(game, game.result(state, a)))
            return v

    def min_value(self, game, state):
        if game.is_terminal(state):
            return game.utility(state)
        else:
            v = np.inf
            for a in game.actions(state):
                v = min(v, self.max_value(game, game.result(state, a)))
            return v
