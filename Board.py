import copy

class Board:
    def __init__(self, height, width, blank, player1, player2, win, board):
        self.height = height
        self.width = width
        self.blank = blank
        self.player1 = player1
        self.player2 = player2
        self.win = win
        self.board = board
        self.turn = self.calc_turn()

    def calc_turn(self):
        count1 = 0
        count2 = 0
        for j in self.board:
            for i in j:
                if i == self.player1:
                    count1 += 1
                elif i == self.player2:
                    count2 += 1
        if count1 == count2:
            return self.player1
        else:
            return self.player2

    def get_turn(self):
        return self.turn

    def next_turn(self):
        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1
    
    def copy_board(self):
        return Board(self.height, self.width, self.blank, self.player1, self.player2, self.win, copy.deepcopy(self.board))

    def display(self):
        for i in range((self.width * 3) - 2):
            print('_', end = "")
        print('\n')
        for b in self.board:
            for i in b:
                print(i, ' ', end = "")
            print('\n')

    def move(self, col, char):
        for i in reversed(range(self.height)):
            if self.board[i][col] == self.blank:
                self.board[i][col] = char
                return

    def check_valid(self, col):
        if col >= self.width:
            return False
        if self.board[0][col] != self.blank:
            return False
        return True

    def check_win(self):
        # Horizontal 1 & 2 Checking
        count = 0
        for i in self.board:
            for j in i:
                if j == self.player1:
                    count += 1
                else:
                    count = 0
                if count >= self.win:
                    return self.player1
            count = 0
        count = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] == self.player1:
                    count += 1
                else:
                    count = 0
                if count >= self.win:
                    return self.player1
            count = 0
        count = 0
        for i in self.board:
            for j in i:
                if j == self.player2:
                    count += 1
                else:
                    count = 0
                if count >= self.win:
                    return self.player2
            count = 0
        count = 0
        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] == self.player2:
                    count += 1
                else:
                    count = 0
                if count >= self.win:
                    return self.player2
            count = 0
        # Diagonal 1 & 2 Checking
        for i in range(self.height - self.win + 1):
            for j in range(self.win - 1, self.width):
                if (self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == self.board[i+3][j-3] == self.player1):
                    return self.player1
        for i in range(self.height - self.win + 1):
            for j in range(self.win):
                if (self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] == self.player1):
                    return self.player1
        for i in range(self.height - self.win + 1):
            for j in range(self.win - 1, self.width):
                if (self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == self.board[i+3][j-3] == self.player2):
                    return self.player2
        for i in range(self.height - self.win + 1):
            for j in range(self.win):
                if (self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] == self.player2):
                    return self.player2
        return False
        