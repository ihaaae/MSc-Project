from Go_ultimate import Go
from Go_ultimate import GoState
from AI_class import AI

go = Go()
ai = AI()
state0 = GoState()

print(ai.minimax_search(go, state0))
go.actions(state0)