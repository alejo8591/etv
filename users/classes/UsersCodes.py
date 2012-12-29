"""
this algorithm is created by Alejandro Romero @alejo8591 MIT or BSD licensed
"""
from random import randint

class UserCode(object):
    """
        Instantiate the class with the following parameters:
        :param quantity: Number of codes to return
        :param lonitude: Catidad character must have a code
    """
    def __init__(self, quantity, longitude):
        self._quantity = quantity
        self._longitude = longitude
        
    def generateCodes(self):
        self.i=0
        self.alphabet = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
        self.numeric  = ('1','2','3','4','5','5','7','8','9','0')
        self.alphanumeric = (self.alphabet, self.numeric)
        self.codes,self.position = [], 0
        for self.i in  range(self._quantity):
            self.j,self.code=0,''
            for self.j in range(self._longitude):
                self.option = randint(0,1)
                if self.option == 0: self.code += self.alphanumeric[self.option][randint(0,25)]
                else:self.code += self.alphanumeric[self.option][randint(0,9)]
            self.codes.append(self.code)
        return self.codes