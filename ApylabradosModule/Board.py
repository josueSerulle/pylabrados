from Word import Word
from FrequencyTable import FrequencyTable
from Pawns import Pawns

class Board:

    def __init__(self):
        self.board = [[" " for _ in range(15)] for _ in range(15)]
        self.totalWords = 0
        self.totalPawns = 0
        self.score = 0

    def showBoard(self) -> None:
        """
        show the bard game with row and column coordinate
        """

        board_len = len(self.board)

        for n in range(board_len):
            print(f" {n:02}", end=" ")
        print("\n+" + "---+" * board_len)

        for i in range(board_len):
            print("|", end=" ")
            for j in range(board_len):
                print(self.board[i][j] + " |", end=" ")
            print(f"{i:02}")
            print("+" + "---+" * board_len)

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
            if letter != self.board[x][y]:
                player_pawns.takePawn(letter)
                self.totalPawns += 1
                self.board[x][y] = letter
                self.score += Pawns.getPoinst(letter)

            if direction == "V":
                x += 1
            else:
                y += 1

        self.totalWords += 1

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
            if self.board[x][y] != letter:
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
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                for direction in ["H", "V"]:
                    print("{}:".format("Verical" if direction == "V" else "Horizontal"))
                    
                    if self.isPossible(word, x, y, direction)[0]:
                        needPawns = self.getPawns(word, x, y, direction)
                        
                        if FrequencyTable.isSubset(needPawns.getFrequency(), pawns.getFrequency()):
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

        if self.totalWords == 0:
            if direction == "V" and not (
                x == 7 and 7 in range(y, y + word.getLengthWord() - 1)
            ):
                return (False, "The first word must go through the central box (7,7).")

            elif direction == "H" and not (
                y == 7 and 7 in range(x, x + word.getLengthWord() - 1)
            ):
                return (False, "The first word must go through the central box (7,7).")

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
        
        if direction == "H" and (x < 0 or y < 0 or (y + word.getLengthWord() - 1) > 15):
            return (False, "The word goes beyond the horizontal limit of the board.")
        elif direction == "V" and (x < 0 or y < 0 or (x + word.getLengthWord() - 1) > 15):
            return (False, "The word goes beyond the vertical limit of the board.")
        
        return (True, "")
    
    def __placeWordsUsingExistingBoard(self, word) -> tuple:
        """
        Validation of word using have a letter that exinsting in board

        Args:
            word (Word): word object for validation

        Returns:
            Tuple: (bool, str): validation result and message
        """
        if self.totalWords > 0:
            boardSet = set().union(*self.board)
            wordSet = set(word.word)
            
            if not wordSet.intersection(boardSet):
                return (False, "All words, except the first, must use a tile already existing on the board.")
            
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
        if self.totalWords > 0:
            hasNewPawn = False
            
            for letter in word.word:
                if self.board[x][y] != " " and letter != self.board[x][y]:
                    return (False, "You cannot place a pawn on a square already occupied by a different pawn.")
                elif self.board[x][y] == " ":
                    hasNewPawn = True
                    
                if direction == "V":
                    x += 1
                else:
                    y += 1
            
            if not hasNewPawn:
                return (False, "At least one new pawn must be placed on the board.")
            
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
        if self.totalWords > 0:
            if direction == "V" and (x != 0 and self.board[x - 1][y] != " "):
                return (False, "There are additional pawn at the beginning or end of a word.")
            elif (x != 0 and self.board[x][y] - 1 != " "):
                return (False, "There are additional pawn at the beginning or end of a word.")
            
        return (True, "")