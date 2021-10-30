from typing import List
import copy


class Game:
    def __init__(self, board: List[List[int]] = None):
        if board is None:
            self.__board = [[0 for _ in range(9)] for _ in range(9)]
        else:
            self.__board = copy.deepcopy(board)
            self.__check_valid()

    def get_board(self) -> List[List[int]]:
        return copy.deepcopy(self.__board)

    def set(self, i: int, j: int, num: int):
        if not (0 <= i < 9 and 0 <= j < 9 and 1 <= num <= 9):
            raise ValueError
        for k in range(9):
            if k != j and self.__board[i][k] == num:
                raise ValueError

            if k != i and self.__board[k][j] == num:
                raise ValueError

        for ii in range((i // 3) * 3, (i // 3 + 1) * 3):
            for jj in range((j // 3) * 3, (j // 3 + 1) * 3):
                if ii != i and jj != j and self.__board[ii][jj] == num:
                    raise ValueError

        self.__board[i][j] = num

    def get(self, i: int, j: int) -> int:
        if not (0 <= i < 9 and 0 <= j < 9):
            raise ValueError
        return self.__board[i][j]

    def __str__(self):
        ans = '┏━━━━┯━━━━┯━━━━┳━━━━┯━━━━┯━━━━┳━━━━┯━━━━┯━━━━┓\n'
        for i in range(9):
            ans += '┃'
            for j in range(9):
                c = ' ' if self.__board[i][j] == 0 else str(self.__board[i][j])
                if (j + 1) % 3 == 0:
                    ans += '  ' + c + ' ┃'
                else:
                    ans += '  ' + c + ' │'
            ans += '\n'
            if i == 8:
                ans += '┗━━━━┷━━━━┷━━━━┻━━━━┷━━━━┷━━━━┻━━━━┷━━━━┷━━━━┛'
            elif (i + 1) % 3 == 0:
                ans += '┣━━━━┿━━━━┿━━━━╋━━━━┿━━━━┿━━━━╋━━━━┿━━━━┿━━━━┫\n'
            else:
                ans += '┠────┼────┼────╂────┼────┼────╂────┼────┼────┨\n'
        return ans

    def __check_valid(self) -> None:
        def has_duplicate(nums: List[int]) -> bool:
            return len(nums) - nums.count(0) != len(set(nums) - {0})

        if len(self.__board) != 9:
            raise ValueError
        for i in range(9):
            if len(self.__board[i]) != 9:
                raise ValueError
            for j in range(9):
                if not 0 <= self.__board[i][j] <= 9:
                    raise ValueError
        for i in range(9):
            if has_duplicate(self.__board[i]) or has_duplicate([line[i] for line in self.__board]):
                raise ValueError
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if has_duplicate(self.__board[i][j:j + 3] +
                                 self.__board[i + 1][j:j + 3] +
                                 self.__board[i + 2][j:j + 3]):
                    raise ValueError
