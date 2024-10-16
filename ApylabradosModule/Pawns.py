import csv
from numpy import random
from .FrequencyTable import FrequencyTable

class Pawns():
    def __init__(self):
        self.letters = []
    
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
        
        self.letters.append(character)
    
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
        
        for letter in self.letters:
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
        random_pawn = random.choice(self.letters)
        self.takePawn(random_pawn)
        
        return random_pawn

    def takePawn(self, character) -> None:
        """
        Take a Pawns in player's pawns bag
        
        Args:
            character (str): character for remove the pawns bag
        """
        
        self.letters.remove(character)
    
    def getTotalPawns(self) -> int:
        """
        returns the total of pawns
        
        returns:
            int: Total of pawns
        """
        
        return len(self.letters)