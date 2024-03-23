class State:
    def __init__(self, name) -> None:
        self.name = name
        self.adjacencydic = {}
        self.finalState = False

    def addTransition(self, another, transition) -> None:
        self.adjacencydic[transition] = another

    def removeTransition(self, transition) -> None:
        self.adjacencydic.pop(transition)

    def setFinal(self):
        self.finalState = True

    def setNonFinal(self):
        self.finalState = False

    def findTransition(self, string):
        letters = ''
        for letter in string:
            letters += letter
            if letters in self.adjacencydic:
                return letters
        return ""

    def removeFirstCharacter(self, string):
        return string[1:]

    def simulate(self, input_str):

        current_state = self
        remaining_input = input_str

        while remaining_input:
            transition = current_state.findTransition(remaining_input)
            if transition:
                current_state = current_state.adjacencydic[transition]
                remaining_input = self.removeFirstCharacter(remaining_input)
            else:
                return False

        if current_state.finalState:
            return True
        else:
            return False
# Exemplo de uso:
# Defina seus estados, transições e estados finais antes de usar o método simulate
