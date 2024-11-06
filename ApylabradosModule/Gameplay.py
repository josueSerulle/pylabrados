from .Pawns import Pawns
from .Board import Board
from .Dictionary import Dictionary
from .Word import Word
from .FrequencyTable import FrequencyTable

class Gameplay:
    
    def __init__(self) -> None:
        self._word = None
        self._end = False
        self._show_menu = True
        self._show_game_option = True
        self._player_pawns = Pawns()
        self._bag_of_pawns = Pawns()
        self._board = Board()
        
        self._bag_of_pawns.createBag("DataSets/bag_of_pawns.csv")
    
    def startGame(self) -> None:
        self.welcome()
        self.instructions()
    
    def welcome(self) -> None:
        """
        Display welcome message 
        """
        
        filePath = "../Datasets/welcome_message.txt"
        with open(filePath) as file:
            print(file.read())
    
    def instructions(self) -> None:
        """
        Display the game instructions
        """
        
        filePath = "../Datasets/instructions.txt"
        with open(filePath) as file:
            print(file.read())
    
    def showMenu(self) -> None:
        """
        Displays Menu options
        """
        
        filePath = "../Datasets/menu.txt"
        
        if self._show_menu:
            with open(filePath) as file:
                print(file.read())

            self._show_menu = False
        
        print("\nQue deseas hacer? {}".format("" if self._show_menu else "(Introduce H para ver las diferentes opciones)"))
        
        option = input("Opcion: ").upper()
        
        if option == "H":
            self._show_menu = True
        elif option == "IW":
            self.introduceNewWord()
            return None
        elif option == "MP":
            print("Estas son tus fichas:")
            self._player_pawns.showPawns()
        elif option == "S":
            print("Puntos: {}".format(self._board.score))
        elif option == "PP":
            Pawns.showPoints()
        elif option == "HW":
            self.helpWithWords()
        elif option == "Q":
            self.endGame()
            return None
        
        self.showMenu()
    
    def showGameOption(self) ->  None:
        """
        Display the game options
        """
        
        filePath = "../Datasets/game_options.txt"
        
        if self._show_game_option:
            with open(filePath) as file:
                print(file.read())

            self._show_game_option = False
        
        print("\nQue deseas hacer? {}".format("" if self._show_game_option else "(Introduce H para ver las diferentes opciones)"))
        
        option = input("Opcion: ").upper()
        
        if option == "H":
            self._show_game_option = True
        elif option == "EP":
            self.introduceCoordinatesAndDirection()
            return None
        elif option == "IW":
            self.introduceNewWord()
        elif option == "MP":
            print("Estas son tus fichas:")
            self._player_pawns.showPawns()
        elif option == "S":
            print("Puntos: {}".format(self._board.score))
        elif option == "PP":
            Pawns.showPoints()
        elif option == "HW":
            self.helpWithWords()
        elif option == "HP":
            self.helpWithPosition()
        elif option == "Q":
            self.endGame()
            return None
        
        self.showGameOption()
    
    def helpWithWords(self) -> None:
        """
        Shows the possible words that can be formed with the player's available pawns and
        those already placed on the board
        """
        
        print("Estas son las posibles palabras a formar:")
        
        if self._board.totalWords == 0:
            Dictionary.showWords(self._player_pawns)
            return None
        
        board_len = len(self._board.board)
        board_letters = []
        
        for x in range(board_len):
            for y in range(board_len):
                if self._board.board[x][y] != " " and  self._board.board[x][y] not in board_letters:
                    board_letters.append(self._board.board[x][y])
                    Dictionary.showWordPlus(self._player_pawns, self._board.board[x][y])
    
    def helpWithPosition(self) -> None:
        """
        Shows the possible placements on the board of the entered word
        """
        
        print("Estas son las posibles colocaciones")
        self._board.showWordPlacement(self._player_pawns,self._word)
        
    def introduceNewWord(self) -> None:
        """
        Allows the user to enter a new word via the console and checks that it exists in the dictionary, 
        and that it can be formed with the pawns available to the player and those placed on the board.
        """

        print("Introduce tu palabra:")
        self._word = Word.readWord()
        word_ft = self._word.getFrequency()
        player_pawns_ft = self._player_pawns.getFrequency()
        isInDictionary = Dictionary.validationWord(self._word)
        
        if self._board.totalWords == 0:
            wordIsSubset = FrequencyTable.isSubset(word_ft, player_pawns_ft)
        else:
            board_len = len(self._board.board)
            board_letters = []
            flag = False
            
            for x in range(board_len):
                for y in range(board_len):
                    
                    if self._board.board[x][y] != " " and self._board.board[x][y] not in board_letters:
                        board_letters.append(self._board.board[x][y])
                        player_pawns = player_pawns_ft
                        player_pawns.update(self._board.board[x][y])
                        
                        wordIsSubset = FrequencyTable.isSubset(word_ft, player_pawns)
                        player_pawns.delete(self._board.board[x][y])
                        
                        if wordIsSubset:
                            flag = True
                            break
                
                if flag:
                    break
    
        if not isInDictionary or not wordIsSubset:
            if not wordIsSubset:
                print("No puedes formar esa palabra con tus fichas")
                
            self.showMenu()
            
            return None
        
        self.showGameOption()
    
    def introduceCoordinatesAndDirection(self) -> None:
        """
        Allows the player to input the position and orientation of a word via the console.
        Checks if the word can be placed at that location.
        """

        x = int(input("Introduce coordenada de la fila: "))
        y = int(input("Introduce coordenada de la columna: "))
        direction = input("Introduce dirección: ").upper()
        
        if direction != "V" and direction != "H":
            print("Recuerda: solamente hay dos posibles direcciones para colocar las palabras: V (vertical) y H (horizontal)")
            self.showGameOption()
            return None

        possible, message = self._board.isPossible(self._word, x, y, direction)
        
        if not possible:
            print(message)
            self.showGameOption()
            return None
        
        #### Me quede aqui
    
    def dealPawns(self) -> None:
        """
        Deal pawns to the player until the 7
        """
        
        while(self._player_pawns.getTotalPawns() < 7):
            self._player_pawns.addPawn(self._bag_of_pawns.takeRandomPawn())
        
        print("Estas son tus fichas:")
        self._player_pawns.showPawns()