from typing import List

from sudoku import Game
from utils import DancingLinksX


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


class DancingLinksXSolver(BaseSolver):
    def __init__(self, game: Game):
        super().__init__(game)

        def calc_line(i: int, j: int, num: int) -> List[int]:
            ans = [0 for _ in range(324)]
            for idx in [i * 9 + j, i * 9 + num - 1 + 81, j * 9 + num - 1 + 162,
                        ((i // 3) * 3 + (j // 3)) * 9 + num - 1 + 243]:
                ans[idx] = 1
            return ans

        mat = []
        pos_nums = []
        board = game.get_board()
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for k in range(1, 10):
                        mat.append(calc_line(i, j, k))
                        pos_nums.append((i, j, k))
                else:
                    mat.append(calc_line(i, j, board[i][j]))
                    pos_nums.append((i, j, board[i][j]))

        lines = DancingLinksX(mat).get_lines()
        if len(lines) != 81:
            raise ValueError

        board = [[0 for _ in range(9)] for _ in range(9)]
        for i in lines:
            board[pos_nums[i][0]][pos_nums[i][1]] = pos_nums[i][2]
        self.__solved_board = board

    def get_solved_game(self) -> Game:
        return Game(self.__solved_board)
