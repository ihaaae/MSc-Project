from AI_class import AI

class Egame:
    def __init__(self):
        pass

    def actions(self, state):
        if state == 'A':
            return ["a1", "a2", "a3"]
        elif state == 'B':
            return ["b1", "b2", "b3"]
        elif state == 'C':
            return ["c1", "c2", "c3"]
        elif state == 'D':
            return ["d1", "d2", "d3"]
        else:
            return []

    def result(self, state, action):
        if state == "A":
            if action == "a1":
                return "B"
            elif action == "a2":
                return "C"
            elif action == "a3":
                return "D"
        elif state == "B":
            if action == "b1":
                return 3
            elif action == "b2":
                return 12
            elif action == "b3":
                return 8
        elif state == "C":
            if action == "c1":
                return 2
            elif action == "c2":
                return 4
            elif action == "c3":
                return 6
        elif state == "D":
            if action == "d1":
                return 14
            elif action == "d2":
                return 5
            elif action == "d3":
                return 2

    def to_move(self, state):
        if state == "B" or state == "C" or state == "D":
            return 2
        else:
            return 1

    def is_terminal(self, state):
        return isinstance(state, int)

    def utility(self, state: int) -> int:
        return state

egame = Egame()
ai = AI()
print(ai.minimax_search(egame, "A"))