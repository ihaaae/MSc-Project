import numpy as np
import enum


class Point(enum.Enum):
    black = 1
    white = 2
    empty = 0
    black_eye = -1
    white_eye = -2


boardSize = 4

# board is [Matrix of point], a boardsize * boardsize size matrix
# point is
black = 1
white = 2
empty = 0


def neighbors(x: int, y: int) -> list[tuple[int, int]]:
    def belong_board(xn: int, yn: int) -> bool:
        global boardSize
        return xn % boardSize == xn and yn % boardSize == yn

    nxs = [0, 0, -1, 1]
    nys = [-1, 1, 0, 0]
    return [(x + nxs[i], y + nys[i]) for i in range(4) if belong_board(x + nxs[i], y + nys[i])]


class Liberty:
    def __init__(self):
        self.items = [[]]

    def reduceliberty(self, w: int, x: int, y: int):
        for es in self.items[w]:
            if es[0] == x and es[1] == y:
                self.items[w].remove(es)

    def mergeliberty(self, index_of_worms_one, index_of_worms_current):
        self.items[index_of_worms_current] += self.items[index_of_worms_one]

    def __getitem__(self, key):
        return self.items[key]

    def append(self, new_liberty):
        self.items.append(new_liberty)

    def add_liberty_by_wormindex(self, wormindex, posn):
        self.items[wormindex].append(posn)


class GoState:
    def __init__(self):
        self.board = np.zeros((boardSize, boardSize), dtype=int)
        self.worms = np.zeros((boardSize, boardSize), dtype=int)
        self.liberties = Liberty()
        self.neighbors_current_stone = []
        self.enemies_current_stone = []
        self.idx = 1


class Go:
    def result(self, state: GoState, action: tuple[int, int]) -> GoState:
        self.turn = 2 - state.idx % 2

        x = action[0]
        y = action[1]
        if state.board[x, y] == empty:
            state.board[x, y] = self.turn

        state = self.update_enemy_liberty(state, action)

        state = self.capture_enemy(state)

        state = self.update_worm(state, action)

        state = self.update_self_liberty(state, action)

        state = self.capture_self(state, action)

        state = self.change_turn(state)

        return state

    @staticmethod
    def actions(state: GoState) -> list[tuple[int, int]]:
        board = state.board
        actions = []
        for i in range(boardSize):
            for j in range(boardSize):
                if board[i][j] == empty:
                    actions.append((i, j))

        return actions

    @staticmethod
    def utility(state: GoState) -> int:
        def reach_black(point: tuple[int, int]) -> bool:
            for element in neighbors(point[0], point[1]):
                p = state.board[element[0], element[1]]
                if p == black or p == -1:
                    return True
            return False

        def reach_white(point: tuple[int, int]) -> bool:
            for element in neighbors(point[0], point[1]):
                p = state.board[element[0], element[1]]
                if p == white or p == -2:
                    return True
            return False

        black_score = 0
        white_score = 0
        for i in range(boardSize):
            for j in range(boardSize):
                if state.board[i, j] == 1 or state.board[i, j] == -1:
                    black_score += 1
                elif state.board[i, j] == 2 or state.board[i, j] == -2:
                    white_score += 1
                else:
                    if reach_black((i, j)) and not reach_white((i, j)):
                        black_score += 1
                    elif not reach_black((i, j)) and reach_white((i, j)):
                        white_score += 1
        return black_score - white_score

    @staticmethod
    def is_terminal(state: GoState) -> bool:
        return state.idx >= boardSize * 2

    def update_enemy_liberty(self, state: GoState, action: tuple[int, int]) -> GoState:
        x = action[0]
        y = action[1]
        state.enemies_current_stone = self.nearby_enemy_worms(state, action)

        for enemy_worm in state.enemies_current_stone:
            state.liberties.reduceliberty(enemy_worm, x, y)

        return state

    def capture_enemy(self, state: GoState) -> GoState:
        for enemy_worm in state.enemies_current_stone:
            if len(state.liberties[enemy_worm]) == 0:
                self.clear_worm(state, enemy_worm)

        return state

    def update_worm(self, state: GoState, action: tuple[int, int]) -> GoState:
        def transformworm(nw):
            state.worms[state.worms == nw] = state.idx

        x = action[0]
        y = action[1]
        state.worms[x][y] = state.idx

        state.neighbors_current_stone = self.nearby_own_worms(state, action)

        for neighbor_worm in state.neighbors_current_stone:
            transformworm(neighbor_worm)

        return state

    def update_self_liberty(self, state, action):
        x = action[0]
        y = action[1]
        state.liberties.append([(n[0], n[1]) for n in neighbors(x, y)
                                if state.board[n[0]][n[1]] == empty or state.board[n[0]][n[1]] == -self.turn])
        for neighbor_worm in state.neighbors_current_stone:
            state.liberties.reduceliberty(neighbor_worm, x, y)
            state.liberties.mergeliberty(neighbor_worm, state.idx)

        return state

    def capture_self(self, state, action):
        x = action[0]
        y = action[1]
        if len(state.liberties[state.worms[x][y]]) == 0:
            self.clear_worm(state, state.worms[x][y])

        return state

    @staticmethod
    def nearby_enemy_worms(state, posn):
        x = posn[0]
        y = posn[1]
        return [state.worms[n[0]][n[1]] for n in neighbors(x, y)
                if state.worms[n[0]][n[1]] % 2 == (state.board[x][y] + 1) % 2 and state.worms[n[0]][n[1]] != 0]

    @staticmethod
    def nearby_own_worms(state, action):
        x = action[0]
        y = action[1]
        return [state.worms[n[0]][n[1]] for n in neighbors(x, y)
                if state.worms[n[0]][n[1]] % 2 == state.board[x][y] % 2 and state.worms[n[0]][n[1]] != 0]

    def clear_worm(self, state, target_worm: int):
        for i in range(boardSize):
            for j in range(boardSize):
                if state.worms[i][j] == target_worm:
                    for worm in self.nearby_enemy_worms(state, (i, j)):
                        if (i, j) not in state.liberties[worm]:
                            state.liberties.add_liberty_by_wormindex(worm, (i, j))
                    state.worms[i][j] = empty
                    state.board[i][j] = -self.turn

        return state

    @staticmethod
    def change_turn(state):
        state.idx += 1
        return state

    def test(self, state, action):
        return self.result(state, action)
