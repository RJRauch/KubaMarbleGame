# Author: Ryan Rauch
# Date: 5/24/2021
# Description: Virtual implementation of the Kuba  marble board game according to the rules listed below

# Rules of Kuba:
# 1) No consecutive turns for same player (modified by professors for this project)
# 2) 8 back, 8 white, and 13 red marbles arranged at same configuration at each start
# 3) Left upper corner is (0,0) and right lower corner is (6,6)
# 4) Game is won when a player gets 7 red stones or by pushing off all opposing player stones
# 5) must be an empty space at the end of the side you are pushing from or an edge piece
# 6) You cannot reverse a previous move if it creates an identical game state (would create infinity)- KO RULE
# 7) A player has also lost if there are no legal moves available--> although this logic will not be tested per the professors
# 8) Turns are alternating between players, any player may go first
# 9) Moves may only occur in an orthogonal direction (Left(L), Right (R), Forward (F), and Backward (B)
# 10)Up to six marbles can be pushed by your marble in one turn, but a player cannot push one of his own stones off
# 11) Any marbles pushed off that are black and white are removed from the game.
# 12) Red, black, and white marbles are represented by R,B, W respectively

#Deep copy is utilized to generate and compare game states for verification of the Ko Rule
#Utilized in the KubaGame  class
from copy import deepcopy


class Player:
    """Player class object it responsible for tracking a player and the marble associated with that player as well as captured red marbles of the player"""
    """Communicates with KubaGame class and is instantiated when necessary within KubaGame class """
    """Data member values are obtained and modified when necessary from within KubaGame class"""
    """Player objects are referenced as KubaClass data members"""
    def __init__(self, player, marble):
        """constructor for the player class that initializes the data members player and marble and captured red"""
        """returns implicit None type singleton"""
        self.player = player                # Expected arguments for this is data type string, "PlayerA" or "PlayerB"
        self.marble = marble                # Expected argument for this is data type string, "B" or "W"
        self.captured_red = 0               # Initialized statically to integer 0, is incremented as appropriate during gameplay

    #--SETTER/GETTER METHODS--------------------------------------------------------------------------------------------
    #NONE AT THIS TIME, consider adding get/set captured red so that this class has a justified existence


