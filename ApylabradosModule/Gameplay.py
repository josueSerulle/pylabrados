from pathlib import Path
from ApylabradosModule import Board, Dictionary, FrequencyTable, Pawns, Vertex, Word
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt

class Gameplay:
    
    def __init__(self):
        self.__word = None
        self.__end = False
        self.__show_menu = True
        self.__show_game_option = True
        self.__player_pawns = Pawns()
        self.__bag_of_pawns = Pawns()
        self.__board = Board()
        
        self.__bag_of_pawns.createBag(Path(__file__).parent / "DataSets/bag_of_pawns.csv")
        self.__board.setMultiplier()
    
    @property
    def end(self) -> bool:
        return self.__end
    
    @property
    def bagOfPawns(self) -> Pawns:
        return self.__bag_of_pawns
    
    @property
    def board(self) -> Board:
        return self.__board
    
    def startGame(self) -> None:
        self.welcome()
        self.instructions()

    def dealPawns(self) -> None:
        """
        Deal pawns to the player until the 7
        """
        
        while self.__player_pawns.getTotalPawns() < 7:
            self.__player_pawns.addPawn(self.__bag_of_pawns.takeRandomPawn())
        
        self.__board.showBoard(self.__player_pawns.letters)

    def showMenu(self) -> None:
        """
        Displays Menu options
        """
        
        filePath = Path(__file__).parent / "DataSets/menu.txt"
        
        if self.__show_menu:
            with open(filePath) as file:
                print(file.read())

            self.__show_menu = False
        
        print("\nQue deseas hacer? {}".format("" if self.__show_menu else "(Introduce H para ver las diferentes opciones)"))
        
        option = input("Opcion: ").upper()
        
        if option == "H":
            self.__show_menu = True
        elif option == "IW":
            self.introduceNewWord()
            return None
        elif option == "MP":
            self.__player_pawns.showPawns()
        elif option == "PP":
            Pawns.showPoints()
        elif option == "L":
            self.legend()
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
        
        filePath = Path(__file__).parent / "DataSets/game_options.txt"
        
        if self.__show_game_option:
            with open(filePath) as file:
                print(file.read())

            self.__show_game_option = False
        
        print("\nQue deseas hacer? {}".format("" if self.__show_game_option else "(Introduce H para ver las diferentes opciones)"))
        
        optionGame = input("Opcion: ").upper()
        
        if optionGame == "H":
            self.__show_game_option = True
        elif optionGame == "EP":
            self.introduceCoordinatesAndDirection()
            return None
        elif optionGame == "IW":
            self.introduceNewWord()
            return None
        elif optionGame == "MP":
            self.__player_pawns.showPawns()
        elif optionGame == "PP":
            Pawns.showPoints()
        elif optionGame == "L":
            self.legend()
        elif optionGame == "HW":
            self.helpWithWords()
        elif optionGame == "HP":
            self.helpWithPosition()
        elif optionGame == "Q":
            self.endGame()
            return None
        
        self.showGameOption()
    
    def helpWithWords(self) -> None:
        """
        Shows the possible words that can be formed with the player's available pawns and
        those already placed on the board
        """
        
        print("Estas son las posibles palabras a formar:")
        
        if self.__board.totalWords == 0:
            Dictionary.showWords(self.__player_pawns)
            return None
        
        board_len = self.__board.boardLen
        board_letters = []
        
        for x in range(board_len):
            for y in range(board_len):
                if self.__board.board[x][y] != " " and  self.__board.board[x][y] not in board_letters:
                    board_letters.append(self.__board.board[x][y])
                    Dictionary.showWordPlus(self.__player_pawns, self.__board.board[x][y])
    
    def helpWithPosition(self) -> None:
        """
        Shows the possible placements on the board of the entered word
        """
        
        print("Estas son las posibles colocaciones")
        self.__board.showWordPlacement(self.__player_pawns,self.__word)
        
    def introduceNewWord(self) -> None:
        """
        Allows the user to enter a new word via the console and checks that it exists in the dictionary, 
        and that it can be formed with the pawns available to the player and those placed on the board.
        """

        self.__word = Word.readWord()
        word_ft = self.__word.getFrequency()
        player_pawns_ft = self.__player_pawns.getFrequency()
        isInDictionary = Dictionary.validationWord(self.__word)
        wordIsSubset = True
        
        if self.__board.board == 0:
            wordIsSubset = FrequencyTable.isSubset(word_ft, player_pawns_ft)
        else:
            board_len = self.__board.boardLen
            board_letters = []
            flag = False
            
            for x in range(board_len):
                for y in range(board_len):
                    
                    if self.__board.board[x][y] != " " and self.__board.board[x][y] not in board_letters:
                        board_letters.append(self.__board.board[x][y])
                        player_pawns = player_pawns_ft
                        player_pawns.update(self.__board.board[x][y])
                        
                        wordIsSubset = FrequencyTable.isSubset(word_ft, player_pawns)
                        player_pawns.delete(self.__board.board[x][y])
                        
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
        try:
            x = int(input("Introduce coordenada de la fila: "))
            y = int(input("Introduce coordenada de la columna: "))
            
            if not 0 <= x <= 14 or not 0 <= y <= 14:
                print("La coordenadas debe estar entre 0 y 14.")
                self.introduceCoordinatesAndDirection()
                return None
        except ValueError:
            print("En las coordenadas debes ingresar un número entero.")
            self.introduceCoordinatesAndDirection()
            return None
        
        direction = input("Introduce dirección: ").upper()
        
        if direction != "V" and direction != "H":
            print("Recuerda: solamente hay dos posibles direcciones para colocar las palabras: V (vertical) y H (horizontal)")
            self.introduceCoordinatesAndDirection()
            return None

        possible, message = self.__board.isPossible(self.__word, x, y, direction)
        
        if not possible:
            print(message)
            self.showGameOption()
            return None
        
        needed_pawns = self.__board.getPawns(self.__word, x, y, direction)
        
        if FrequencyTable.isSubset(needed_pawns.getFrequency(), self.__player_pawns.getFrequency()):
            self.__board.placeWord(self.__player_pawns, self.__word, x, y, direction)
            return None
        
        print("Las fichas de que dispones no son suficientes")
        self.showGameOption()

    def endGame(self) -> None:
        """
        Finish current game
        """
        
        print("Fin del juego")
        self.__end = True

    @staticmethod
    def welcome() -> None:
        """
        Display welcome message
        """

        filePath = Path(__file__).parent / "DataSets/welcome_message.txt"
        with open(filePath) as file:
            print(file.read())

    @staticmethod
    def instructions() -> None:
        """
        Display the game instructions
        """

        filePath = Path(__file__).parent / "DataSets/instructions.txt"
        with open(filePath) as file:
            print(file.read())

    @staticmethod
    def legend() -> None:
        colors = ["#FFCCCC", "#B2FFCD", "#CCCEFF", "#CCF9FF"]
        texts = ["x3\nPalabra", "x2\nPalabra", "x3\nLetra", "x2\nLetra"]

        # create the plt figure that will save to board
        figure = plt.figure(figsize=(10, 2))
        ax = figure.add_subplot(111)

        # define the limits of the axes
        ax.set_xlim(-1, 16)
        ax.set_ylim(-1, 2)

        # scale so that grill occupies the entire figure
        ax.set_position((0, 0, 1, 1))
        ax.set_axis_off()

        for i in range(4):
            polygon = Polygon(Vertex.generateVertex(1.5 + 4 * i, 0.5), color=colors[i])
            ax.add_artist(polygon)

            ax.text(
                Vertex.transformationX(3.5 + 4 * i), Vertex.transformationY(0.5), texts[i],
                verticalalignment="center", horizontalalignment="center", fontsize=25,
                fontfamily="fantasy", fontweight="bold", transform=ax.transAxes
            )

        plt.show()