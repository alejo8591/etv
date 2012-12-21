"""
this algorithm is created by Alejandro Romero @alejo8591 MIT or BSD licensed
"""
from random import randint

class UserCode:
    def __init__(self):
        return
    
    def generateCodes(self, identification):
        i=0
        alphabet = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
        numeric  = ('1','2','3','4','5','5','7','8','9','0')
        alphanumeric = (alphabet, numeric)
        codes,position = [], 0
        for i in  range(20):
            j,code=0,''
            for j in range(8):
                option = randint(0,1)
                if option == 0: code += alphanumeric[option][randint(0,25)]
                else:code += alphanumeric[option][randint(0,9)]
            codes.append(code)
        return codes