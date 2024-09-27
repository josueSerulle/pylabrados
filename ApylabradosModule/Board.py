class Board:
    def __init__(self):
        self.board = [[" " for _ in range(15)] for _ in range(15)]
        self.totalWords = 0
        self.totalPawns = 0

    def showBoard(self):
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

    def placeWord(self, player_pawns, word, x, y, direction):
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

            if direction == "V":
                x += 1
            else:
                y += 1

        self.totalWords += 1

    def isPossible(self, word, x, y, direction):
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

        validation = self.__firstPawnIsCentralPosition(word, x, y, direction)

        if validation[0]:
            return validation

        return (True, "")

    def __firstPawnIsCentralPosition(self, word, x, y, direction):
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
                x == 7 and 7 in range(y, y + word.getLengthWord())
            ):
                return (False, "The first word must go through the central box (7,7).")

            elif direction == "H" and not (
                y == 7 and 7 in range(x, x + word.getLengthWord())
            ):
                return (False, "The first word must go through the central box (7,7).")

        return (True, "")
