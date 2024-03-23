class state:
    def __init__(self,name) -> None:
        self.name = name
        self.adjacencydic = {}
        self.finalState = False
    def addTransiction(self,another,transiction) -> None:
        self.adjacencydic[transiction] = another
    def removeTransiction(self,transiction) -> None:
        self.adjacencydic.pop(transiction)
    def setfinal(self):
        self.finalState = True
    def setnonfinal(self):
        self.finalState = False
    def findTransiction(self,string):
        letras = ''
        for letra in string:
            letras += letra
            if letras in self.adjacencydic:
                return letras
        return ""
    def simulate(self,input):
        if self.findTransiction(self,input):
            transiction = self.findTransiction(self,input)
            self = self.adjacencydic[transiction]
            transiction = transiction.replace
        else:
            return False
