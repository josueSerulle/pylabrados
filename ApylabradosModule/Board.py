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