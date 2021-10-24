from sudoku import Game


class BaseSolver:
    def __init__(self, game: Game):
        if game is None or not isinstance(game, Game):
            raise ValueError

    def get_solved_game(self) -> Game:
        raise NotImplementedError


class DfsSolver(BaseSolver):
    def __init__(self, game: Game):
        super().__init__(game)

        board = game.get_board()

        zero_cords = []
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    zero_cords.append((i, j))
        if not zero_cords:
            return

        def dfs(idx: int) -> bool:
            # nonlocal c
            # c += 1
            cord = zero_cords[idx]
            flags = [True for _ in range(9)]
            for i in range(9):
                if board[cord[0]][i] != 0:
                    flags[board[cord[0]][i] - 1] = False
                if board[i][cord[1]] != 0:
                    flags[board[i][cord[1]] - 1] = False
            chunk_cord = ((cord[0] // 3) * 3, (cord[1] // 3) * 3)
            for i in range(chunk_cord[0], chunk_cord[0] + 3):
                for j in range(chunk_cord[1], chunk_cord[1] + 3):
                    if board[i][j] != 0:
                        flags[board[i][j] - 1] = False

            possible_nums = [i + 1 for i, flag in enumerate(flags) if flag]

            if not possible_nums:
                return False
            if idx == len(zero_cords) - 1:
                board[cord[0]][cord[1]] = possible_nums[0]
                return True

            for num in possible_nums:
                board[cord[0]][cord[1]] = num
                if dfs(idx + 1):
                    return True
            board[cord[0]][cord[1]] = 0

            return False

        # c = 0
        dfs(0)
        self.__solved_board = board
        # print('dfs:', c)

    def get_solved_game(self) -> Game:
        return Game(self.__solved_board)


class DancingLinksSolver(BaseSolver):
    def __init__(self, game: Game):
        super().__init__(game)

