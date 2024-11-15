from pathlib import Path
from ApylabradosModule import Word, FrequencyTable, Pawns, Vertex
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import pandas as pd

class Board:

    def __init__(self):
        self.__boardLen = 15
        self.__board = [[" " for _ in range(self.__boardLen)] for _ in range(self.__boardLen)]
        self.__totalWords = 0
        self.__totalPawns = 0
        self.__score = 0
        self.__multiplier = [[(1, "") for _ in range(self.__boardLen)] for _ in range(self.__boardLen)]

    @property
    def board(self) -> list:
        return self.__board
    
    @property
    def boardLen(self) -> int:
        return  self.__boardLen
    
    @property
    def score(self) -> int:
        return self.__score
    
    @property
    def totalWords(self) -> int:
        return self.__totalWords
    
    def showBoard(self, player_pawns_letter) -> None:
        """
        show the bard game with row and column coordinate
        """

        xy_colors = pd.read_csv(Path(__file__).parent / "DataSets/xycolor_board.csv")
        
        # create the plt figure that will save to board
        figure = plt.figure(figsize= (10, 10))
        ax = figure.add_subplot(111)

        # draw the vertical and horizontal line
        for x in range(self.boardLen + 1):
            ax.plot([x, x], [0, self.boardLen], 'k')
        
        for y in range(self.boardLen + 1):
            ax.plot([0, self.boardLen], [y, y], 'k')
        
        # define the limits of the axes
        ax.set_xlim(-1, self.boardLen + 1)
        ax.set_ylim(-1, self.boardLen + 1)
        
        # scale so that grill occupies the entire figure
        ax.set_position((0, 0, 1, 1))    
        ax.set_axis_off()

        for row in xy_colors.itertuples():
            polygon = Polygon(Vertex.generateVertex(row[1], row[2]), color = row[3])
            ax.add_artist(polygon)

        for i in range (self.boardLen):
            # draw the number in the board
            # top number
            ax.text(
                Vertex.transformation(i + 0.5), Vertex.transformation(self.boardLen + 0.5), str(i),
                verticalalignment = "center", horizontalalignment = "center", fontsize = 20, 
                fontfamily = "fantasy", fontweight = "bold", transform = ax.transAxes
            )

            # right number
            ax.text(
                Vertex.transformation(self.boardLen + 0.5), Vertex.transformation(i + 0.5), str(14 - i),
                verticalalignment = "center", horizontalalignment = "center", fontsize = 20, 
                fontfamily = "fantasy", fontweight = "bold", transform = ax.transAxes
            )
        
            # draw the letters in the board
            for j in range(self.boardLen):
                ax.text(
                    Vertex.transformation(j + 0.5), Vertex.transformation(14 - i + 0.5),
                    self.__board[i][j], verticalalignment = "center", horizontalalignment = "center",
                    fontsize = 15, transform = ax.transAxes
                )
        
        # display score in the screen
        ax.text(
            Vertex.transformation(0), Vertex.transformation(-0.5),
            "Score: {}".format(self.__score), verticalalignment = "center", horizontalalignment = "left",
            fontsize = 25, fontfamily = "fantasy", fontweight = "bold", transform = ax.transAxes
        )

        pawns_position = 4
        
        for pawn in player_pawns_letter:
            polygon = Polygon(Vertex.generateVertex(pawns_position, -0.6), color = "#FFF68F")
            ax.add_artist(polygon)
            
            ax.text(
                Vertex.transformation(pawns_position), Vertex.transformation(-0.6),
                pawn, verticalalignment = "center", horizontalalignment = "center",
                fontsize = 15, fontfamily = "fantasy", fontweight = "bold", transform = ax.transAxes
            )
            
            pawns_position += 1.5

        plt.show()

    def placeWord(self, player_pawns, word, x, y, direction) -> None:
        """
        Put the word in the board, removing used pawn form the player's bag
        Args:
            player_pawns (Pawns): player's pawns bag
            word (Word): create word
            x (int): coordinates on the x-axis
            y (int): coordinate on the y-axis
            direction (str): "V" if the word is on the y-axis or "H" if the word is on the x-axis
        """

        word_points = 0
        word_multiplier = 1
        
        for letter in word.word:
            if letter != self.__board[x][y]:
                player_pawns.takePawn(letter)
                self.__totalPawns += 1
                self.__board[x][y] = letter
                
                if self.__multiplier[x][y][1] != "w":
                    word_points += Pawns.getPoints(letter) * self.__multiplier[x][y][0]
                else:
                    word_points += Pawns.getPoints(letter)
                    word_multiplier *= self.__multiplier[x][y][0]

            if direction == "V":
                x += 1
            else:
                y += 1

        self.__totalWords += 1
        self.__score += word_points * word_multiplier

    def isPossible(self, word, x, y, direction) -> tuple:
        """
        Is possible put the word on board

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x-axis
            y (int): coordinates on the y-axis
            direction (str): "V" if the word is on the y-axis or "H" if the word is on the x-axis

        returns:
            Tuple: (bool, str): is possible put the word and message
        """

        validation = self.__firstPawnIsCentralPosition(word, x, y, direction)

        if not validation[0]:
            return validation
        
        validation = self.__isWordGoOffBoard(word, x, y, direction)
        
        if not validation[0]:
            return validation

        validation = self.__placeWordsUsingExistingBoard(word, x, y, direction)

        if not validation[0]:
            return validation

        validation = self.__putCorrectPawn(word, x, y, direction)

        if not validation[0]:
            return validation
        
        validation = self.__isPawnInitialInStartOrFinalOtherPawns(x, y, direction)

        if not validation[0]:
            return validation

        return True, ""

    def getPawns(self, word, x, y, direction) -> Word:
        """
        get Pawns missing on the board for make a word

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x-axis
            y (int): coordinates on the y-axis
            direction (str): "V" if the word is on the y-axis or "H" if the word is on the x-axis

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

        for x in range(self.boardLen):
            for y in range(self.boardLen):
                for direction in ["H", "V"]:
                    
                    if self.isPossible(word, x, y, direction)[0]:
                        needPawns = self.getPawns(word, x, y, direction)
                        
                        if FrequencyTable.isSubset(needPawns.getFrequency(), pawns.getFrequency()):
                            print("{}:".format("Verical" if direction == "V" else "Horizontal"))
                            print("(x = {}, y = {})".format(x, y))

    def setMultiplier(self) -> None:
        """
        Setup multiplier in the game
        """
        
        multipliers = pd.read_csv(Path(__file__).parent / "DataSets/multiplier_board.csv")
        
        for row in multipliers.itertuples():
            self.__multiplier[row[1]][row[2]] = (row[3], row[4])

    def __firstPawnIsCentralPosition(self, word, x, y, direction) -> tuple:
        """
        Validation of first Pawns is in central position (7,7)

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x-axis
            y (int): coordinates on the y-axis
            direction (str): "V" if the word is on the y-axis or "H" if the word is on the x-axis

        Returns:
            Tuple: (bool, str): validation result and message
        """

        if self.__totalWords == 0:
            if direction == "V" and not (
                x == 7 and 7 in range(y, y + word.getLengthWord() - 1)
            ):
                return False, "La primera palabra debe pasar por la casilla central (7,7)."

            elif direction == "H" and not (
                y == 7 and 7 in range(x, x + word.getLengthWord() - 1)
            ):
                return False, "La primera palabra debe pasar por la casilla central (7,7)."

        return True, ""
    
    def __isWordGoOffBoard(self, word, x, y, direction) -> tuple:
        """
        Validation of length of word cannot go off the board

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x-axis
            y (int): coordinates on the y-axis
            direction (str): "V" if the word is on the y-axis or "H" if the word is on the x-axis

        Returns:
            Tuple: (bool, str): validation result and message
        """

        if direction == "H" and (x < 0 or y < 0 or (y + word.getLengthWord() - 1) >= self.boardLen):
            return False, "La palabra sobrepasa el límite horizontal del tablero."
        elif direction == "V" and (x < 0 or y < 0 or (x + word.getLengthWord() - 1) >= self.boardLen):
            return False, "La palabra sobrepasa el límite vertical del tablero."
        
        return True, ""
    
    def __placeWordsUsingExistingBoard(self, word, x, y, direction) -> tuple:
        """
        Validation of word using have a letter that existing in board

        Args:
            word (Word): word object for validation

        Returns:
            Tuple: (bool, str): validation result and message
        """
        if self.__totalWords > 0:
            blank = 0
            
            for _ in word.word:
                if self.__board[x][y] == " ":
                    blank += 1
                
                if direction == "V":
                    x += 1
                else:
                    y += 1
            
            if blank == word.getLengthWord():
                return False, "No se está utilizando ninguna ficha del tablero"
            
        return True, ""
    
    def __putCorrectPawn(self, word, x, y, direction) -> tuple: 
        """
        Validation of Put a pawn in position empty o equal letter in position and put at least one new pawns

        Args:
            word (Word): word object for validation
            x (int): coordinates on the x-axis
            y (int): coordinates on the y-axis
            direction (str): "V" if the word is on the y-axis or "H" if the word is on the x-axis

        Returns:
            Tuple: (bool, str): validation result and message
        """
        if self.__totalWords > 0:
            hasNewPawn = False
            
            for letter in word.word:
                if self.__board[x][y] != " " and letter != self.__board[x][y]:
                    return False, "No se puede colocar una ficha en una casilla que ya esté ocupada por un ficha diferente."
                elif self.__board[x][y] == " ":
                    hasNewPawn = True
                    
                if direction == "V":
                    x += 1
                else:
                    y += 1
            
            if not hasNewPawn:
                return False, "Se debe colocar al menos una ficha nuevo en el tablero."
            
        return True, ""
    
    def __isPawnInitialInStartOrFinalOtherPawns(self, x, y, direction) -> tuple:
        """
        Validation of new pawn initial in start or final other word in board

        Args:
            x (int): coordinates on the x-axis
            y (int): coordinates on the y-axis
            direction (str): "V" if the word is on the y-axis or "H" if the word is on the x-axis

        Returns:
            Tuple: (bool, str): validation result and message
        """
        if self.__totalWords > 0:
            if direction == "V" and (x != 0 and self.__board[x - 1][y] != " "):
                return False, "Hay fichas adicionales al principio o al final de una palabra."
            elif x != 0 and self.__board[x][y - 1] != " ":
                return False, "Hay fichas adicionales al principio o al final de una palabra."
            
        return True, ""