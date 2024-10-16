class FrequencyTable():
    def __init__(self):
        self.frequencies = {chr(i):0 for i in range(ord("A"), ord("Z") + 1)}
    
    def showFrequency(self) -> None:
        """
        show the frequency when the element is different to 0
        """
        
        for character, frequency in self.frequencies.items():
            if frequency != 0:
                print(f"{character}: {frequency}")
    
    def update(self, character) -> None:
        """
        Update the frequency of chracter
        
        Args:
            character(str): The to be updated
        """
        self.frequencies[character.upper()] += 1
        
    @staticmethod
    def isSubset(freq_table1, freq_table2) -> bool:
        """
        Determinate if "freq_table1" is subSet the "freq_table2"
        
        Args:
            freq_table1(FrequencyTable): FrequencyTable object
            freq_table2(FrequencyTable): FrequencyTable object
        
        Raises:
            TypeError: the parameter must be an object of the FrequencyTable class
            
        returns:
            Bool: if "freq_table1" is subSet the "freq_table2"
        """
        
        if not (isinstance(freq_table1, FrequencyTable) and isinstance(freq_table2, FrequencyTable)):
            raise TypeError("the parameter must be an object of the FrequencyTable class")
            
        for character, freq in freq_table1.frequencies.items(): 
            if freq > freq_table2.frequencies[character]:
                return False
        return True