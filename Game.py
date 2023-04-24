from Board import Board
from Tree import Tree
import copy

class Game:
    def __init__(self, height, width, blank, player1, player2, win):
        self.height = height
        self.width = width
        self.blank = blank
        self.player1 = player1
        self.player2 = player2
        self.win = win
        self.board = [[blank for i in range(width)] for j in range(height)]
        self.skip = False
        self.display()

    def start_game(self):
        num = 0
        while self.check_win() == False and self.skip != True:
            self.turn((num % 2) + 1)
            num += 1
        #self.win(self.check_win())
        print(f"Congrats, player {self.check_win()} wins!")
        return self.copy_board()

    def start_game_AI(self):
        num = 0
        while self.check_win() == False and self.skip != True:
            if (num % 2) + 1 == 1:
                self.turn(1)
            else:
                self.AI_turn()
            num += 1
        #self.win(self.check_win())
        print(f"Congrats, player {self.check_win()} wins!")
        return self.copy_board()

    def AI_turn(self):
        tree = Tree(self.copy_board())
        move = tree.find_path()

        self.move(move, self.player2)
        self.display()
        print(f"AI makes move {move + 1}")

    def turn(self, player):
        piece = 0
        if player == 1:
            piece = self.player1
        elif player == 2:
            piece = self.player2

        move = 0
        print(f"Enter your turn player {piece}")
        try:
            move = int(input()) - 1
        except:
            print(f"Invalid input. Enter an integer between 1 and {self.width}")
            self.turn(player)
        else:
            if move < 0:
                self.skip = True
            elif self.check_valid(move):
                self.move(move, piece)
                self.display()
            else:
                print("Try again")
                self.turn(player)

    def display(self):
        for i in range((self.width * 3) - 2):
            print('_', end = "")
        print('\n')
        for b in self.board:
            for i in b:
                print(i, ' ', end = "")
            print('\n')

    def win(self, player):
        print(f"Congrats, player {player} wins!")

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
        score1 = 0
        score2 = 0
        for i in self.board:
            for j in i:
                if j == self.player1:
                    score1 += 1
                elif j == self.player2:
                    score2 += 1

        if score2 < self.win and score1 < self.win:
            return False

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

    def copy_board(self):
        return Board(self.height, self.width, self.blank, self.player1, self.player2, self.win, copy.deepcopy(self.board))