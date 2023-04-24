from Board import Board
import random

class Node():
        def __init__(self, board):
            self.board = board
            self.children = []
            self.win = self.board.check_win()
            self.avg = self.average_for_board(self.board.board, 4, self.board.player1)

        def fill_child_array(self):
            if self.win == False:
                for i in range(self.board.width):
                    self.children.append(Node(self.board.copy_board()))
                    self.children[i].board.move(i, self.board.turn)
                    self.children[i].board.next_turn()
                    self.children[i].win = self.board.check_win()

        def display_head_then_children(self):
            self.board.display()
            for i in range(self.board.width):
                self.children[i].board.display()

        def instantiate_recursive(self, num):
            self.win = self.board.check_win()
            self.avg = self.average_for_board(self.board.board, 4, self.board.player1)
            if (num == 0):
                return
            if self.win != False:
                return 0
            if self.win == False:
                self.fill_child_array()
                for node in self.children:
                    node.instantiate_recursive(num - 1)

        def display_recursive(self, num):
            if (num == 0):
                return
            self.board.display()
            print(self.avg)
            for node in self.children:
                node.display_recursive(num - 1)

        def display_win_recursive(self, num, ):
            if (num == 0):
                return
            if self.win != False:
                self.board.display()
                print(self.win)
            for node in self.children:
                node.display_win_recursive(num - 1)

        def find_path(self):
            self.instantiate_recursive(2)
            for i in range(self.board.width):
                if (self.children[i].win == self.board.player2):
                    return i

            possible_moves = [*range(self.board.width)]

            for i in range(self.board.width):
                for j in range(self.board.width):
                    if self.children[i].children[j].win == self.board.player1:
                        try:
                            possible_moves.remove(i)
                        except:
                            pass
            
            avg = [0 for i in range(len(possible_moves))]

            iterator = 0
            for i in possible_moves:
                sum = 0
                for i in self.children[i].children:
                    if i != None:
                        sum += i.avg
                    else:
                        sum += 1.0
                avg[iterator] = sum/self.board.width
                iterator += 1
            
            # Temporary fix
            if len(avg) == 0:
                return random.randint(0,self.board.width)

            return possible_moves[avg.index(min(avg))]

        def four_row(self, iterable):
            iterator = iter(iterable)
            try:
                firstItem = next(iterator)
            except StopIteration:
                return True
            for x in iterator:
                if x!=firstItem:
                    return False
            return True

        def possible_win(self, check_list):
            curr_val = check_list[0]
            number = 0
            for item in check_list:
                if item != curr_val and item != "-":
                    return False
                if item == curr_val:
                    number+=1
            return number  

        def check_right(self, board,win_num,x,y): # checks for wins to the right
            curr_val = str(board[y][x])
            check_list = []
            check_list.append(curr_val)
            while len(check_list)<win_num:
                x+=1
                curr_val = str(board[y][x])
                check_list.append(curr_val)
            if self.four_row(check_list) is True:
                return True 
            else:
                return self.possible_win(check_list)

        def check_up_right(self, board,win_num,x,y): #checks for wins up and to the right
            curr_val = str(board[y][x])
            check_list = []
            check_list.append(curr_val)
            while len(check_list)<win_num:
                x+=1
                y-=1
                curr_val = str(board[y][x])
                check_list.append(curr_val)
            if self.four_row(check_list) is True:
                return True
            else:
                return self.possible_win(check_list)

        def check_up_left(self, board,win_num,x,y): #checks for wins up and to the left
            curr_val = str(board[y][x])
            check_list = []
            check_list.append(curr_val)
            while len(check_list)<win_num:
                x-=1
                y-=1
                curr_val = str(board[y][x])
                check_list.append(curr_val)
            if self.four_row(check_list) is True:
                return True
            else:
                return self.possible_win(check_list)
                
        def check_up(self, board, win_num, x, y): #checks for wins straight up
            curr_val = str(board[y][x])
            check_list = []
            check_list.append(curr_val)
            while len(check_list)<win_num:
                y-=1
                curr_val = str(board[y][x])
                check_list.append(curr_val)
                if self.four_row(check_list) is True:
                    return True
                else:
                    return self.possible_win(check_list)

        def average_for_board(self, board,win_num,curr_player): #insert an array and a number to win and see the average of the current player
            potential_list = []
            Y = len(board)
            X = len(board[0])
            end_state=0
            y=Y-1
            for row in reversed(board): #start at the bottom on the board
                if end_state == X: #if there is a row of characters that are not the curr_player
                    total = 0
                    for items in potential_list:
                        total += items
                    average = total/len(potential_list)
                    return average
                end_state=0
                x=0
                for item in row:
                    value = str(board[y][x])
                    if value==curr_player:
                        if x>=(win_num-1): #if there are three spots to the left of current position
                            if self.check_up_left(board,win_num,x,y) != False:#if no win then check for the average
                                potential_list.append(self.check_up_left(board,win_num,x,y))
                            
                        if X-x>=win_num: #if there are three spots to the right of the current position
                            if self.check_right(board,win_num,x,y) != False:#if no win then check for the average
                                potential_list.append(self.check_right(board,win_num,x,y))
                            if self.check_up_right(board,win_num,x,y) != False: #if no win then check for the average
                                potential_list.append(self.check_up_right(board,win_num,x,y))

                        if y>=win_num: #if there are three spots above the current position
                            if self.check_up(board,win_num,x,y) != False: #if no win then check for the average
                                potential_list.append(self.check_up(board,win_num,x,y))
                    else:
                        end_state+=1
                    x+=1
                y-=1
        
class Tree:
    def __init__(self, board):
        self.head = Node(board)

    def add_child(self, to_add):
        self.head.children.prepend(Node(to_add))

    def fill_head_children(self):
        self.head.fill_child_array()

    def display_head_then_children(self):
        self.head.display_head_then_children()

    def find_path(self):
        return self.head.find_path()