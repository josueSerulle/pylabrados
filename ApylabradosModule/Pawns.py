import csv
from numpy import random
from .FrequencyTable import FrequencyTable

class Pawns():
    
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
        Createss the bag of pawns from csv file.
        
        Args:
            csv_path (str): Path to the csv file containing pawn data

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
                    
                    chracter, repetitions = row
                    
                    self.addPawns(chracter, int(repetitions))
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
        
        frequrncyTable = self.getFrequency()
        frequrncyTable.showFrequency()
    
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
        count = 0
        end = " "
        
        print("Puntos de cada ficha: ")
        
        for letter, point in Pawns.points.items():
            print("{}:{}{}".format(letter, " " if point < 9 else "", point), end= end)
            count += 1
            end = "\n" if count % 3 == 2 else " "