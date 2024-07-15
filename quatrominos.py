import numpy as np
import typing


class Quatrominos(object):

    def __init__(self, player0: typing.Set[typing.Tuple[int, int, int, int]],
                 player1: typing.Set[typing.Tuple[int, int, int, int]],
                 board: np.ndarray,
                 player_on_turn: int):
        """
        Initializes the game board, and divides the tiles among both players.
        Each tile is represented as a 1d numpy array, consisting of exactly
        four numbers, where the first number (index 0) is positioned north, the
        second number (index 1) is positioned east, the third number (index 2)
        is positioned south and finally the fourth number (index 3) is
        positioned west. Of course, both players are free to rotate the numbers
        both clockwise and anti-clockwise.

        :param player0: The tiles that are in the hand of player 0
        :param player1: the tiles that are in the hand of player 1
        :param board: The playing board will be a 3-dimensional array, where
        the first two dimensions depict the columns and rows of the game board,
        respectively, and the third dimension is of size 4, representing a
        tile.
        :param player_on_turn: 0 iff player 0 is on turn, 1 otherwise
        """
        self.player_hand = [player0, player1]
        self.board = board
        self.player_on_turn = player_on_turn

    def print_current_state(self) -> None:
        """
        Prints the current state, in free format
        """
        print("player0's hand is:")
        for tile in self.player_hand[0]:
            print(f"""
+---+
| {tile[0]} |
|{tile[3]} {tile[1]}|
| {tile[2]} |
+---+""", end= "")
        print("\nplayer1's hand is:")
        for tile in self.player_hand[1]:
            print(f"""
+---+
| {tile[0]} |
|{tile[3]} {tile[1]}|
| {tile[2]} |
+---+\n""", end= "")
            print("Current board is:")
            tilesInRow = [[] for x in range(5)]
            for row in self.board:
                for tile in row:
                    tilesInRow[0].append(f"+---+")
                    tilesInRow[4].append("+---+")
                    if -1 in tile:
                        tilesInRow[1].append(f"|   |")
                        tilesInRow[2].append(f"|   |")
                        tilesInRow[3].append(f"|   |")

                    else:
                        tilesInRow[1].append(f"| {tile[0]} |")
                        tilesInRow[2].append(f"|{tile[3]} {tile[1]}|")
                        tilesInRow[3].append(f"| {tile[2]} |")

                for i in range(5):
                    print("".join(tilesInRow[i]))
                    tilesInRow[i] = []

    @staticmethod
    def get_rotated_tile(tile: typing.Tuple[int, int, int, int],
                         rotations: int) -> typing.Tuple[int, int, int, int]:
        """
        Returns a tile that is a clock-wise rotation of the input tile. E.g.,
        tile (1, 2, 3, 4) will in case of a single rotation be rotated to
        tile (4, 1, 2, 3)

        :param tile: the input tile to rotate
        :param rotations: the number of rotations (each rotation being a 90
        degree clockwise turn)
        :return: The rotated tile
        """
        for _ in range(rotations):
            #will iterate for the amount of rotations given
            #takes the last element of the tile, makes it into a single element tuple,
            #then takes the rest of the original tile and adds it to the tuple.
            tile = (tile[-1], ) + tile[:-1]

        return tile

    def board_is_empty(self) -> bool:
        """
        Function which checks whether the board is empty by looking at all the tiles on the board
        and checking whether -1 is in the tile. If it encounters one tile which doesn't contain -1,
        it will know the board isn't empty and return False.
        :return: True if board is empty, False if it isn't.
        """

        for row in self.board:
            for column in row:
                if -1 not in column:
                    return False #Returns false because a tile which isn't empty has been found

        return True

    def is_next_to_tile(self, board_y, board_x) -> bool:
        """
        Function which checks whether there is already a tile next to a given position on a board

        :param board_y: the y value of the position
        :param board_x: the x value of the position
        :return: True if there is a tile next to a certain position, False if there is not
        """

        if board_y-1 >= 0 and -1 not in self.board[board_y-1][board_x]:
            return True
        if board_x+1 < len(self.board) and -1 not in self.board[board_y][board_x+1]:
            return True
        if board_y+1 < len(self.board) and -1 not in self.board[board_y+1][board_x]:
            return True
        if board_x-1 >= 0 and -1 not in self.board[board_y][board_x-1]:
            return True

        return False

    def adjacent_locations(self) -> typing.Set[typing.Tuple[int, int]]:
        """
        Returns a set with tuples of (y,x)-coordinates where we could
        potentially fit a tile (if the numbers would match). Note that the
        first tile should always be placed in the middle.

        :return: a set with tuples of (y,x)-coordinates of vacant positions
        adjacent to non-vacant positions
        """

        postitions_of_possible_moves = set()

        if self.board_is_empty() == True:
            return {(2,2)}

        for y, row in enumerate(self.board):
            for x, column in enumerate(row):
                for i, element in enumerate(column):
                    if element != -1:
                        if i == 0 and 0 <= y-1 < len(self.board) and -1 in self.board[y-1][x]:
                            #if i == 0 it's the north tile so you want to place it up one tile so the row is -1.
                            #so you have to check if y-1 (where you want to place it) is not smaller than 0
                            #because if it was, it would be out of the board.
                            #then you also need to check if -1 is in the tile, which means it's empty
                            postitions_of_possible_moves.add((y-1, x))
                        elif i == 1 and 0 <= x+1 < len(self.board) and -1 in self.board[y][x+1]:  #east
                            postitions_of_possible_moves.add((y, x+1))
                        elif i == 2 and 0 <= y+1 < len(self.board) and -1 in self.board[y+1][x]:  #south
                            postitions_of_possible_moves.add((y+1, x))
                        elif i == 3 and 0 <= x-1 < len(self.board) and -1 in self.board[y][x-1]:  #west
                            postitions_of_possible_moves.add((y, x-1))


        return postitions_of_possible_moves


    def can_place_given_tile(self, board_y: int, board_x: int, #Zijn er aantal true die false moeten zijn
                             tile: np.array) -> bool:
        """
        Checks whether the tile, in its current orientation, can be placed on
        the indicated position on the board. Note that the numbers of the tile
        are north, east, south, west, respectively.

        :param board_y: board y index to place the tile
        :param board_x: board x index to place the tile
        :param tile: the numpy array representing the tile
        :return: true if the tile can be placed in this orientation on the
        board, false otherwise
        """

        #First checking for the northern element of the tile if the place you want to put the tile is on the
        #northern edge of the board. If it is, then you don't have to check for the southern element of the tile above you
        #because there isn't any. If it isn't on the edge, you have to check if the nothern element of your tile is
        #the same as the southern element of the tile above you or if the tile above is empty. If any of these statements
        #are true then you're good to go on the nothern part. Then you have to check for all other directions.
        #If they all turn out true, you can place the tile.
        if self.board_is_empty():
            return True

        if self.is_next_to_tile(board_y, board_x) == True:
            if -1 in self.board[board_y][board_x]:
                if board_y-1 < 0 or tile[0] == self.board[board_y-1][board_x][2] or self.board[board_y-1][board_x][2] == -1:
                    if board_x+1 >= len(self.board) or tile[1] == self.board[board_y][board_x+1][3] or self.board[board_y][board_x+1][3] == -1:
                        if board_y+1 >= len(self.board) or tile[2] == self.board[board_y+1][board_x][0] or self.board[board_y+1][board_x][0] == -1:
                            if board_x-1 < 0 or tile[3] == self.board[board_y][board_x-1][1] or self.board[board_y][board_x-1][1] == -1:
                                return True


        return False

    def count_available_moves(self, tiles: np.array) -> int:
        """
        Counts the number of moves that can be made, with the tiles provided.
        Note that a tile can be placed in various orientations. Different
        orientations count as different moves.

        :param tiles: A numpy array with the tiles
        :return: The number of moves a player can make
        """

        if self.board_is_empty() == True:
            return 4
        else:
            number_of_moves = 0
            for tile in tiles:
                for rotations in range(4): #rotations
                    for y in range(len(self.board)):
                        for x in range(len(self.board)):
                            if -1 in self.board[y][x]:
                                if self.can_place_given_tile(y,x,tile) == True:
                                    number_of_moves += 1
                    tile = self.get_rotated_tile(tile, 1)

        return number_of_moves

    def check_current_player_lost(self) -> bool:
        """
        Determines whether the player that is currently on turn has lost the
        game. That can either happen by the other player having played all
        their tiles, or the current player having no available moves.

        :return: True iff the current player has lost, False otherwise
        """

        for i in range(2): #This bit is to correct for the mistake in the unit test which sees an empty hand as an empty dictionary
            if self.player_hand[i] == set():
                self.player_hand[i] = {}

        if self.player_hand[abs(self.player_on_turn-1)] == {} or self.count_available_moves(self.player_hand[self.player_on_turn]) == 0:
            #First condition is true if the opponent's hand is empty
            #Second statement is true if the current player has no more moves
            return True
        else:
            return False

    def current_player_can_win(self) -> bool:
        """
        Uses a exhaustive search algorithm to determine which player will win,
        if both players adopt an optimal strategy. Use a recursive function.
        See the slides of lecture 3 to find pseudo-code for this algorithm.
        Ensure that after this function, all class variables that were changed
        are set back to their original values.

        :return: True iff the player on turn can win
        """

        #If the current player has lost it obviously cannot win so return False
        if self.check_current_player_lost():
            return False
        else:
            possible_moves = self.adjacent_locations()
            playing_hand = self.player_hand[self.player_on_turn]
            #Starting a loop which will run until the current player has a way to win or all possible moves have been played
            for y, x in possible_moves:
                for tile in playing_hand:
                    for i in range(4):
                        rotated = self.get_rotated_tile(tile, i)
                        if self.can_place_given_tile(y, x, rotated):
                            self.board[y][x] = rotated
                            playing_hand.remove(tile) #Removing the tile from the player's hand
                            self.player_on_turn = abs(self.player_on_turn-1)  #Giving the turn to the other player
                            if self.current_player_can_win() == False: #Recursion
                                #Reverting the move that has been played to try again
                                self.board[y][x] = np.array([-1, -1, -1, -1])
                                playing_hand.add(tile)
                                self.player_on_turn = abs(self.player_on_turn-1)
                                return True
                            self.board[y][x] = np.array([-1, -1, -1, -1])
                            playing_hand.add(tile)
                            self.player_on_turn = abs(self.player_on_turn-1)
            return False


    def best_move_greedy(self) -> typing.Tuple[int, int, np.array]:
        """
        OPTIONAL. Design a greedy function to determine the best way. This
        algorithm involves enumerating all possible moves, and determining
        which of the moves seems good, without looking further ahead. A logical
        greedy approach would be, e.g., select the move that leaves the other
        player with the least possible amount of free moves.

        :return: A 3-tuple, containing the (y, x) coordinate of the tile, and
        the tile in its proper orientation
        """

        playing_moves = [] #List in which we will store the moves which can be played

        possible_moves = self.adjacent_locations()
        playing_hand = self.player_hand[self.player_on_turn]

        for y, x in possible_moves:
            for tile in playing_hand:
                for i in range(4):
                    rotated = self.get_rotated_tile(tile, i)
                    if self.can_place_given_tile(y, x, rotated):
                        playing_moves.append((y, x, rotated))

        amount_of_opponent_moves = [] #storing the amount of moves the opponent has in a list per move
        for move in playing_moves:
            self.board[move[0]][move[1]] = move[2]
            amount = self.count_available_moves(self.player_hand[abs(self.player_on_turn-1)])
            amount_of_opponent_moves.append(amount)
            self.board[move[0]][move[1]] = np.array([-1, -1, -1, -1])
        #returning the move where the opponent has the least amount of moves
        return playing_moves[amount_of_opponent_moves.index(min(amount_of_opponent_moves))]



