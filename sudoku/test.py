from sudoku import Game, DfsSolver

DefaultSolver = DfsSolver


def test1():
    game = Game([[7, 0, 0, 0, 2, 0, 6, 0, 0],
                 [1, 0, 0, 0, 0, 6, 5, 0, 0],
                 [0, 5, 0, 3, 0, 7, 9, 0, 0],

                 [0, 6, 3, 0, 0, 0, 0, 5, 0],
                 [0, 0, 1, 0, 4, 0, 7, 0, 0],
                 [0, 9, 0, 6, 0, 0, 8, 2, 0],

                 [0, 0, 8, 1, 0, 2, 0, 7, 0],
                 [0, 0, 6, 5, 0, 0, 0, 0, 9],
                 [0, 0, 5, 0, 9, 0, 0, 0, 8]])
    solver = DefaultSolver(game)
    print()
    print(game)
    print()
    print(solver.get_solved_game())


def test2():
    game = Game([[8, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 3, 6, 0, 0, 0, 0, 0],
                 [0, 7, 0, 0, 9, 0, 2, 0, 0],

                 [0, 5, 0, 0, 0, 7, 0, 0, 0],
                 [0, 0, 0, 0, 4, 5, 7, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 3, 0],

                 [0, 0, 1, 0, 0, 0, 0, 6, 8],
                 [0, 0, 8, 5, 0, 0, 0, 1, 0],
                 [0, 9, 0, 0, 0, 0, 4, 0, 0]])
    solver = DefaultSolver(game)
    print()
    print(game)
    print()
    print(solver.get_solved_game())


def test3():
    game = Game([[0, 0, 5, 3, 0, 0, 0, 0, 0],
                 [8, 0, 0, 0, 0, 0, 0, 2, 0],
                 [0, 7, 0, 0, 1, 0, 5, 0, 0],

                 [4, 0, 0, 0, 0, 5, 3, 0, 0],
                 [0, 1, 0, 0, 7, 0, 0, 0, 6],
                 [0, 0, 3, 2, 0, 0, 0, 8, 0],

                 [0, 6, 0, 5, 0, 0, 0, 0, 9],
                 [0, 0, 4, 0, 0, 0, 0, 3, 0],
                 [0, 0, 0, 0, 0, 9, 7, 0, 0]])
    solver = DefaultSolver(game)
    print()
    print(game)
    print()
    print(solver.get_solved_game())


def test4():
    game = Game([[0, 0, 1, 2, 0, 0, 0, 0, 9],
                 [0, 9, 2, 1, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 1, 2, 0],

                 [0, 0, 0, 0, 0, 0, 0, 1, 0],
                 [9, 0, 0, 0, 1, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 9, 0],

                 [0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 0, 0, 0, 1, 0, 0, 0],
                 [1, 0, 0, 0, 0, 0, 0, 0, 0]])
    solver = DefaultSolver(game)
    print()
    print(game)
    print()
    print(solver.get_solved_game())


def test5():
    game = Game([[0, 6, 0, 5, 0, 0, 0, 0, 0],
                 [0, 0, 0, 8, 0, 0, 4, 0, 0],
                 [0, 0, 9, 0, 0, 0, 0, 6, 0],

                 [0, 0, 0, 0, 0, 0, 0, 4, 0],
                 [0, 0, 2, 0, 0, 0, 0, 9, 7],
                 [5, 0, 0, 3, 0, 0, 0, 0, 0],

                 [0, 0, 4, 0, 0, 9, 0, 0, 0],
                 [8, 0, 0, 0, 0, 0, 5, 0, 0],
                 [0, 0, 0, 0, 0, 7, 0, 0, 0]])
    solver = DefaultSolver(game)
    print()
    print(game)
    print()
    print(solver.get_solved_game())
