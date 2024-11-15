import csv
from numpy import random
from ApylabradosModule import FrequencyTable, Vertex
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt

class Pawns:
    
    points = {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 
        'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 
        'Y': 4, 'Z': 10
    }
    
    def __init__(self):
        self.__letters = []
    
    @property
    def letters(self) -> list:
        return self.__letters
    
    def addPawn(self,character) -> None:
        """
        Add a single character to the letters list.
        
        Args:
            character (str): Character to add.
        
        Raises:
            ValueError: If character is not a single character
        """
        
        if not isinstance(character, str) or len(character) != 1:
            raise ValueError("The parameter must be a single character.")
        
        self.__letters.append(character)
    
    def addPawns(self, character, repetitions) -> None:
        """
        Add the character to the letters list repeatedly.
        
        Args:
            character (str): Character to add.
            repetitions (int): Number of repetitions
        Raises:
            ValueError: If character is not a single character or repetitions is not a positive integer
        """
        if not isinstance(character, str) or len(character) != 1:
            raise ValueError("The parameter 'character' must be a single character.")
        
        if not isinstance(repetitions, int) or repetitions < 1:
            raise ValueError("The parameter 'repetitions' must be a positive integer.")
        
        for _ in range(repetitions):
            self.addPawn(character)
    
    def createBag(self, csv_path) -> None:
        """
        Creates the bag of pawns from csv file.
        
        Args:
            csv_path (path): Path to the csv file containing pawn data

        Raises:
            FileNotFoundError: Error to open csv file failed.
            ValueError: CSV file format is Incorrect.
        """
        try:
            with open(csv_path) as file:
                reader = csv.reader(file)
                
                # skip the header row
                next(reader)
                
                for row in reader:
                    if len(row) != 2:
                        raise ValueError("CSV file format is incorrect. Each row should have exactly two columns.")
                    
                    character, repetitions = row
                    
                    self.addPawns(character, int(repetitions))
        except FileNotFoundError:
            print(f"Error: the file {csv_path} was not found.")
        except ValueError as ex:
            print(f"Error: {ex}")
    
    def getFrequency(self) -> FrequencyTable:
        """
        returns a FrequencyTable object with the pawns list
        
        returns:
            FrequencyTable: FrequencyTable object
        """
        frequencyTable = FrequencyTable()
        
        for letter in self.__letters:
            frequencyTable.update(letter)
        
        return frequencyTable
        
    def showPawns(self) -> None:
        """
        Show the pawns that contained in the bag and the numbers of time each pawns is repeated
        """
        pawns_position = 4
        
        # create the plt figure
        figure = plt.figure(figsize= (8, 2))
        ax = figure.add_subplot(111)
        
        # define the limits of the axes
        ax.set_xlim(-1, 16)
        ax.set_ylim(-1, 2)
        
        # scale so that grill occupies the entire figure
        ax.set_position((0, 0, 1, 1))    
        ax.set_axis_off()
        
        for pawn in self.__letters:
            polygon = Polygon(Vertex.generateVertex(pawns_position, 0.5), color = "#FFF68F")
            ax.add_artist(polygon)
            
            ax.text(
                Vertex.transformation(pawns_position), 0.5,
                pawn, verticalalignment = "center", horizontalalignment = "center",
                fontsize = 15, fontfamily = "fantasy", fontweight = "bold", transform = ax.transAxes
            )
            
            pawns_position += 1.5
        
        plt.show()
    
    def takeRandomPawn(self) -> str:
        """
        Removes and returns a random pawn from the letters list.
        
        Returns:
            str: The randomly selected character.
        
        Raises:
            ValueError: If the letters list is empty.
        """
        random_pawn = random.choice(self.__letters)
        self.takePawn(random_pawn)
        
        return random_pawn

    def takePawn(self, character) -> None:
        """
        Take a Pawns in player's pawns bag
        
        Args:
            character (str): character for remove the pawns bag
        """
        
        self.__letters.remove(character)
    
    def getTotalPawns(self) -> int:
        """
        returns the total of pawns
        
        returns:
            int: Total of pawns
        """
        
        return len(self.__letters)
    
    @staticmethod
    def getPoints(character) -> int:
        """
        Returns the point value of a given letter.
        
        Args:
            character (str): The character (letter)
            
        Returns:
            int: The score of the letter
        """
        return Pawns.points.get(character.upper(), 0)
    
    @staticmethod
    def showPoints() -> None:
        """
        Displays the points for each letter using the getPoints method.
        """
        data = [["Letra", "Puntos"]]
        
        for letter, point in Pawns.points.items():
            data.append([letter, str(point)])
        
        #create figure and axis
        figure, ax = plt.subplots(figsize= (10, 8))
        
        plt.text(0.5, 1.05, "Puntos de cada ficha: ", ha= "center", va= "bottom", fontsize= 14, fontweight= "bold")
        
        #create a table and add the graphic
        table = ax.table(cellText= data, loc= "center", colWidths= [0.2, 0.2])
        
        # customize the table
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)
        
        #customize the color of header cell
        for (i, j), cell in table.get_celld().items():

            if i == 0:  # Headers
                cell.set_fontsize(14)
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#f1f1f1')
                if j == 1:
                    break

        ax.axis('off')
        
        plt.show()