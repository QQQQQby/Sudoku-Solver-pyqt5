import copy
from typing import List


class DancingLinks:
    def __init__(self, mat: List[List[int]]):
        self.__check_valid(mat)

        row, col = len(mat), len(mat[0])

        # Initialize nodes
        head = DancingNode()
        col_heads = [DancingNode(col=j) for j in range(col)]
        node_mat = [[DancingNode(row=i, col=j) if mat[i][j] == 1 else None for j in range(col)] for i in range(row)]
        counts = [0 for _ in range(col)]
        for i in range(row):
            for j in range(col):
                if mat[i][j] == 1:
                    counts[j] += 1

        def link_left_right(left: DancingNode, right: DancingNode) -> None:
            left.right = right
            right.left = left

        def link_up_down(up: DancingNode, down: DancingNode) -> None:
            up.down = down
            down.up = up

        # Link all the rows
        link_left_right(head, col_heads[0])
        link_left_right(col_heads[-1], head)
        for j in range(col - 1):
            link_left_right(col_heads[j], col_heads[j + 1])

        for i in range(row):
            j = 0
            while j < col and node_mat[i][j] is None:
                j += 1
            if j == col:
                continue
            first = node_mat[i][j]
            pre = first
            j += 1
            while j < col:
                if node_mat[i][j]:
                    link_left_right(pre, node_mat[i][j])
                    pre = node_mat[i][j]
                j += 1
            link_left_right(pre, first)

        # Link all the columns
        for j in range(col):
            first = col_heads[j]
            pre = first
            for i in range(row):
                if node_mat[i][j]:
                    link_up_down(pre, node_mat[i][j])
                    pre = node_mat[i][j]
            link_up_down(pre, first)

        ans = []

        def remove(p: DancingNode) -> None:
            p.remove()
            counts[p.col] -= 1

        def recover(p: DancingNode) -> None:
            p.recover()
            counts[p.col] += 1

        def dfs_solve() -> bool:
            if head.right is head:
                return True

            p = head.right
            first_col_head = p
            while p is not head:
                if counts[p.col] < counts[first_col_head.col]:
                    first_col_head = p
                p = p.right
            if counts[first_col_head.col] < 1:
                return False

            col_nodes = []
            p = first_col_head.down
            while p is not first_col_head:
                col_nodes.append(p)
                p = p.down
            if not col_nodes:
                return False

            same_row_nodes = []
            for p in col_nodes:
                q = p.right
                curr_row_nodes = []
                same_row_nodes.append(curr_row_nodes)
                while q is not p:
                    curr_row_nodes.append(q)
                    q = q.right

            # Remove nodes
            remove(first_col_head)
            for p in col_nodes:
                remove(p)
            for nodes in same_row_nodes:
                for p in nodes:
                    remove(p)

            for i in range(len(col_nodes)):
                # Remove some nodes if we chose one line
                other_nodes = []
                for p in same_row_nodes[i]:
                    q = col_heads[p.col]
                    r = q.down
                    k = len(other_nodes)
                    while r is not q:
                        other_nodes.append(r)
                        s = r.right
                        while s is not r:
                            other_nodes.append(s)
                            s = s.right
                        r = r.down
                    for j in range(k, len(other_nodes)):
                        remove(other_nodes[j])
                for p in same_row_nodes[i]:
                    remove(col_heads[p.col])

                # Run Depth-First Search
                ans.append(col_nodes[i].row)
                if dfs_solve():
                    return True
                ans.pop()

                # Recover these nodes
                for j in range(len(same_row_nodes[i]) - 1, -1, -1):
                    recover(col_heads[same_row_nodes[i][j].col])
                for j in range(len(other_nodes) - 1, -1, -1):
                    recover(other_nodes[j])

            # Recover nodes
            for i in range(len(same_row_nodes) - 1, -1, -1):
                for j in range(len(same_row_nodes[i]) - 1, -1, -1):
                    recover(same_row_nodes[i][j])
            for i in range(len(col_nodes) - 1, -1, -1):
                recover(col_nodes[i])
            recover(first_col_head)

            # Cannot solve current problem
            return False

        dfs_solve()
        self.__results = ans

    def get_lines(self) -> List[int]:
        return copy.deepcopy(self.__results)

    @staticmethod
    def __check_valid(mat: List[List[int]]) -> None:
        if not mat or not mat[0]:
            raise ValueError
        for line in mat:
            if not line or len(line) != len(mat[0]) or not all(num == 0 or num == 1 for num in line):
                raise ValueError


class DancingNode:
    def __init__(self, row=-1, col=-1):
        self.up = None
        self.down = None
        self.left = None
        self.right = None

        self.row = row
        self.col = col

        self.__up_ori = None
        self.__down_ori = None
        self.__left_ori = None
        self.__right_ori = None

        # self.removed = False

    def remove(self) -> None:
        # assert not self.removed
        self.__up_ori = self.up
        self.__down_ori = self.down
        self.__left_ori = self.left
        self.__right_ori = self.right

        # print('remove:', str(self))
        # assert self.up.down is self
        # assert self.down.up is self
        # assert self.left.right is self
        # assert self.right.left is self

        self.up.down = self.down
        self.down.up = self.up
        self.left.right = self.right
        self.right.left = self.left

        # self.removed = True

    def recover(self) -> None:
        # assert self.removed
        # print('recover:', str(self))

        self.__up_ori.down = self
        self.__down_ori.up = self
        self.__left_ori.right = self
        self.__right_ori.left = self

        # self.removed = False

    def __str__(self):
        return str(self.row) + ', ' + str(self.col)


def test1():
    assert sorted(DancingLinks(
        [[0, 0, 1, 0, 1, 1, 0],
         [1, 0, 0, 1, 0, 0, 1],
         [0, 1, 1, 0, 0, 1, 0],
         [1, 0, 0, 1, 0, 0, 0],
         [0, 1, 0, 0, 0, 0, 1],
         [0, 0, 0, 1, 1, 0, 1]]
    ).get_lines()) == [0, 3, 4]


def test2():
    assert sorted(DancingLinks(
        [[1, 1, 1, 1, 1]]
    ).get_lines()) == [0]


def test3():
    assert sorted(DancingLinks(
        [[1, 0, 0, 0, 0],
         [1, 0, 0, 0, 0]]
    ).get_lines()) == []
