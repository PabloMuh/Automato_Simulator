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
        if transiction in self.adjacencydic:
            self.adjacencydic.pop(transition)
            print(f"Was successfully removed the transiction")

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
def remover_por_valor(dicionario, valor):
    chaves_para_remover = []
    # Itera sobre os itens do dicionário para encontrar as chaves correspondentes ao valor
    for chave, val in dicionario.items():
        if val == valor:
            chaves_para_remover.append(chave)

    # Remove as chaves encontradas do dicionário
    for chave in chaves_para_remover:
        del dicionario[chave]
stateList = []
removekey = []
i = 0

while True:
    clear_terminal()
    print('''1 - Create State
2 - Create transiction
3 - Set final state
4 - remove state
5 - remove transiction
6 - simulate word''')
    choice = int(input("Select Your choice: "))
    if choice == 1:
        c = str(i)
        i += 1
        name = "q" + c
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
                if transiction in state1.adjacencydic:
                    print("already have this transiction")
                    enter()
                    continue
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
        removed = input("Enter the name of state to be removed: ")
        removed_state = buscar_por_nome(removed, stateList)
        if not removed_state:
            print("This state doesn't exist")
            enter()
            continue

        # Itera sobre todos os estados para remover as transições que levam ao estado removido
        for state in stateList:
            if removed_state in state.adjacencydic.values():
                remover_por_valor(state.adjacencydic,removed_state) # Remove a transição para o estado removido

        # Remove o estado da lista de estados
        stateList.remove(removed_state)
        print(f"{removed_state.name} was successfully removed")
        enter()

    elif choice == 5:
        removed = input("Enter the name of state will be removed the transiction: ")
        removed_transiction = input("enter the transiction caractere: ")
        removed_state = buscar_por_nome(removed, stateList)
        if not removed_state:
            print("This state doesn't exist")
            enter()
            continue

        removed_state.removeTransition(removed_transiction) # Remove a transição para o estado removido

        enter()
    elif choice == 6:
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
