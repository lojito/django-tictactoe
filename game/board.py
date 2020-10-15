from abc import ABCMeta, abstractmethod
from random import randint

class BoardError(Exception, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, board):
        self._board = board

    @abstractmethod
    def __str__(self):
        return
        
class BoardInvalidPlayerError(BoardError):
    def __init__(self, board, player):
        super().__init__(board)
        self._player = player

    def __str__(self):
        return f'Invalid player = {self._player}. Valids values for a player are {Board.UNKNOWN_PLAYER} for an unknown user, {Board.USER} for the user and {Board.COMPUTER} for the computer' 

class BoardInvalidSquareError(BoardError):
    def __init__(self, board, square):
        super().__init__(board)
        self._square = square;

    def __str__(self):
        return 	f'The square {self._square} does not exist. Squares values range from 0 to {Board.SQUARES_NUMBER}.'

class BoardInvalidError(BoardError):
    def __init__(self, board, board_str):
        super().__init__(board)
        self._board_str = board_str
        
    def __str__(self):
        return 	f'The Tic-Tac-Toe board value of "{self._board_str}" is invalid. Expecting a string of {Board.SQUARES_NUMBER} characters with {Board.UNKNOWN_PLAYER}(empty square), {Board.USER}(user played on that square) or {Board.COMPUTER}(computer played on that square) as the only possible values.'
        
class Board:
    UNKNOWN_PLAYER = 0
    USER = 1
    COMPUTER = 2
    SQUARE_NOT_FOUND = -1
    SQUARES_NUMBER = 16
    
    def __init__(self, board):
        if not isinstance(board, str) or len(board) != Board.SQUARES_NUMBER:
            raise BoardInvalidError(self, board)
        
        self.board = []
        for player in board:
            if int(player) not in [Board.UNKNOWN_PLAYER, Board.USER, Board.COMPUTER]:
                raise BoardInvalidError(self, board)
            self.board.append(int(player))
     
    def is_full(self):
        return not Board.UNKNOWN_PLAYER in self.board

    def play(self, player, square):
        if player != Board.USER and player != Board.COMPUTER:
            raise BoardInvalidPlayerError(self, player)
            
        if self.is_full():
            return Board.SQUARE_NOT_FOUND

        try:
            self.board[square] = player
        except IndexError:
            raise BoardInvalidSquareError(self, square)
        
        return square
        
    def get_winning_square(self, player):
        if player != Board.USER and player != Board.COMPUTER:
            raise BoardInvalidPlayerError(self, player)
            
        if self.is_full():
            return Board.SQUARE_NOT_FOUND
            
        squares = [[0,1,2,3], [4,5,6,7], [8,9,10,11], [12,13,14,15], [0,4,8,12], [1,5,9,13], [2,6,10,14], [3,7,11,15], [0,5,10,15], [3,6,9,12]];
        for square0, square1, square2, square3 in squares:
            if self.board[square0] == player and self.board[square1] == player and self.board[square2] == player and self.board[square3] == Board.UNKNOWN_PLAYER:
              return square3
            if self.board[square0] == player and self.board[square1] == player and self.board[square2] == Board.UNKNOWN_PLAYER and self.board[square3] == player:
              return square2
            if self.board[square0] == player and self.board[square1] == Board.UNKNOWN_PLAYER and self.board[square2] == player and self.board[square3] == player:
              return square1
            if self.board[square0] == Board.UNKNOWN_PLAYER and self.board[square1] == player and self.board[square2] == player and self.board[square3] == player:
              return square0            
              
        return Board.SQUARE_NOT_FOUND
       
    def get_random_empty_square(self):
        if self.is_full():
            return Board.SQUARE_NOT_FOUND
    
        square = randint(0, Board.SQUARES_NUMBER - 1)
        while self.board[square] != Board.UNKNOWN_PLAYER:
            square = randint(0, Board.SQUARES_NUMBER - 1)
            
        return square    
            
    def __str__(self):
        board_str = ''
        for player in self.board:
            board_str = board_str + str(player)
        return board_str