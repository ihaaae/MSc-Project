from Go_ultimate import Go
from Go_ultimate import GoState
from AI_class import AI

go = Go()
ai = AI()
state0 = GoState()

go.actions(state0)
print(ai.minimax_search(go, state0))
go.actions(state0)