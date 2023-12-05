from tkinter import *
import time

class sudoku(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Sudoku")
        self.root.geometry("550x550")

        self.solveButton = Button(self.root, command=self.getValues, text="Solve", width=10)
        self.solveButton.grid(row=20, column=1, columnspan=5, pady=10)

        self.clearButton = Button(self.root, command=self.getValuesVis, text="Visualize", width=10)
        self.clearButton.grid(row=20, column=3, columnspan=5, pady=10)

        self.clearButton = Button(self.root, command=self.clearValues, text="Clear", width=10)
        self.clearButton.grid(row=20, column=5, columnspan=5, pady=10)

        self.speedIncreaseButton = Button(self.root, command=self.increaseSpeed, text="Increase Speed", width=15)
        self.speedIncreaseButton.grid(row=21, column=1, columnspan=5, pady=10)

        self.speedDecreaseButton = Button(self.root, command=self.decreaseSpeed, text="Decrease Speed", width=15)
        self.speedDecreaseButton.grid(row=21, column=5, columnspan=5, pady=10)

        self.board = []
        self.cells = {}
        self.N = 9
        self.speed = 0.1
        self.firstColor = "#F94C10"
        self.secondColor = "#FFB84C"

        self.label = Label(self.root, text="Fill in the numbers and click solve").grid(row=0, column=1, columnspan=10)

        self.errLabel = Label(self.root, text="", fg="red")
        self.errLabel.grid(row=15, column=1, columnspan=10, pady=5)

        self.solvedLabel = Label(self.root, text="", fg="green")
        self.solvedLabel.grid(row=15, column=1, columnspan=10, pady=5)

        self.reg = self.root.register(self.numberValidation)

    def increaseSpeed(self):
        if self.speed > 0.01:
            self.speed -= 0.01

    def decreaseSpeed(self):
        if self.speed > 0.001:
            self.speed += 0.01

    def numberValidation(self, value):
        return (value.isdigit() or value == "") and len(value) < 2

    def clearLabels(self):
        self.errLabel.configure(text="")
        self.solvedLabel.configure(text="")

    def draw3x3Grid(self, row, column, bgcolor):
        for i in range(3):
            for j in range(3):
                e = Entry(self.root, width=5, bg=bgcolor, justify="center", validate="key", validatecommand=(self.reg, "%P"))
                e.grid(row=row+i+1, column=column+j+1, sticky="nsew", padx=1, pady=2, ipady=5)
                self.cells[(row+i+1, column+j+1)] = e

    def draw9x9Grid(self):
        color = self.firstColor
        for r in range(1, 10, 3):
            for c in range(0, 9, 3):
                self.draw3x3Grid(r, c, color)
                if color == self.firstColor:
                    color = self.secondColor
                else:
                    color = self.firstColor

    def clearValues(self):
        self.clearLabels()
        self.board = []

        for r in range(2, 11):
            for c in range(1, 10):
                cell = self.cells[(r, c)]
                cell.delete(0, "end")

        self.draw9x9Grid()

    def getValues(self):
        self.clearLabels()

        for r in range(2, 11):
            rows = []
            for c in range(1, 10):
                val = self.cells[(r, c)].get()
                if val == "":
                    rows.append(0)
                else:
                    rows.append(int(val))
            self.board.append(rows)
        self.updateValues()

    def getValuesVis(self):
        self.clearLabels()

        for r in range(2, 11):
            rows = []
            for c in range(1, 10):
                val = self.cells[(r, c)].get()
                if val == "":
                    rows.append(0)
                else:
                    rows.append(int(val))
            self.board.append(rows)
        self.updateValues(vis=True)

    def updateValues(self, vis=False):
        sol = self.solver(self.board.copy()) if not vis else self.visualize(self.board.copy())
        if sol != "NO":
            for r in range(2, 11):
                for c in range(1, 10):
                    current_value = self.cells[(r, c)].get()
                    if current_value != str(sol[r - 2][c - 1]) and sol[r - 2][c - 1] != 0:
                        self.cells[(r, c)].delete(0, "end")
                        self.cells[(r, c)].insert(0, sol[r - 2][c - 1])
                        self.cells[(r, c)].config(bg="light green")
            self.solvedLabel.configure(text="Sudoku Solved")
        else:
            self.errLabel.configure(text="No solution exists for this sudoku!!")

    def isSafe(self, board, r, c, number):
        for i in range(self.N):
            if board[r][i] == number:
                return False

        for i in range(self.N):
            if board[i][c] == number:
                return False

        startR = r - r % 3
        startC = c - c % 3

        for i in range(3):
            for j in range(3):
                if board[startR + i][startC + j] == number:
                    return False
        return True

    def delay_backtracking(self, board, r, c):
        if r == self.N - 1 and c == self.N:
            return True
        if c == self.N:
            r += 1
            c = 0
        if board[r][c] > 0:
            return self.delay_backtracking(board, r, c + 1)

        for num in range(1, self.N + 1):
            if self.isSafe(board, r, c, num):
                board[r][c] = num

                self.cells[(r + 2, c + 1)].delete(0, "end")
                self.cells[(r + 2, c + 1)].insert(0, num)
                self.cells[(r + 2, c + 1)].config(bg="light green")
                self.root.update()
                time.sleep(self.speed * 2)

                if self.delay_backtracking(board, r, c + 1):
                    return True
                board[r][c] = 0

                original_color = self.cells[(r + 2, c + 1)].cget("bg")

                self.cells[(r + 2, c + 1)].config(bg="yellow")
                self.root.update()
                time.sleep(self.speed * 2)

                self.cells[(r + 2, c + 1)].config(bg=original_color)
                self.cells[(r + 2, c + 1)].delete(0, "end")
                self.cells[(r + 2, c + 1)].insert(0, "")
                self.root.update()

        return False

    def backtracking(self, board, r, c):
        if r == self.N - 1 and c == self.N:
            return True
        if c == self.N:
            r += 1
            c = 0
        if board[r][c] > 0:
            return self.backtracking(board, r, c+1)
        for num in range(1, self.N+1):
            if self.isSafe(board, r, c, num):
                board[r][c] = num
                if self.backtracking(board, r, c+1):
                    return True
            board[r][c] = 0
        return False

    def visualize(self, board):
        if self.delay_backtracking(board, 0, 0):
            return board
        else:
            return "NO"

    def solver(self, board):
        if self.backtracking(board, 0, 0):
            return board
        else:
            return "NO"

    def startGame(self):
        self.draw9x9Grid()
        self.root.mainloop()


sudokuTest = sudoku()
sudokuTest.startGame()
