
import numpy as np
import random
class Board():
    def __init__(self):
        self.board = np.zeros([3,3]) #creates a 3 by 3 matrix full of zeros.
        
    def empty_spots(self):
        not_occupied = np.where(self.board == 0)  
        not_occupied_1= list(zip(not_occupied[0], not_occupied[1])) #finds any zeros on the board, and saves their positions into a list. postions are accessed by elemnt of row.
        return not_occupied_1 

    def possible_moves(self, player):
        possible_locations = self.empty_spots() #creates all possible zero locations
        next_location = random.choice(possible_locations) #randomly assigns a space on the board for a 1 or a 2 to be placed.
        self.board[next_location] = player  #the players turn (a 1 or a 2) takes the spot of that 0.
        return self.board

    def horiztonal_win(self,player):
        board = self.board
        for x in range(len(board)): #uses nested loops to iterate through all the elements of the board.
            three_in_a_row = True
            
            for y in range(len(board)):
                if board[x, y] != player: #board[x,y] slicing means that each row and its elements are checked.
                     three_in_a_row = False 
                     continue               #if the elements in the row are not the same, continue checking.
            if three_in_a_row == True:
                return three_in_a_row
        return three_in_a_row    #if the elements of any of the row are the same (a player has won). stop looping and save the row.
    
    def vertical_wins(self,player):
        board = self.board
        for x in range(len(board)):
            three_in_a_row = True
            for y in range(len(board)): #board[y,x] means that each column and its elements are checked. (the indexing goes by the columns.)
                if board[y,x] != player:
                    three_in_a_row = False #if no elements in a column are the same, continue checking.
                    continue
            if three_in_a_row == True: #if any there are 3 matching elements in a column, save the column.
                 return three_in_a_row
        return three_in_a_row

    def diagonal_wins(self, player):
        board = self.board
        three_in_a_row = True
        y = 0
        
        for x in range(len(board)):
            if board[x,x] != player: #from row 1 to 3, slice the 0th, 1st, and 2nd elemntents from each row respectively. (the first row returns its 0th element, the second row returns its 1st element, and the third row returns its second element.)
                three_in_a_row = False 
        if three_in_a_row: 
            return three_in_a_row
        three_in_a_row = True
        if three_in_a_row:
            for x in range(len(board)):
                y = len(board) - 1 - x #flips the matri from left to right, fights the top right to the bottem left.
                if board[x,y] != player:
                    three_in_a_row = False
        return three_in_a_row

    def check_game_status(self):
        winner = 0
        for player in [1,2]: #possible players are 1 or 2
            if (self.horiztonal_win(player) or self.vertical_wins(player)) or self.diagonal_wins(player): #if any of the check functions (1 or 2 have three in a row, column or diagonal), set the winner equal to the player value.
                winner = player
        if np.all(self.board != 0) and winner == 0: #checks if game is tied. if all the elements in the board are not equal to 0 (all possible moves have been made) and no one has won, there is a draw.
            winner =  "The game has ended in a draw."
        return winner
    def play_game(self):

        board = self.board
        winner = 0
        print(board)  #prints the board before any moves are made


    
        while winner == 0:
            for player in [1,2]: #players or moves 1 or 2 are allowed to replace 0s on the board.
                board = self.possible_moves(player) #a 1 or a 2 gets randomly placed onto the board
                print(board,'\n' ) #prints the board to see where the player was randomly placed.
                winner = self.check_game_status() #continues to loop through until someone has won or there is a draw/out of space.
                if winner != 0: #if winner value from other functions is changed because a player won or there was a draw, break out of the loop
                    break
        return  winner #this returns which player has won the game

    def giveReward(self):
        result = self.winner()
        # backpropagate reward
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.1)

    def reset(self):
        self.board = np.zeros((3,3))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def play(self, rounds=10000):
        for i in range(rounds):
            if i % 1000 == 0:
                    print("Round {}".format(i))
        while not self.isEnd:
            # Player 1
            positions = self.availablePositions()
            p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
            # take action and update board state
            self.updateState(p1_action)
            board_hash = self.getHash()
            self.p1.addState(board_hash)
            # check board status if it is end

            win = self.winner()
            if win is not None:
            # self.showBoard()
            # ended with p1 either win or draw
                self.giveReward()
                self.p1.reset()
                self.p2.reset()
                self.reset()
                break

            else:
                # Player 2
                positions = self.availablePositions()
                p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                self.updateState(p2_action)
                board_hash = self.getHash()
                self.p2.addState(board_hash)

                win = self.winner()
                if win is not None:
                    # self.showBoard()
                    # ended with p2 either win or draw
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break
        









board = Board()
print(board.play_game())
    


    