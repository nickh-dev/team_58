import pygame 
import sys
import random

pygame.init()

screen_width, screen_height = 850, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game with Alpha-Beta Pruning')

# Define colors
BACKGROUND_COLOR = (41, 47, 54)
BUTTON_COLOR = (255, 87, 34)
BUTTON_HOVER_COLOR = (255, 138, 101)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0, 100)
font = pygame.font.Font(None, 36)



#Draws a button with text on the screen and detects clicks
def draw_button(text, position, active_color, inactive_color, screen):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(position[0], position[1], 200, 80)
    shadow_rect = button_rect.move(6, 6)
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect)
    pygame.draw.rect(screen, inactive_color if button_rect.collidepoint(mouse) else active_color, button_rect, border_radius=10)  # Main body of button with rounded corners

    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    return button_rect.collidepoint(mouse) and click[0] == 1



#Displays the main menu and handles the algorithm selection.
def main_menu():
    chosen_algorithm = None
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        start_button_clicked = draw_button('START', (screen_width // 2 - 100, 100), BUTTON_COLOR, BUTTON_HOVER_COLOR, screen)
        quit_button_clicked = draw_button('EXIT', (screen_width // 2 - 100, 200), BUTTON_COLOR, BUTTON_HOVER_COLOR, screen)

        if draw_button('Minimax', (screen_width // 2 - 100, 300), BUTTON_COLOR, BUTTON_HOVER_COLOR, screen):
            chosen_algorithm = "minimax"
        elif draw_button('Alpha-Beta', (screen_width // 2 - 100, 400), BUTTON_COLOR, BUTTON_HOVER_COLOR, screen):
            chosen_algorithm = "alphabeta"
        elif draw_button('Random', (screen_width // 2 - 100, 500), BUTTON_COLOR, BUTTON_HOVER_COLOR, screen):
            chosen_algorithm = "random"

        if start_button_clicked and chosen_algorithm is not None:
            start_number = start_menu()
            game_loop(start_number, chosen_algorithm)
            running = False

        if quit_button_clicked:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()



#Allows the player to choose a starting number
def start_menu():
    input_number = ''
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        title_text = font.render('Choose a starting number (25 to 40): ' + input_number, True, TEXT_COLOR)
        screen.blit(title_text, (screen_width // 2 - 250, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_number = input_number[:-1]
                elif event.key == pygame.K_RETURN:
                    if 25 <= int(input_number) <= 40:
                        return int(input_number)
                    else:
                        input_number = ''
                else:
                    if event.unicode.isdigit() and len(input_number) < 2:
                        input_number += event.unicode

        pygame.display.flip()

#Calculates points and updates the bank based on the current number.
def update_points_and_bank(number):
    points = 0
    bank = 0
    if number % 2 == 0:
        points -= 1
    else:
        points += 1
    
    if number % 10 == 0 or number % 10 == 5:
        bank += 1
    
    return points, bank

#Displays the end game screen showing final scores
def display_end_game_screen(player_points, ai_points, game_bank, log_messages):
    screen.fill(BACKGROUND_COLOR)
    result_text = f"Player points: {player_points}, AI points: {ai_points}, Bank: {game_bank}"
    result_msg = font.render(result_text, True, TEXT_COLOR)
    screen.blit(result_msg, (screen_width // 2 - result_msg.get_width() // 2, 20))

    log_start_y = 60
    for i, log_message in enumerate(log_messages[-15:], start=1):
        log_text = font.render(log_message, True, TEXT_COLOR)
        screen.blit(log_text, (50, log_start_y + i * 20))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()

        restart_button_clicked = draw_button('RESTART', (screen_width // 2 - 100, 800), BUTTON_COLOR, BUTTON_HOVER_COLOR, screen)
        if restart_button_clicked:
            waiting = False

        pygame.display.flip()

    main_menu()  # Перезапуск игры после выхода из цикла





class Node:
    def __init__(self, current_number, ai_points, player_points, game_bank, depth, is_maximizing, multiplier=None,is_ai_turn=True):
        self.current_number = current_number #The current number in the game state
        self.ai_points = ai_points #The AI's points.
        self.player_points = player_points #The player's points. 
        self.game_bank = game_bank # Bank points
        self.depth = depth #depth of this node in the game tree
        self.is_maximizing = is_maximizing #goal at this node is to maximize points (AI's turn) or minimize (player's turn).
        self.multiplier = multiplier #multiplier, used to modify calculations in the game logic.
        self.children = [] # children list
        self.is_ai_turn = is_ai_turn # Indicates if it's currently the AI's turn at this game state.
    def add_child(self, child):
        self.children.append(child) #add a child Node to the children list, forming parent-child relationships in the tree structure.



#Evaluates the current state of the game for AI.                    
def evaluate(current_number, ai_points, player_points, game_bank,  is_ai_turn):
    A = 1
    B = 1
    C = 0.001
    base_score = A * (ai_points - player_points) + B * game_bank - C * abs(5000 - current_number)

    if current_number >= 5000:
        return float('inf') if is_ai_turn else float('-inf')
    else:
        return base_score




# minimax algorithm    
def minimax(node, depth, is_maximizing):
    if node.current_number >= 5000 or depth == 0:
        score = evaluate(node.current_number, node.ai_points, node.player_points, node.game_bank,  node.is_ai_turn)

        #print(f"Minimax: Depth {depth}, Score: {score}, Maximizing: {is_maximizing}")
        return score, None
    
    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = node.current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_node = Node(new_number, node.ai_points + points, node.player_points, node.game_bank + bank, node.depth + 1, False, multiplier)
            print(f"Minimax: Creating node at depth {new_node.depth} with current_number {new_node.current_number}, ai_points {new_node.ai_points}, player_points {new_node.player_points}, game_bank {new_node.game_bank}, is_maximizing {new_node.is_maximizing}, multiplier {new_node.multiplier}")
            score, _ = minimax(new_node, depth-1, False)
            if score > best_score:
                best_score = score
                best_move = multiplier
        print(f"Minimax: Depth {depth}, Best Score: {best_score}, Best Move: {best_move}, Maximizing: {is_maximizing}")
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = node.current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_node = Node(new_number, node.ai_points, node.player_points + points, node.game_bank + bank, node.depth + 1, True, multiplier)
            score, _ = minimax(new_node, depth-1, True)
            if score < best_score:
                best_score = score
                best_move = multiplier
        print(f"Minimax: Depth {depth}, Best Score: {best_score}, Best Move: {best_move}, Maximizing: {is_maximizing}")
        return best_score, best_move
    



# alphabeta algorithm 
def alphabeta(node, depth, alpha, beta, is_maximizing):
    if node.current_number >= 5000 or depth == 0:
        score = evaluate(node.current_number, node.ai_points, node.player_points, node.game_bank, node.is_ai_turn)
        return score, None
    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = node.current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_node = Node(new_number, node.ai_points + points, node.player_points, node.game_bank + bank, node.depth + 1, False, multiplier)
            #print(f"AlphaBeta: Creating node at depth {new_node.depth} with current_number {new_node.current_number}, ai_points {new_node.ai_points}, player_points {new_node.player_points}, game_bank {new_node.game_bank}, is_maximizing {new_node.is_maximizing}, multiplier {new_node.multiplier}")
            score, _ = alphabeta(new_node, depth-1, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = multiplier
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = node.current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_node = Node(new_number, node.ai_points, node.player_points + points, node.game_bank + bank, node.depth + 1, True, multiplier)
            score, _ = alphabeta(new_node, depth-1, alpha, beta, True)
            if score < best_score:
                best_score = score
                best_move = multiplier
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score, best_move


    
#game field
def game_loop(start_number,algorithm):
    current_number = start_number
    player_points = 0
    ai_points = 0
    game_bank = 0
    is_player_turn = True
    algorithm_name = "Minimax" if algorithm == "minimax" else "Alpha-Beta" if algorithm == "alphabeta" else "Random"
    
    log_messages = []

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Tekst
        info_text = font.render(f'Pionts: {current_number} || Player: {player_points} | AI: {ai_points} ({algorithm_name}) || Bank {game_bank}', True, TEXT_COLOR)
        screen.blit(info_text, (50, 50))

        # log
        log_y_start = 450
        for message in log_messages[-5:]:
            log_text = font.render(message, True, TEXT_COLOR)
            screen.blit(log_text, (50, log_y_start))
            log_y_start += 30
        # player turn
        if is_player_turn and current_number < 5000:  
            
            choice_made = False
            while not choice_made:
                screen.fill(BACKGROUND_COLOR)  
                
                
                screen.blit(info_text, (50, 50))
                log_y_start = 500
                for message in log_messages[-5:]:
                    log_text = font.render(message, True, TEXT_COLOR)
                    screen.blit(log_text, (50, log_y_start))
                    log_y_start += 30

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                
                button_y_offset = 0  
                button_spacing = 100  
                
                if draw_button('x2', (350, 150 + button_y_offset), BUTTON_COLOR, BUTTON_HOVER_COLOR, screen):
                    multiplier = 2
                    choice_made = True
                button_y_offset += button_spacing

                if draw_button('x3', (350, 150 + button_y_offset), BUTTON_COLOR, BUTTON_HOVER_COLOR, screen):
                    multiplier = 3
                    choice_made = True
                button_y_offset += button_spacing

                if draw_button('x4', (350, 150 + button_y_offset), BUTTON_COLOR, BUTTON_HOVER_COLOR, screen):
                    multiplier = 4
                    choice_made = True

                pygame.display.flip()

            pygame.time.wait(500)
            new_number = current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            log_messages.append(f"Player x{multiplier}, Result: {new_number} (P: {points}, Bank: {bank})")
            current_number = new_number
            player_points += points
            game_bank += bank
            

        # AI turn
        elif not is_player_turn and current_number < 5000:
            initial_node = Node(current_number, ai_points, player_points, game_bank, 0, True)

            if algorithm == "minimax":
                _, multiplier = minimax(initial_node, 2, True)
            elif algorithm == "alphabeta":
                _, multiplier = alphabeta(initial_node, 2, float('-inf'), float('inf'), True)
            elif algorithm == "random":
                multiplier = random.choice([2, 3, 4])

            new_number = current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            log_messages.append(f"AI  x{multiplier}, Result: {new_number} (P: {points}, Bank: {bank})")
            current_number = new_number
            ai_points += points
            game_bank += bank
            

        # check for end
        if current_number >= 5000:
            if not is_player_turn:
                ai_points += game_bank
                log_messages.append(f"Game over: AI reached {current_number}. Bank points ({game_bank}) added to AI.")
            else:
                player_points += game_bank
                log_messages.append(f"Game over: Player reached {current_number}. Bank points ({game_bank}) added to Player.")
            break

        # If the game continues, the turn changes
        is_player_turn = not is_player_turn

    display_end_game_screen(player_points, ai_points, game_bank, log_messages)  




def main():
    main_menu()

if __name__ == "__main__":
    main()
