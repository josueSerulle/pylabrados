from .FrequencyTable import FrequencyTable

class Word():
    def __init__(self):
        self.__word = []
    
    @property
    def word(self) -> list:
        return self.__word
    
    @word.setter
    def word(self, word) -> None:
        self.__word = word
        
    def areEqual(self, w) -> bool:
        """
        returns True if they are equal
        
        Args:
            w (Word): Word object
        
        Raises:
            TypeError: the parameter must be an object of the word class
        
        return:
            bool: if equal or not
        """
        if isinstance(w, Word):
            return self.__word == w.word
        
        raise TypeError("the parameter must be an object of the word class")
    
    def isEmpty(self) -> bool:
        """
        returns True if empty
        
        return:
            bool: if empty or not
        """
        
        return len(self.__word) == 0
    
    def getFrequency(self) -> FrequencyTable:
        """
        returns a FrequencyTable object with the pawns list
        
        returns:
            FrequencyTable: FrequencyTable object
        """
        frequencyTable = FrequencyTable()
        
        for word in self.__word:
            frequencyTable.update(word)
        
        return frequencyTable
    
    def getLengthWord(self) -> int:
        """
        returns the length of word
        
        returns:
            int: length of word
        """
        
        return len(self.__word)

    @classmethod
    def readWord(cls) -> 'Word':
        input_word = input("Introduce una palabra: ").strip().upper()
        word_obj = cls()
        word_obj.word = list(input_word)
        
        return word_obj
    
    @staticmethod
    def readWordFromFile(file) -> 'Word':
        """"
        Read the word in file line
        
        Args:
            file (io.TextIOWrapper): file for read
        
        returns:
            Word: Word Object
        """
        
        w = Word()
        file_word = file.readline()

        for c in file_word[:-1]:
            w.word.append(c)
        return w
        
    def __str__(self):
        return "".join(self.__word)