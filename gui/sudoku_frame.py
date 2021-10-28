from PyQt5.QtCore import Qt, QEvent, QRect
from PyQt5.QtGui import QPaintEvent, QPainter, QMouseEvent, QPen
from PyQt5.QtWidgets import QFrame

from sudoku import Game


class SudokuFrame(QFrame):
    BORDER_WIDTH = 7
    NORMAL_LINE_WIDTH = 3

    def __init__(self, game: Game, solved_game: Game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = game
        self.solved_game = solved_game

        self.row_pressed = -1
        self.col_pressed = -1
        self.x = -1
        self.y = -1

    def leaveEvent(self, a0: QEvent) -> None:
        self.x = -1
        self.y = -1
        self.repaint()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        pos = a0.pos()
        self.x = pos.x()
        self.y = pos.y()
        self.repaint()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        pos = a0.pos()
        self.row_pressed, self.col_pressed = self.__get_coord(pos.x(), pos.y())
        self.repaint()

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if self.row_pressed == -1 or self.col_pressed == -1:
            return
        pos = a0.pos()
        row_released, col_released = self.__get_coord(pos.x(), pos.y())
        if row_released == self.row_pressed and col_released == self.col_pressed:
            print('select', row_released, col_released)
        self.row_pressed = -1
        self.col_pressed = -1
        self.repaint()

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        pen = QPen()

        # Draw lines
        xs, ys = self.__get_line_xs(), self.__get_line_ys()
        pen.setColor(Qt.black)
        for i, x in enumerate(xs):
            pen.setWidth(self.BORDER_WIDTH if i % 3 == 0 else self.NORMAL_LINE_WIDTH)
            painter.setPen(pen)
            painter.drawLine(x, self.BORDER_WIDTH // 2, x, self.height() - 1 - self.BORDER_WIDTH // 2)
        for i, y in enumerate(ys):
            pen.setWidth(self.BORDER_WIDTH if i % 3 == 0 else self.NORMAL_LINE_WIDTH)
            painter.setPen(pen)
            painter.drawLine(self.BORDER_WIDTH // 2, y, self.width() - 1 - self.BORDER_WIDTH // 2, y)

        if self.x == -1 or self.y == -1:
            return

        if self.row_pressed == -1 or self.col_pressed == -1:
            row, col = self.__get_coord(self.x, self.y, xs, ys)
            pen.setColor(Qt.blue)
        else:
            row, col = self.row_pressed, self.col_pressed
            pen.setColor(Qt.red)

        if row == -1 or col == -1:
            return

        # Draw block
        x1, y1, x2, y2 = xs[col], ys[row], xs[col + 1], ys[row + 1]
        x1 += self.BORDER_WIDTH // 2 + 1 if col % 3 == 0 else self.NORMAL_LINE_WIDTH // 2 + 1
        y1 += self.BORDER_WIDTH // 2 + 1 if row % 3 == 0 else self.NORMAL_LINE_WIDTH // 2 + 1

        x2 -= self.BORDER_WIDTH // 2 if (col + 1) % 3 == 0 else self.NORMAL_LINE_WIDTH // 2
        y2 -= self.BORDER_WIDTH // 2 if (row + 1) % 3 == 0 else self.NORMAL_LINE_WIDTH // 2

        pen.setWidth(1)
        painter.setPen(pen)
        rect = QRect(x1, y1, x2 - x1, y2 - y1)
        painter.fillRect(rect, pen.color())

    def __get_line_xs(self):
        return [int(col * (self.width() - self.BORDER_WIDTH) / 9) + self.BORDER_WIDTH // 2 for col in range(10)]

    def __get_line_ys(self):
        return [int(row * (self.height() - self.BORDER_WIDTH) / 9) + self.BORDER_WIDTH // 2 for row in range(10)]

    def __get_coord(self, x, y, xs=None, ys=None):
        if not xs:
            xs = self.__get_line_xs()
        if not ys:
            ys = self.__get_line_ys()

        if x in xs or y in ys:
            return -1, -1

        row, col = -1, -1
        for i in range(9):
            if xs[i] < x < xs[i + 1]:
                col = i
                break
        for j in range(9):
            if ys[j] < y < ys[j + 1]:
                row = j
                break
        return row, col