class KubaGame:
    """Kuba board game class that contains the board logic for movement, ability to track turns, and check for win states"""
    """Adheres to the rules as commented above"""
    """Needs to interact with Player class objects and does so by instantiating them when necessary"""
    """References the Player objects my making them data members of the KubaClass"""

    def __init__(self, player_1, player_2):
        """constructor that takes two tuples and initializes as data member values of a newly instantiated player object"""
        """The player object them becomes a data member fo the KubaGame Object"""
        """each parameter will have data expected to be passed in as a tuple"""
        " first element in tuple parameter will be player, second element will be marble type"
        self.player_1 = Player(player_1[0], player_1[1])                                    # Player object created, tuple elements assigned as data member values of player object
        self.player_2 = Player(player_2[0], player_2[1])
        self.current_turn = None                                                            # will track a player name (either "PlayerA" or "PlayerB"), whose turn it is currently
        self.game_on = True                                                                 # this will remain True as long as the game remains in session
        self.winner = None                                                                  # will return the winner in form of player name (Either "PlayerA" or "PlayerB"
        self.marble_list = [8, 8, 13]                                                       # Marble list keeps track of number of marbles in play in order [W,B,R]
        # Implements a 7x7 game board with marbles initialized in starting locations according to kuba game diagram for display purposes
        # Each list is a row, each element in each list is a column. Thus a column is a traversal down the same index of every list
        # Thus to access an element of any list, input a (row,column) tuple pair
        self.game_board = [['W', 'W', 'X', 'X', 'X', 'B', 'B'], ['W', 'W', 'X', 'R', 'X', 'B', 'B'],
                           ['X', 'X', 'R', 'R', 'R', 'X', 'X'], ['X', 'R', 'R', 'R', 'R', 'R', 'X'],
                           ['X', 'X', 'R', 'R', 'R', 'X', 'X'], ['B', 'B', 'X', 'R', 'X', 'W', 'W'],
                           ['B', 'B', 'X', 'X', 'X', 'W', 'W']]
        self.last_state = list()   # This will be the previous state of the game board before move is implemented on it (using deepcopy), it is changed every OTHER turn
        self.next_state = list()   # This will be the game board after the current move is implemented on it (using deepcopy)
        self.current_player_marble = None   # Tracks the marble color of the current player ("B" or "W")
        self.ko_counter = 0                 # A counter that tracks when the previous state needs to be copied for validation of the ko rule

    #------GETTER METHODS #---------------------------------------------------------------------------------------------
    def get_current_turn(self):
        """Getter method for current turn data member, returns the same"""
        return self.current_turn

    def get_winner(self):
        """Getter method for winner data member, returns the same """
        return self.winner

    def get_captured(self, player_name: str):
        """returns number of captured red marbles for given player"""
        """Expects to be passed a player name (str)"""
        if self.player_1.player == player_name:
            return self.player_1.captured_red
        else:
            if self.player_2.player == player_name:
                return self.player_2.captured_red
            else:
                return "That player does not exist!"                            # Has built in error handling in event of invalid data

    def get_marble(self, position_tuple: tuple):
        """returns marble in the given passed tuple of integers (row,column) argument containing coordinate location
         returns X if spot is empty because empty spots are the defaulted to X in game initialization"""
        try:
            return self.game_board[position_tuple[0]][position_tuple[1]]        # Has built in error handling in event of invalid data
        except IndexError:
            return "That is not a board position"

    def get_marble_count(self):
        """Getter method that returns the marble count in tuple format of order (W,B,R)"""
        return tuple(self.marble_list)

    # END GETTER METHODS #----------------------------------------------------------------------------------------------
    def display_board(self):
        """prints a visual display for debugging purposes, and for display of game logic"""
        """Returns None"""
        print("\n")
        print("\n")
        print(self.game_board[0][0]+'|'+self.game_board[0][1]+'|'+self.game_board[0][2]+'|'+
              self.game_board[0][3]+'|'+self.game_board[0][4]+'|'+self.game_board[0][5]+'|'+
              self.game_board[0][6])
        print('-|-|-|-|-|-|-')
        print(self.game_board[1][0]+'|'+self.game_board[1][1]+'|'+self.game_board[1][2]+'|'+
              self.game_board[1][3]+'|'+self.game_board[1][4]+'|'+self.game_board[1][5]+'|'+
              self.game_board[1][6])
        print('-|-|-|-|-|-|-')
        print(self.game_board[2][0]+'|'+self.game_board[2][1]+'|'+self.game_board[2][2]+'|'+
              self.game_board[2][3]+'|'+self.game_board[2][4]+'|'+self.game_board[2][5]+'|'+
              self.game_board[2][6])
        print('-|-|-|-|-|-|-')
        print(self.game_board[3][0]+'|'+self.game_board[3][1]+'|'+self.game_board[3][2]+'|'+
              self.game_board[3][3]+'|'+self.game_board[3][4]+'|'+self.game_board[3][5]+'|'+
              self.game_board[3][6])
        print('-|-|-|-|-|-|-')
        print(self.game_board[4][0]+'|'+self.game_board[4][1]+'|'+self.game_board[4][2]+'|'+
              self.game_board[4][3]+'|'+self.game_board[4][4]+'|'+self.game_board[4][5]+'|'+
              self.game_board[4][6])
        print('-|-|-|-|-|-|-')
        print(self.game_board[5][0]+'|'+self.game_board[5][1]+'|'+self.game_board[5][2]+'|'+
              self.game_board[5][3]+'|'+self.game_board[5][4]+'|'+self.game_board[5][5]+'|'+
              self.game_board[5][6])
        print('-|-|-|-|-|-|-')
        print(self.game_board[6][0]+'|'+self.game_board[6][1]+'|'+self.game_board[6][2]+'|'+
              self.game_board[6][3]+'|'+self.game_board[6][4]+'|'+self.game_board[6][5]+'|'+
              self.game_board[6][6])

    def make_move(self, playername: str, coordinates: tuple, direction: str):
        """method containing the move logic for the game as well as the ability to check for wins"""
        """Playername is expected to be a string"""
        """coordinates are a tuple of two integers in (row,column) format"""
        """ direction is a string of either "F", "R", "L", B" """
        """Returns True if the game move was successful, else returns False """

        if self.get_current_turn() is None:                                # This check will only execute if first move of game
            if self.player_1.player == playername:
                self.current_turn = self.player_1.player                   # Will assign appropriate player to current turn
                self.current_player_marble = self.player_1.marble          # Assigns appropriate marble of current player
                self.last_state = deepcopy(self.game_board)                # makes a deep initial copy of the initialized game state
            else:
                if self.player_2.player == playername:                     # Same as above but for alternate player, if necessary
                    self.current_turn= self.player_2.player
                    self.current_player_marble = self.player_2.marble
                    self.last_state = deepcopy(self.game_board)
                else:
                    return "That player doesn't exist!"

        #--CONDITIONAL CHECKS THAT PROHIBIT A MOVE#---------------------------------------------------------------------
        if self.game_on is False:                                    # Will check if the game has already been won
            return False
        if self.get_current_turn() != playername:                    # If input player is not current player's turn, returns False
            return False
        if self.game_board[coordinates[0]][coordinates[1]] != 'X':   # Check if opponent occupies coordinate point, returns False
            if self.game_board[coordinates[0]][coordinates[1]] != self.current_player_marble:
                return False
        if self.game_board[coordinates[0]][coordinates[1]] == 'X':   # Checks if passed coordinate position is an empty spot, returns False
            return False

        if coordinates[0] > 6 or coordinates[0] < 0:                 # Handles invalid coordinates
            return False

        if coordinates[1] > 6 or coordinates[1] < 0:
            return False


        #--TURN LOGIC# -------------------------------------------------------------------------------------------------
        if direction == 'R':
            if coordinates[1] == 0 or self.game_board[coordinates[0]][coordinates[1]-1] == 'X':
                self.next_state = deepcopy(self.game_board)                                       # create deep copy of game board for comparison to last_state later on
                if "X" in self.next_state[coordinates[0]][coordinates[1]:]:                       # This will handle scenario in which there is an empty space, which will terminate movement of our pieces after that space
                    index = self.next_state[coordinates[0]][coordinates[1]:].index('X')+coordinates[1]  # To get the actual index position of the "X' in the entire list, we add the index position of the 'X" in the sublist to the starting coordinates
                    counter = index - (coordinates[1])                                            # This is actually how many times we will make changes to our pieces before stopping
                    while counter > 0:                                                            # Essentially, the index is our position of our x, and counter is the difference between our ending point and the number of moves we have to make to get to all pieces moved excluding first piece
                        self.next_state[coordinates[0]][index] = self.next_state[coordinates[0]][index-1]
                        index -= 1
                        counter -= 1
                    self.next_state[coordinates[0]][coordinates[1]] = 'X'                          # Change the starting character  to 'X (as that is where we started moving from and it will be left empty)
                    if self.next_state[coordinates[0]]== self.last_state[coordinates[0]]:          # If this undoes the previous last game state return False
                        self.next_state = list()
                        return False
                else:                                                                              # this is special scenario where a piece will be pushed off of the board
                    if self.next_state[coordinates[0]][-1] == self.current_player_marble:          # checks to ensure an edge marble will not be pushed off of the board
                        return False
                    index = -1
                    counter = (len(self.next_state[coordinates[0]][coordinates[1]:])-1)
                    removed = self.next_state[coordinates[0]][-1]                                  # This is the piece that will be pushed off of the board
                    while counter > 0:                                                             # Go through and change all appropriate pieces
                        self.next_state[coordinates[0]][index] = self.next_state[coordinates[0]][index-1]
                        counter -= 1
                        index -= 1
                    self.next_state[coordinates[0]][coordinates[1]] = 'X'                          # sets initial moving piece to "X"
                    if self.next_state[coordinates[0]] == self.last_state[coordinates[0]]:
                        self.next_state = list()                                                    # Reinitialize list
                        return False
                    if removed == 'W':                                                              # subtract removed marble as appropriate from the count
                        self.marble_list[0] -= 1
                    if removed == 'B':
                        self.marble_list[1] -= 1
                    if removed == 'R':
                        self.marble_list[2] -= 1
                        if self.player_1.player == self.get_current_turn():
                            self.player_1.captured_red += 1                                         # increment captured red count
                        else:
                            self.player_2.captured_red += 1
            else:                                                                                   # Returns False if not an edge piece or doesn't have a space to the left
                return False
        if direction == 'L':
            if coordinates[1] == (len(self.game_board[coordinates[0]])-1) or self.game_board[coordinates[0]][coordinates[1] + 1] == 'X':  # Here we check if an edge piece or if a space to the right is empty
                self.next_state = deepcopy(self.game_board)                                                             # create deep copy of our game board
                if "X" in self.next_state[coordinates[0]][:coordinates[1]]:                                             # Checks if there is an "X" in the desired movement space
                    reversed_index= self.next_state[coordinates[0]][coordinates[1]::-1].index('X')                      # Otherwise, we reverse the list to find the FIRST X to the left of our piece (which will stop our movement)
                    index = coordinates[1] - reversed_index                                                             # This will give us the index position of our FIRST x to the left of our marker
                    counter = reversed_index                                                                            # how many pieces we must change (excluding first initial piece)
                    while counter > 0:
                        self.next_state[coordinates[0]][index] = self.next_state[coordinates[0]][index+1]               # Starting at the terminating x, we move each piece left
                        index += 1
                        counter -= 1
                    self.next_state[coordinates[0]][coordinates[1]] = "X"                          # Check for Ko rule
                    if self.next_state[coordinates[0]]== self.last_state[coordinates[0]]:
                        self.next_state = list()
                        return False
                else:
                    if self.next_state[coordinates[0]][0] == self.current_player_marble:           # checks if moving will knock same color off of the board (which is prohibited)
                        self.next_state = list()
                        return False
                    removed = self.next_state[coordinates[0]][0]                                    # This is special circumstance in which 6 marbles will be moved and a marble will be knocked off
                    index= 0                                                                        # We will start at the beginning of our list and then move pieces to the left until the last piece on the right
                    counter = coordinates[1]                                                        # This is how many moves we will have to make
                    while counter > 0:
                        self.next_state[coordinates[0]][index] = self.next_state[coordinates[0]][index+1]   # Iterate through and move to left
                        counter -= 1
                        index += 1
                    self.next_state[coordinates[0]][coordinates[1]] = 'X'                                   # Replace rightmost coordinate in moving space with empty space
                    if self.next_state[coordinates[0]] == self.last_state[coordinates[0]]:
                        self.next_state = list()                                                            # Reinitialize list
                        return False
                    if removed == 'W':                                                                      # subtract removed marble as appropriate from the count
                        self.marble_list[0] -= 1
                    if removed == 'B':
                        self.marble_list[1] -= 1
                    if removed == 'R':
                        self.marble_list[2] -= 1
                        if self.player_1.player == self.get_current_turn():
                            self.player_1.captured_red += 1  # increment captured red count
                        else:
                            self.player_2.captured_red += 1
            else:
                return False

        if direction == 'F':
            if coordinates[0] == 6 or self.game_board[coordinates[0]+1][coordinates[1]] == 'X':     # Checks if this is at the bottom edge of board or if space below moving marble is empty which would allow a forward move
                self.next_state = deepcopy(self.game_board)                                         # create a deep copy
                counter = 0                                                                         # to easier access the desired column, instead of iterating through each list in the gameboard, we create an artificial list of the members of our desired column
                column_list = list()
                while counter <= 6:                                                                 # create the list of desired column members
                    column_list.append(self.next_state[counter][coordinates[1]])
                    counter += 1
                if "X" in column_list[:coordinates[0]]:                                             # Checks if x is in the desired column of movement which will terminate movement early
                    reversed_index = column_list[coordinates[0]::-1].index('X')                     # Since we want to move up ( and effectively left if viewed horizontally, we will use the similar technique we used with leftward horizontal movement)
                    index = coordinates[0] - reversed_index
                    counter = reversed_index
                    while counter > 0:                                                              # Here we iterate through the columns and change members as appropriate
                        self.next_state[index][coordinates[1]] = self.next_state[index+1][coordinates[1]]
                        index += 1
                        counter -= 1
                    self.next_state[coordinates[0]][coordinates[1]] = "X"                           # change the initial marker to x
                    counter = 0
                    column_list = list()
                    last_list = list()
                    while counter <= 6:                                                             # to check the Ko rule, we have a to make an artificial row of the column from the last saved game state to the moved game state to see if the ko rule violated
                        column_list.append(self.next_state[counter][coordinates[1]])
                        last_list.append(self.last_state[counter][coordinates[1]])
                        counter += 1
                    if last_list == column_list:                                                    # If ko rule is violated, return False
                        self.next_state = list()
                        return False
                else:                                                                               # This is the case that all the marbles will be moved and one will be removed from the board
                    if self.next_state[0][coordinates[1]] == self.current_player_marble:
                        self.next_state = list()
                        return False

                    else:
                        removed = self.next_state[0][coordinates[1]]                                 # This is special circumstance in which 6 marbles will be moved and a marble will be knocked off
                        index = 0                                                                    # We will start at the beginning
                        counter = coordinates[0]                                                     # This is how many moves we will have to make
                        while counter > 0:
                            self.next_state[index][coordinates[1]] = self.next_state[index+1][coordinates[1]]
                            counter -= 1
                            index += 1
                        self.next_state[coordinates[0]][coordinates[1]] = 'X'                         # Replace rightmost coordinate in moving space with empty space
                        counter = 0
                        column_list = list()
                        last_list = list()
                        while counter <= 6:                                                         # here we iterate and move members forward
                            column_list.append(self.next_state[counter][coordinates[1]])
                            last_list.append(self.last_state[counter][coordinates[1]])
                            counter += 1
                        if last_list == column_list:
                            self.next_state = list()
                            return False
                        if removed == 'W':                                                            # subtract removed marble as appropriate from the count
                            self.marble_list[0] -= 1
                        if removed == 'B':
                            self.marble_list[1] -= 1
                        if removed == 'R':
                            self.marble_list[2] -= 1
                            if self.player_1.player == self.get_current_turn():
                                self.player_1.captured_red += 1  # increment captured red count
                            else:
                                self.player_2.captured_red += 1
            else:
                return False

        if direction == "B":                                                                        # For the final move we see if we can move members backward (vertically down)
            if coordinates[0] == 0 or self.game_board[coordinates[0]+1][coordinates[1]] == 'X':
                self.next_state = deepcopy(self.game_board)                                         # Make a deep list
                counter = 0
                column_list = list()
                while counter <= 6:                                                                 # make artificial list of desired column of movement
                    column_list.append(self.next_state[counter][coordinates[1]])
                    counter += 1
                if "X" in column_list[coordinates[0]:]:                                             # Check for x in desired column of movement, which will terminate or movement
                    index = column_list[coordinates[0]:].index('X')+coordinates[0]
                    counter = index- coordinates[0]
                    while counter > 0:                                                              # Move pieces rightward (in the faux horizontal list, which is down vertically)
                        self.next_state[index][coordinates[1]] = self.next_state[index-1][coordinates[1]]
                        index -= 1
                        counter -= 1
                    self.next_state[coordinates[0]][coordinates[1]] = 'X'                           # Change last piece to x
                    counter = 0
                    column_list = list()
                    last_list = list()
                    while counter <= 6:                                                             # create lists for evaluation of Ko rule
                        column_list.append(self.next_state[counter][coordinates[1]])
                        last_list.append(self.last_state[counter][coordinates[1]])
                        counter += 1
                    if last_list == column_list:
                        self.next_state = list()
                        return False
                else:
                    if self.next_state[6][coordinates[1]] == self.current_player_marble:           # if edge marble is same marble as player's marble, move cannot happen
                        self.next_state = list()
                        return False
                    else:
                        removed = self.next_state[6][coordinates[1]]                                # otherwise we iterate through moving all the marbles
                        index=6
                        counter = 5- coordinates[0]
                        while counter >0:
                            self.next_state[index][coordinates[1]] = self.next_state[index-1][coordinates[1]]
                            index -= 1
                            counter -= 1
                        self.next_state[coordinates[0]][coordinates[1]] = "X"
                        counter = 0
                        column_list = list()
                        last_list = list()
                        while counter <= 6:                                                         # We create the artificial lists for checking ko rule
                            column_list.append(self.next_state[counter][coordinates[1]])
                            last_list.append(self.last_state[counter][coordinates[1]])
                            counter += 1
                        if last_list == column_list:
                            self.next_state = list()
                            return False
                        if removed == 'W':                                                         # subtract removed marble as appropriate from the count
                            self.marble_list[0] -= 1
                        if removed == 'B':
                            self.marble_list[1] -= 1
                        if removed == 'R':
                            self.marble_list[2] -= 1
                        if self.player_1.player == self.get_current_turn():
                            self.player_1.captured_red += 1                                        # increment captured red count
                        else:
                            self.player_2.captured_red += 1
            else:
                return False

        #--END TURN WIN CHECKS------------------------------------------------------------------------------------------
        if self.get_marble_count()[2] == 6:                         # check if a player has 7 red marbles (wins game)
            if self.player_1.captured_red == 7:                     # If player 1, declares winner and returns False
                self.winner = self.player_1.player
                self.game_on = False
            else:                                                   # Else, declares player 2 winner and returns False
                self.winner= self.player_2.player
                self.game_on = False

        if self.get_marble_count()[0] == 0:                         # Checks if all white marbles are off board
            if self.player_1.marble == "W":                         # if player one is white, player 2 wins
                self.winner = self.player_2.player
                self.game_on = False
            else:
                self.winner = self.player_1.player                  # else Player 2 is white, and player 1 wins
                self.game_on = False
        if self.get_marble_count()[1] == 0:                         # Checks if all black marbles are off board
            if self.player_1.marble == "B":                         # if player 1 is black, player 2 has won
                self.winner = self.player_2.player
                self.game_on = False
            else:                                                   # else player 2 is black, and player 1 wins
                self.winner = self.player_1.player
                self.game_on = False
        if self.game_on is True:                                    # ensures game is still ongoing
            if self.player_1.player == self.get_current_turn():     # Changes turn
                self.current_turn = self.player_2.player
                self.current_player_marble = self.player_2.marble
            else:
                self.current_turn = self.player_1.player
                self.current_player_marble = self.player_1.marble
        self.game_board = deepcopy(self.next_state)                # At this point, we update the game board to save the move of the current turn
        self.ko_counter += 1                                       # Increment ko counter
        if self.ko_counter != 0:
            if self.ko_counter %2 == 0:                            # save last state for ko evaluation every other move
                self.last_state = deepcopy(self.game_board)
        self.next_state = list()
        return True


#Guardian script if needed
def main():
    """guardian script if needed"""
    pass

if __name__ == "__main__":
    main()
