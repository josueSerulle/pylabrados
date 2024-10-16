from .Word import Word

class Dictionary():
    filePath = "/content/drive/MyDrive/Colab-Notebooks/Python-Basico/Final-Project/DataSets/dictionary.txt"
    
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
        