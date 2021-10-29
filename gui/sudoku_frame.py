from PyQt5.QtCore import Qt, QEvent, QRect
from PyQt5.QtGui import QPaintEvent, QPainter, QMouseEvent, QPen, QFont, QColor
from PyQt5.QtWidgets import QFrame, QMessageBox, QInputDialog

from sudoku import Game, DancingLinksXSolver


class SudokuFrame(QFrame):
    BORDER_WIDTH = 7
    NORMAL_LINE_WIDTH = 3
    NUMBER_FONT = QFont('Times New Romans', 20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__game = Game()
        self.__solved_game = None

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
        row_clicked, col_clicked = self.__get_coord(pos.x(), pos.y())
        if row_clicked == self.row_pressed and col_clicked == self.col_pressed:
            try:
                val = QInputDialog.getInt(self, '', '')
                if val[1]:
                    num = val[0]
                    if not 1 <= num <= 9:
                        raise ValueError
                    if self.__game.get(row_clicked, col_clicked) != num:
                        self.__game.set(row_clicked, col_clicked, num)
                        if self.__solved_game and \
                                self.__solved_game.get(row_clicked, col_clicked) != num:
                            self.__solved_game = None
            except ValueError:
                QMessageBox.warning(self, 'Error', 'Not a valid number!')
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
            painter.drawLine(x, self.BORDER_WIDTH // 2, x,
                             self.height() - 1 - self.BORDER_WIDTH // 2)
        for i, y in enumerate(ys):
            pen.setWidth(self.BORDER_WIDTH if i % 3 == 0 else self.NORMAL_LINE_WIDTH)
            painter.setPen(pen)
            painter.drawLine(self.BORDER_WIDTH // 2, y,
                             self.width() - 1 - self.BORDER_WIDTH // 2, y)

        # Draw original blocks
        pen.setWidth(1)
        pen.setColor(Qt.black)
        painter.setPen(pen)
        painter.setFont(self.NUMBER_FONT)
        for i in range(9):
            for j in range(9):
                if self.__game.get(i, j) != 0:
                    painter.fillRect(self.__get_rect(i, j, xs, ys), Qt.gray)

        # Draw the selected block
        if self.x != -1 and self.y != -1:
            if self.row_pressed != -1 and self.col_pressed != -1:
                row, col = self.row_pressed, self.col_pressed
                pen.setColor(QColor(0, 0, 150))
            else:
                row, col = self.__get_coord(self.x, self.y, xs, ys)
                pen.setColor(QColor(0, 0, 255))

            if row != -1 and col != -1:
                pen.setWidth(1)
                painter.setPen(pen)
                painter.fillRect(self.__get_rect(row, col, xs, ys), pen.color())

        # Draw numbers
        pen.setWidth(1)
        pen.setColor(Qt.black)
        painter.setPen(pen)
        for i in range(9):
            for j in range(9):
                num = self.__game.get(i, j)
                if num != 0:
                    painter.drawText(self.__get_rect(i, j, xs, ys), Qt.AlignCenter, str(num))

        # Draw solved numbers
        if not self.__solved_game:
            return
        for i in range(9):
            for j in range(9):
                if self.__game.get(i, j) == 0:
                    painter.drawText(self.__get_rect(i, j, xs, ys), Qt.AlignCenter,
                                     str(self.__solved_game.get(i, j)))

    def solve(self):
        try:
            self.__solved_game = DancingLinksXSolver(self.__game).get_solved_game()
        except ValueError:
            self.__solved_game = None
            QMessageBox.warning(self, 'Error', 'The game is not solvable!')
        self.repaint()

    def __get_line_xs(self):
        return [int(col * (self.width() - self.BORDER_WIDTH) / 9) + self.BORDER_WIDTH // 2
                for col in range(10)]

    def __get_line_ys(self):
        return [int(row * (self.height() - self.BORDER_WIDTH) / 9) + self.BORDER_WIDTH // 2
                for row in range(10)]

    def __get_coord(self, x, y, xs=None, ys=None):
        if xs is None:
            xs = self.__get_line_xs()
        if ys is None:
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

    def __get_rect(self, row: int, col: int, xs=None, ys=None) -> QRect:
        if xs is None:
            xs = self.__get_line_xs()
        if ys is None:
            ys = self.__get_line_ys()

        x1, y1, x2, y2 = xs[col], ys[row], xs[col + 1], ys[row + 1]
        x1 += self.BORDER_WIDTH // 2 + 1 if col % 3 == 0 else self.NORMAL_LINE_WIDTH // 2 + 1
        y1 += self.BORDER_WIDTH // 2 + 1 if row % 3 == 0 else self.NORMAL_LINE_WIDTH // 2 + 1

        x2 -= self.BORDER_WIDTH // 2 if (col + 1) % 3 == 0 else self.NORMAL_LINE_WIDTH // 2
        y2 -= self.BORDER_WIDTH // 2 if (row + 1) % 3 == 0 else self.NORMAL_LINE_WIDTH // 2
        return QRect(x1, y1, x2 - x1, y2 - y1)
