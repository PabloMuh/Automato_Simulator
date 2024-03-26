import pygame
import sys
import math

# Inicializando o Pygame
pygame.init()

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW_LIGHT = (255, 255, 204)
RED= (250,128,114)
GREEN= (0,255,127)
BUTTON_ACTIVE_COLOR = (100, 100, 100)

# Definindo constantes
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
RADIUS = 30

# Inicializando a janela
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('FlapJack')

# Lista para armazenar os estados e suas coordenadas
states = []

# Lista para armazenar as transições e seus símbolos
transitions = []
transictions = []

# Lista para armazenar os estados finais
final_states = set()

# Variável para armazenar o estado inicial
initial_state = None

# Definindo a posição da barra de ferramentas
TOOLBAR_HEIGHT = 50

# Definindo cores da barra de ferramentas
TOOLBAR_COLOR = (200, 200, 200)
BUTTON_COLOR = (150, 150, 150)

# Definindo fonte para os botões
font = pygame.font.SysFont(None, 20)

# Variável para armazenar o texto digitado pelo usuário
input_text = ""

# Função para desenhar a barra de ferramentas
def draw_toolbar():
    pygame.draw.rect(window, TOOLBAR_COLOR, (0, 0, WINDOW_WIDTH, TOOLBAR_HEIGHT))

    # Desenhar botão de criar estado
    create_state_button = pygame.Rect(10, 10, 40, 30)
    pygame.draw.rect(window, BUTTON_COLOR, create_state_button)
    pygame.draw.circle(window, BLACK, (create_state_button.x + 20, create_state_button.y + 15), 10)

    # Desenhar botão de criar transição
    create_transition_button = pygame.Rect(60, 10, 40, 30)
    pygame.draw.rect(window, BUTTON_COLOR, create_transition_button)
    pygame.draw.line(window, BLACK, (create_transition_button.x + 5, create_transition_button.y + 15),
                     (create_transition_button.x + 35, create_transition_button.y + 15), 3)

    # Desenhar botão de apagar estado ou transição
    delete_button = pygame.Rect(110, 10, 40, 30)
    pygame.draw.rect(window, BUTTON_COLOR, delete_button)
    draw_text("L", BLACK, delete_button.x + 13, delete_button.y + 5)

    # Botão para definir o estado inicial 
    set_initial_button = pygame.Rect(160, 10, 80, 30)
    pygame.draw.rect(window, BUTTON_COLOR, set_initial_button)
    draw_text("inicial", BLACK, set_initial_button.x + 10, set_initial_button.y + 5)

    # botão estado final 
    set_final_button = pygame.Rect(250, 10, 80, 30)
    pygame.draw.rect(window, BUTTON_COLOR, set_final_button)
    draw_text(" final", BLACK, set_final_button.x + 10, set_final_button.y + 5)

    # Botão para testar palavra
    test_word_button = pygame.Rect(340, 10, 120, 30)
    pygame.draw.rect(window, BUTTON_COLOR, test_word_button)
    draw_text("    Teste", BLACK, test_word_button.x + 10, test_word_button.y + 5)

    # Botão para executar step_test_word
    step_test_button = pygame.Rect(470, 10, 120, 30)
    pygame.draw.rect(window, BUTTON_COLOR, step_test_button)
    draw_text("Step Test", BLACK, step_test_button.x + 10, step_test_button.y + 5)

    return create_state_button, create_transition_button, delete_button, set_initial_button, set_final_button, test_word_button, step_test_button


# Função para desenhar os estados
def draw_states():
    for state in states:
        position, name, is_initial = state
        color = YELLOW_LIGHT if not is_initial else (255, 153, 153)  # Vermelho claro para estados iniciais
        if name in final_states:
            border_color = (0, 0, 0)
            pygame.draw.circle(window, border_color, position, RADIUS + 5, 3)  # Desenha uma borda mais grossa para estados finais
        pygame.draw.circle(window, color, position, RADIUS)
        text_surface = font.render(name, True, BLACK)
        text_rect = text_surface.get_rect(center=position)
        window.blit(text_surface, text_rect)
        if is_initial:
            draw_initial_arrow(position)

# Função para desenhar os estados iniciais
def draw_initial_arrow(position):
    # Desenhar triângulo apontando para a esquerda
    pygame.draw.polygon(window, BLACK, [(position[0] - RADIUS, position[1]), 
                                         (position[0] - RADIUS - 20, position[1] - 10), 
                                         (position[0] - RADIUS - 20, position[1] + 10)])

