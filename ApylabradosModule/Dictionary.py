from pathlib import Path
from ApylabradosModule import Word, FrequencyTable

class Dictionary():
    filePath = Path(__file__).parent / "DataSets/dictionary.txt"
    
    @staticmethod
    def validationWord(word) -> bool:
        """
        Validate if the word exists in the dictionary
        
        Args:
            word (Word): the word validate
        
        FileNotFoundError: The file no found in path
        
        returns:
            bool: if word exists
        """
        
        try:
            with open(Dictionary.filePath) as file:
                w = Word.readWordFromFile(file)
                
                while (not w.isEmpty() and not word.areEqual(w)):
                    w = Word.readWordFromFile(file)
            
            if w.isEmpty() and not word.areEqual(w):
                print("La palabra no se encuentra en el diccionario")
                return False
        
            return True
        
        except FileNotFoundError:
            print(f"The file no found in path {Dictionary.filePath}")
            return False
    
    @staticmethod
    def showWords(pawns) -> None:
        """
        Displays all possible words that can be formed with the given tiles.
        
        Args:
            pawns (Pawns): The player's tiles
        """
        availableLetters = pawns.getFrequency()
        count = 0
        end = " "
        
        with open(Dictionary.filePath) as file:
            word = Word.readWordFromFile(file)
            
            while (not word.isEmpty()):
                n = word.getLengthWord()
                wordFrequency = word.getFrequency()
                
                if FrequencyTable.isSubset(wordFrequency, availableLetters):
                    print(word, end = end * (10 - n) if end == " " else end)
                    count += 1
                    end = "\n" if count % 5 == 4 else " "
                
                word = Word.readWordFromFile(file)
    
    @staticmethod
    def showWordPlus(pawns, character) -> None:
        """
        Displays all possible words containing the specified character
        that can be formed with the given pawns.
        
        Args:
            pawns (Pawns): The player's pawns
            character (str): The specified character
        """
        
        availableLetters = pawns.getFrequency()
        availableLetters.update(character)
        count = 0
        end = " "
        
        with open(Dictionary.filePath) as file:
            word = Word.readWordFromFile(file)
            
            while (not word.isEmpty()):
                n = word.getLengthWord()
                
                if character in word.word:
                    wordFrequency = word.getFrequency()
                
                    if FrequencyTable.isSubset(wordFrequency, availableLetters):
                        print(word, end = end * (10 - n) if end == " " else end)
                        count += 1
                        end = "\n" if count % 5 == 4 else " "
                        
                word = Word.readWordFromFile(file)
