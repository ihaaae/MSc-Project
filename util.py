def draw_test(state):
    print(f"{state.idx - 1}:")
    for row in state.board:
        for element in row:
            if element == 0:
                print(". ", end="")
            elif element == 1:
                print("o ", end="")
            elif element == 2:
                print("x ", end="")
            else:
                print("* ", end="")
        print("")