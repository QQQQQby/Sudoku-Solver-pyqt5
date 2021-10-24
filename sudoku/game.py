from typing import List
import copy


class Game:
    def __init__(self, board: List[List[int]]):
        self.__check_valid(board)
        self.__board = copy.deepcopy(board)

    def get_board(self) -> List[List[int]]:
        return copy.deepcopy(self.__board)

    def __str__(self):
        return '\n'.join(' '.join(str(num) for num in line) for line in self.__board)

    @staticmethod
    def __check_valid(board: List[List[int]]) -> None:
        def has_duplicate(nums: List[int]) -> bool:
            return len(nums) - nums.count(0) != len(set(nums) - {0})

        if len(board) != 9:
            raise ValueError
        for i in range(9):
            if len(board[i]) != 9:
                raise ValueError
            for j in range(9):
                if not 0 <= board[i][j] <= 9:
                    raise ValueError
        for i in range(9):
            if has_duplicate(board[i]) or has_duplicate([line[i] for line in board]):
                raise ValueError
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if has_duplicate(board[i][j:j + 3] + board[i + 1][j:j + 3] + board[i + 2][j:j + 3]):
                    raise ValueError