# Função para desenhar as transições
def draw_transitions():
    state_positions = {state[1]: state[0] for state in states}  # Dicionário que mapeia nome do estado para posição

    for transition in transitions:
        start_state_name = transition[0]
        end_state_name = transition[1]
        symbol = transition[2]

        # Verificar se os estados de início e fim estão presentes no dicionário
        if start_state_name in state_positions and end_state_name in state_positions:
            start_pos = state_positions[start_state_name]
            end_pos = state_positions[end_state_name]

            if start_state_name == end_state_name:  # Se for um loop
                # Calcular a posição final da seta de loop
                end_arrow = (start_pos[0] + RADIUS * math.cos(math.pi / 4), start_pos[1] - RADIUS * math.sin(math.pi / 4))

                # Desenhar a linha curva do loop
                pygame.draw.arc(window, BLACK, (start_pos[0] - RADIUS, start_pos[1] - RADIUS, RADIUS * 2, RADIUS * 2), math.pi / 4, 3 * math.pi / 2, 2)

                # Desenhar seta direcional do loop
                dx = end_arrow[0] - start_pos[0]
                dy = end_arrow[1] - start_pos[1]
                angle = math.atan2(dy, dx)
                end_arrow_head = (end_arrow[0] - 10 * math.cos(angle), end_arrow[1] - 10 * math.sin(angle))
                pygame.draw.polygon(window, BLACK, ((end_arrow[0], end_arrow[1]),
                                                     (end_arrow_head[0] + 5 * math.sin(angle + 0.4), end_arrow_head[1] + 5 * math.cos(angle + 0.4)),
                                                     (end_arrow_head[0] - 5 * math.sin(angle + 0.4), end_arrow_head[1] - 5 * math.cos(angle + 0.4))))

                # Exibir o símbolo da transição no meio do loop
                text_surface = font.render(symbol, True, BLACK)
                text_rect = text_surface.get_rect(center=((start_pos[0] + end_arrow[0]) // 2, (start_pos[1] + end_arrow[1]) // 2))
                window.blit(text_surface, text_rect)
            else:  # Se não for um loop
                # Calcular coordenadas médias para o texto
                text_x = (start_pos[0] + end_pos[0]) // 2
                text_y = (start_pos[1] + end_pos[1]) // 2

                # Ajustar a posição do texto para cima
                text_y -= 10  # Subtrair 10 pixels para mover o texto para cima

                # Exibir o símbolo da transição
                text_surface = font.render(symbol, True, BLACK)
                text_rect = text_surface.get_rect(center=(text_x, text_y))
                window.blit(text_surface, text_rect)

                # Desenhar linha entre os estados
                pygame.draw.line(window, BLACK, start_pos, end_pos, 2)

                # Desenhar seta direcional
                dx = end_pos[0] - start_pos[0]
                dy = end_pos[1] - start_pos[1]
                angle = math.atan2(dy, dx)
                end_arrow = (end_pos[0] - 15 * math.cos(angle), end_pos[1] - 15 * math.sin(angle))
                pygame.draw.polygon(window, BLACK, ((end_pos[0], end_pos[1]),
                                                     (end_arrow[0] + 10 * math.sin(angle + 0.4),
                                                      end_arrow[1] + 10 * math.cos(angle + 0.4)),
                                                     (end_arrow[0] - 10 * math.sin(angle + 0.4),
                                                      end_arrow[1] - 10 * math.cos(angle + 0.4))))



# Função para desenhar texto
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    window.blit(text_surface, (x, y))
def step_test_word(command):
    i = 2
    running = True
    vertical_offset = 150  # Valor para ajustar a posição vertical dos elementos

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if forward.collidepoint(pos):
                    if i > 50:
                        running = False
                    else:
                        try:
                            print("espaco")
                            print(command[i], command[i + 1], command[1 + 2], command[i + 3], command[i + 4])
                            pygame.draw.rect(window, command[i + 2], (command[i], 10 + vertical_offset, 100, 100))
                            pygame.draw.rect(window, BLACK, (command[i], 10 + vertical_offset, 100, 100), 2)
                            draw_text(f"Fita: {command[i + 3]}", BLACK, command[i + 1], 30 + vertical_offset)
                            draw_text(f"Estado: {command[i + 4]}", BLACK, command[i + 1], 60 + vertical_offset)
                            i += 5
                            pygame.display.update()  # Atualiza apenas a área modificada
                        except IndexError:
                            running = False
        # Redesenhe todos os elementos
        pygame.draw.rect(window, WHITE, (10, 10 + vertical_offset, 100, 100))
        pygame.draw.rect(window, BLACK, (10, 10 + vertical_offset, 100, 100), 2)
        draw_text(f"Fita: {command[0]}", BLACK, 20, 30 + vertical_offset)
        draw_text(f"Estado: {command[1]}", BLACK, 20, 60 + vertical_offset)
        forward = pygame.Rect(360, 10 , 120, 30)
        pygame.draw.rect(window, BUTTON_COLOR, forward)
        draw_text("Next", BLACK, forward.x + 10, forward.y + 5 )
        pygame.display.update()


def test_word2(word):
    current_state = initial_state  # Inicializa o estado atual com o estado inicial do autômato
    block_space=100
    text_space=110
    boxes=1
    command_list=[word, current_state]
    # Itera sobre cada símbolo da palavra
    for symbol in word:
        found_transition = False  # Variável para indicar se foi encontrada uma transição válida para o símbolo atual
        for transition in transitions:
            # Verifica se a transição é válida para o estado atual e o símbolo atual
            if transition[0] == current_state and transition[2] == symbol:
                current_state = transition[1]  # Atualiza o estado atual para o estado de destino da transição
                found_transition = True  # Marca que uma transição válida foi encontrada

                break  # Interrompe o loop assim que uma transição válida é encontrada

        command =[boxes*block_space+20, boxes*block_space+30, 'WHITE', word, current_state]
        command_list.extend(command)
        boxes+=1
        # Se nenhuma transição válida for encontrada para o símbolo atual, a palavra é rejeitada
        if not found_transition:
            command =[boxes*block_space+20,boxes*text_space, 'RED', word, current_state]
            command_list.extend(command)
            step_test_word(command_list)
            return False
    command =[boxes*block_space+20,boxes*text_space, 'GREEN', word, current_state]
    command_list.extend(command)
    step_test_word(command_list)
    # Verifica se o estado atual após processar toda a palavra é um estado final
    return current_state in final_states        
    
def test_word(word):
    current_state = initial_state  # Inicializa o estado atual com o estado inicial do autômato
    # Itera sobre cada símbolo da palavra
    for symbol in word:
        found_transition = False  # Variável para indicar se foi encontrada uma transição válida para o símbolo atual
        
        # Itera sobre cada transição definida no autômato
        for transition in transitions:
            # Verifica se a transição é válida para o estado atual e o símbolo atual
            if transition[0] == current_state and transition[2] == symbol:
                current_state = transition[1]  # Atualiza o estado atual para o estado de destino da transição
                found_transition = True  # Marca que uma transição válida foi encontrada
                break  # Interrompe o loop assim que uma transição válida é encontrada
        
        # Se nenhuma transição válida for encontrada para o símbolo atual, a palavra é rejeitada
        if not found_transition:
            return False
    # Verifica se o estado atual após processar toda a palavra é um estado final
    return current_state in final_states
def get_user_input():
    user_input = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        window.fill(WHITE)
        draw_text("palavra:", BLACK, 90, 10)
        pygame.draw.rect(window, WHITE, (150, 5, 200, 30))
        pygame.draw.rect(window, BLACK, (150, 5, 200, 30), 2)
        draw_text(user_input, BLACK, 160, 10)
        draw_text("Pressione Enter para testar a palavra", BLACK, 10, 550)
        pygame.display.flip()
    return user_input
def get_user_input_2():
    user_input = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if step_test_word_button.collidepoint(pos):
                    test_word2(user_input)

        window.fill(WHITE)
        draw_text("Palavra:", BLACK, 90, 10)
        pygame.draw.rect(window, WHITE, (150, 5, 200, 30))
        pygame.draw.rect(window, BLACK, (150, 5, 200, 30), 2)
        draw_text(user_input, BLACK, 160, 10)
        step_test_word_button = pygame.Rect(360, 10, 120, 30)
        pygame.draw.rect(window, BUTTON_COLOR, step_test_word_button)
        draw_text("StepTeste", BLACK, step_test_word_button.x + 10, step_test_word_button.y + 5)
        draw_text("Pressione Enter para voltar", BLACK, 10, 550)
            
        pygame.display.flip()
    return user_input

# Função principal do programa
def main():
    global states, transitions, input_text, final_states, initial_state, word_test_result, step_test_word_result

    word_test_result = ""  # Inicializar a variável word_test_result

    running = True
    create_state_active = False
    create_transition_active = False
    delete_active = False
    set_initial_active = False
    set_final_active = False
    start_state = None

    while running:
        window.fill(WHITE)

        create_state_button, create_transition_button, delete_button, set_initial_button, set_final_button, test_word_button, step_test_button = draw_toolbar()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if create_state_button.collidepoint(pos):
                    create_state_active = not create_state_active
                    create_transition_active = False
                    delete_active = False
                    set_initial_active = False
                    set_final_active = False
                    
                elif create_transition_button.collidepoint(pos):
                    create_transition_active = not create_transition_active
                    create_state_active = False
                    delete_active = False
                    set_initial_active = False
                    set_final_active = False

                elif delete_button.collidepoint(pos):
                    delete_active = not delete_active
                    create_state_active = False
                    create_transition_active = False
                    set_initial_active = False
                    set_final_active = False

                elif set_initial_button.collidepoint(pos):
                    set_initial_active = not set_initial_active
                    create_state_active = False
                    create_transition_active = False
                    delete_active = False
                    set_final_active = False

                elif set_final_button.collidepoint(pos):
                    set_final_active = not set_final_active
                    set_initial_active = False
                    create_state_active = False
                    create_transition_active = False
                    delete_active = False

                elif create_state_active:
                    state_name = f'q{len(states)}'  # Nome do estado com prefixo "q" minúsculo e número
                    states.append((pos, state_name, False))
                
                #monta a tupla de transiçoes 
                elif create_transition_active:
                    if start_state is None:
                        for state in states:
                            if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                        RADIUS * 2).collidepoint(pos):
                                start_state = state[1]  # Armazena o nome do estado de início
                                break
                    else:
                        for state in states:
                            if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                        RADIUS * 2).collidepoint(pos):
                                transitions.append((start_state, state[1], input_text))  # Armazena o nome dos estados de início e fim
                                start_state = None
                                input_text = ""  # Limpar o texto de entrada

                                # Calcular o ponto médio entre os centros dos estados de início e fim
                                text_x = (state[0][0] + states[states.index((state[0], state[1], False))][0][0]) // 2
                                text_y = (state[0][1] + states[states.index((state[0], state[1], False))][0][1]) // 2
                                break

                elif delete_active:
                    state_positions = {state[1]: state[0] for state in states}  # Dicionário que mapeia nome do estado para posição

                    # Verifica se o clique foi em um estado
                    for state in states:
                        # Corrigindo a criação do retângulo para verificar colisões com o mouse
                        if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2, RADIUS * 2).collidepoint(pos):
                            # Remove o estado da lista de estados
                            states.remove(state)
                            # Remove o estado da lista de estados finais, se estiver presente
                            if state[1] in final_states:
                                final_states.remove(state[1])
                            # Remove o estado inicial, se for o estado removido
                            if state[1] == initial_state:
                                initial_state = None
                            # Remove também as transições que partem ou chegam nesse estado
                            transitions = [t for t in transitions if t[0] != state[1] and t[1] != state[1]]
                            break

                    # Verifica se o clique foi em uma linha de transição
                    for transition in transitions:
                        start_pos = state_positions[transition[0]]
                        end_pos = state_positions[transition[1]]
                        width = abs(end_pos[0] - start_pos[0])
                        height = abs(end_pos[1] - start_pos[1])
                        if pygame.Rect(start_pos[0], start_pos[1], width, height).collidepoint(pos):
                            # Remove a transição da lista de transições
                            transitions.remove(transition)
                            break


                elif set_initial_active:
                    for i, state in enumerate(states):
                        if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                       RADIUS * 2).collidepoint(pos):
                            initial_state = state[1]
                            states[i] = (state[0], state[1], True)
                            break

                elif set_final_active:
                    for state in states:
                        if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                       RADIUS * 2).collidepoint(pos):
                            if state[1] in final_states:
                                final_states.remove(state[1])
                            else:
                                final_states.add(state[1])
                            break

                elif test_word_button.collidepoint(pos):
                    word= get_user_input()  # Abrir janela para entrada de palavra
                    if word==False:
                        running=False
                    else:
                        word_test_result = "Aceita" if test_word(word) else "Rejeitada"
                elif step_test_button.collidepoint(pos):
                    word= get_user_input_2()  # Abrir janela para entrada de palavra
                    if word==False:
                        running=False
                    else:
                        word_test_result = "Aceita" if test_word(word) else "Rejeitada"

            elif event.type == pygame.KEYDOWN:
                if create_transition_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        for state in states:
                            if pygame.Rect(state[0][0] - RADIUS, state[0][1] - RADIUS, RADIUS * 2,
                                           RADIUS * 2).collidepoint(pygame.mouse.get_pos()):
                                transitions.append((start_state, state[0], input_text))
                                start_state = None
                                input_text = ""  # Limpar o texto de entrada
                                break
                    else:
                        input_text += event.unicode

        if create_state_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, create_state_button)
        if create_transition_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, create_transition_button)
            # Desenhar a caixa de entrada de texto para o símbolo da transição
            pygame.draw.rect(window, WHITE, (160, 55, 100, 30))
            pygame.draw.rect(window, BLACK, (160, 55, 100, 30), 2)
            draw_text(input_text, BLACK, 170, 60)

        if delete_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, delete_button)
        if set_initial_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, set_initial_button)
        if set_final_active:
            pygame.draw.rect(window, BUTTON_ACTIVE_COLOR, set_final_button)

        draw_states()
        draw_transitions()

        # Exibir o resultado do teste da palavra
        draw_text(f"Resultado do teste: {word_test_result}", BLACK, 10, WINDOW_HEIGHT - 30)


        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()