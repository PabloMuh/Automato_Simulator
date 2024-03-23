import os

def clear_terminal():
    # Verifica qual é o sistema operacional
    if os.name == 'nt':  # Windows
        os.system('cls')
def enter():
    input()


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
def buscar_por_nome(name, lista):
    resultado = list(filter(lambda x: x.name == name, lista))
    return resultado[0] if resultado else None

stateList = []

while True:
    clear_terminal()
    print('''1 - Create State
2 - Create transiction
3 - Set final state
4 - simulate word''')
    choice = int(input("Select Your choice: "))
    if choice == 1:
        name = input("Enter the State name: ")
        newState = State(name)
        stateList.append(newState)
        print(f"{name} was created")
        enter()

    elif choice == 2:

        name1 = input("Enter the name of a1: ")

        if name1:
            state1 = buscar_por_nome(name1,stateList)
            if not state1:
                continue
        
        name2 = input("Enter the name of a2: ")
        transiction = input("Enter the transiction: ")
        if name2:
            state2 = buscar_por_nome(name2,stateList)
            if state2:
                state1.addTransition(state2,transiction)
                print(f"Transiction between {name1} and {name2} is {transiction}")
            else:
                print("Fail")
            enter()
    elif choice == 3:
        final = input("Enter the name of final state: ")
        stateFinal = buscar_por_nome(final,stateList)
        if stateFinal:
            stateFinal.setFinal()
            print(f"{stateFinal.name} is now final")
            enter()
    elif choice == 4:
        starter = input("Enter the name of initial State: ")
        entry = input("Enter your input: ")
        stateInitial = buscar_por_nome(starter,stateList)
        if stateInitial.simulate(entry):
            print("The word was accepted")
        else:
            print("the word was rejected")
        enter()
    else:
        break
