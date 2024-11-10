from pathlib import Path
from .Word import Word
from .FrequencyTable import FrequencyTable
from .Pawns import Pawns
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Board:

    def __init__(self):
        self.__board = [[" " for _ in range(15)] for _ in range(15)]
        self.__totalWords = 0
        self.__totalPawns = 0
        self.__score = 0

    @property
    def getBoard(self) -> list:
        return self.__board
    
    @property
    def getBoardlen(self) -> int:
        return len(self.__board)
    
    @property
    def getScore(self) -> int:
        return self.__score
    
    @property
    def getTotalWords(self) -> int:
        return self.__totalWords
    
    def showBoard(self) -> None:
        """
        show the bard game with row and column coordinate
        """

        xycolors = pd.read_csv( Path(__file__).parent / "DataSets/xycolor_board.csv")
        
        # create the plt figurte that will save to board
        figure = plt.figure(figsize= (10, 10))
        ax = figure.add_subplot(111)

        # draw the vertical and horizontal line
        for x in range(self.getBoardlen + 1):
            ax.plot([x, x], [0, self.getBoardlen], 'k')
        
        for y in range(self.getBoardlen + 1):
            ax.plot([0, self.getBoardlen], [y, y], 'k')
        
        # define the limits of the axes
        ax.set_xlim(-1, self.getBoardlen + 1)
        ax.set_ylim(-1, self.getBoardlen + 1)
        
        # scale so that grill occupies the entire figure
        ax.set_position((0, 0, 1, 1))    
        ax.set_axis_off()

        for row in xycolors.itertuples():
            polygon = Polygon(self.__generateVertex(row[1], row[2]), color = row[3])
            ax.add_artist(polygon)

        for i in range (self.getBoardlen):
            # draw the number in the board
            # top number
            ax.text(
                self.__transformation(i + 0.5), self.__transformation(self.getBoardlen + 0.5), str(i), 
                verticalalignment = "center", horizontalalignment = "center", fontsize = 20, 
                fontfamily = "fantasy", fontweight = "bold", transform = ax.transAxes
            )

            # right number
            ax.text(
                self.__transformation(self.getBoardlen + 0.5), self.__transformation(i + 0.5), str(i), 
                verticalalignment = "center", horizontalalignment = "center", fontsize = 20, 
                fontfamily = "fantasy", fontweight = "bold", transform = ax.transAxes
            )
        
            # draw the letters in the board
            for j in range(self.getBoardlen):
                ax.text(
                    self.__transformation(j + 0.5), self.__transformation(14 - i + 0.5), 
                    self.__board[i][j], verticalalignment = "center", horizontalalignment = "center",
                    fontsize = 15, transform = ax.transAxes
                )
        plt.show()

    def placeWord(self, player_pawns, word, x, y, direction) -> None:
        """
        Put the word in the board, removing used pawn form the player's bag
        Args:
            player_pawns (Pawns): player's pawns bag
            word (Word): create word
            x (int): coordinates on the x axis
            y (int): coordinate on the y axis
            direction (str): "V" if the word is on the y axis or "H" if the word is on the x axis
        """

        for letter in word.word:
            if letter != self.__board[x][y]:
                player_pawns.takePawn(letter)
                self.__totalPawns += 1
                self.__board[x][y] = letter
                self.__score += Pawns.getPoinst(letter)

            if direction == "V":
                x += 1
            else:
                y += 1

        self.__totalWords += 1

    def isPossible(self, word, x, y, direction) -> tuple:
        """
        Is possible put the word on board

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x axis
            y (int): coordinates on the y axis
            direction (str): "V" if the word is on the y axis or "H" if the word is on the x axis

        returns:
            Tuple: (bool, str): is possible put the word and message
        """

        validation = self.__isWordGoOffBoard(word, x, y, direction)
        
        if not validation[0]:
            return validation

        validation = self.__firstPawnIsCentralPosition(word, x, y, direction)

        if not validation[0]:
            return validation

        validation = self.__placeWordsUsingExistingBoard(word)

        if not validation[0]:
            return validation

        validation = self.__putCorrectPawn(word, x, y, direction)

        if not validation[0]:
            return validation
        
        validation = self.__isPawnInitalInSartOrFinalOtherPawns(x, y, direction)

        if not validation[0]:
            return validation

        return (True, "")

    def getPawns(self, word, x, y, direction) -> Word:
        """
        get Pawns missing on the board for make a word

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x axis
            y (int): coordinates on the y axis
            direction (str): "V" if the word is on the y axis or "H" if the word is on the x axis

        returns:
            Word: is possible put the word and message
        """
        
        missing_pawns = Word()
        possible, message = self.isPossible(word, x, y, direction)
        
        if not possible:
            print(message)
            return word
        
        for letter in word.word:
            if self.__board[x][y] != letter:
                missing_pawns.word.append(letter)
            
            if direction == "V":
                x += 1
            else:
                y += 1
        
        return missing_pawns
    
    def showWordPlacement(self, pawns, word) -> None:
        """
        Displays all possible placements of the word on the board.

        Args:
            pawns (Pawns): The player's pawns
            word (Word): The word to place
        """

        for x in range(self.getBoardlen):
            for y in range(self.getBoardlen):
                for direction in ["H", "V"]:
                    
                    if self.isPossible(word, x, y, direction)[0]:
                        needPawns = self.getPawns(word, x, y, direction)
                        
                        if FrequencyTable.isSubset(needPawns.getFrequency(), pawns.getFrequency()):
                            print("{}:".format("Verical" if direction == "V" else "Horizontal"))
                            print("(x = {}, y = {})".format(x, y))

    def __firstPawnIsCentralPosition(self, word, x, y, direction) -> tuple:
        """
        Validation of first Pawns is in central position (7,7)

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x axis
            y (int): coordinates on the y axis
            direction (str): "V" if the word is on the y axis or "H" if the word is on the x axis

        Returns:
            Tuple: (bool, str): validation result and message
        """

        if self.__totalWords == 0:
            if direction == "V" and not (
                x == 7 and 7 in range(y, y + word.getLengthWord() - 1)
            ):
                return (False, "La primera palabra debe pasar por la casilla central (7,7).")

            elif direction == "H" and not (
                y == 7 and 7 in range(x, x + word.getLengthWord() - 1)
            ):
                return (False, "La primera palabra debe pasar por la casilla central (7,7).")

        return (True, "")
    
    def __isWordGoOffBoard(self, word, x, y, direction) -> tuple:
        """
        Validation of length of word cannot go off the board

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x axis
            y (int): coordinates on the y axis
            direction (str): "V" if the word is on the y axis or "H" if the word is on the x axis

        Returns:
            Tuple: (bool, str): validation result and message
        """

        if direction == "H" and (x < 0 or y < 0 or (y + word.getLengthWord() - 1) >= 15):
            return (False, "La palabra sobrepasa el límite horizontal del tablero.")
        elif direction == "V" and (x < 0 or y < 0 or (x + word.getLengthWord() - 1) >= 15):
            return (False, "La palabra sobrepasa el límite vertical del tablero.")
        
        return (True, "")
    
    def __placeWordsUsingExistingBoard(self, word) -> tuple:
        """
        Validation of word using have a letter that exinsting in board

        Args:
            word (Word): word object for validation

        Returns:
            Tuple: (bool, str): validation result and message
        """
        if self.__totalWords > 0:
            boardSet = set().union(*self.__board)
            wordSet = set(word.word)
            
            if not wordSet.intersection(boardSet):
                return (False, "Todas las palabras, excepto la primera, deben utilizar una ficha ya existente en el tablero.")
            
        return (True, "")
    
    def __putCorrectPawn(self, word, x, y, direction) -> tuple: 
        """
        Validation of Put a pawn in position empty o equal letter in position and put at least one new pawns

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x axis
            y (int): coordinates on the y axis
            direction (str): "V" if the word is on the y axis or "H" if the word is on the x axis

        Returns:
            Tuple: (bool, str): validation result and message
        """
        if self.__totalWords > 0:
            hasNewPawn = False
            
            for letter in word.word:
                if self.__board[x][y] != " " and letter != self.__board[x][y]:
                    return (False, "No se puede colocar una ficha en una casilla que ya esté ocupada por un ficha diferente.")
                elif self.__board[x][y] == " ":
                    hasNewPawn = True
                    
                if direction == "V":
                    x += 1
                else:
                    y += 1
            
            if not hasNewPawn:
                return (False, "Se debe colocar al menos una ficha nuevo en el tablero.")
            
        return (True, "")
    
    def __isPawnInitalInSartOrFinalOtherPawns(self, x, y, direction) -> tuple:
        """
        Validation of new pawn initial in start or final other word in board

        Args:
            x (int): coordinates on the x axis
            y (int): coordinates on the y axis
            direction (str): "V" if the word is on the y axis or "H" if the word is on the x axis

        Returns:
            Tuple: (bool, str): validation result and message
        """
        if self.__totalWords > 0:
            if direction == "V" and (x != 0 and self.__board[x - 1][y] != " "):
                return (False, "Hay fichas adicionales al principio o al final de una palabra.")
            elif (x != 0 and self.__board[x][y  - 1] != " "):
                return (False, "Hay fichas adicionales al principio o al final de una palabra.")
            
        return (True, "")
    
    def __transformation(self, x) -> int:
        """
        Convert interval (-1,16) to interval (0,1)

        Args:
            x (int): interval for transformation

        Returns:
            int: the transformation interval
        """
        
        return (x + 1) / 17
    
    def __generateVertex(self, center_x, center_y) -> np.ndarray:
        """
        Generate the vertices of a square centered at (center_x, center_y).
        
        Args:
            center_x (int): x-coordinate of the center
            center_y (int): y-coordinate of the center

        Returns:
            np.ndarray: 2D array of vertices representing the square
        """
        
        return np.array([
            [center_x - 0.5, center_y - 0.5], [center_x - 0.5, center_y + 0.5],
            [center_x + 0.5, center_y + 0.5], [center_x + 0.5, center_y - 0.5]
        ])