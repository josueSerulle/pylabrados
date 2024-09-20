from .FrequencyTable import FrequencyTable

class Word():
    def __init__(self):
        self.word = []
    
    def areEqual(self, w):
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
            return self.word == w.word
        
        raise TypeError("the parameter must be an object of the word class")
        
    def isEmpty(self):
        """
        returns True if empty
        
        return:
            bool: if empty or not
        """
        
        return len(self.word) == 0;
    
    def getFrequency(self):
        """
        returns a FrequencyTable object with the pawns list
        
        returns:
            FrequencyTable: FrequencyTable object
        """
        frequencyTable = FrequencyTable()
        
        for word in self.word:
            frequencyTable.update(word)
        
        return frequencyTable
        
    @classmethod
    def readWord(cls):
        input_word = input("Introduce una palabra: ").strip().upper()
        word_obj = cls()
        word_obj.word = input_word
        
        return word_obj
    
    @staticmethod
    def readWordFromFile(file):
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
        return "".join(self.word)