class Board():
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
        print(f" {n:02}", end = " ")
      print("\n+" + "---+" * board_len)
      
      for i in range(board_len):
        print("|", end = " ")
        for j in range(board_len):
          print(self.board[i][j] + " |", end = " ")
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
        x +=  1
      else:
        y += 1
    
    self.totalWords += 1