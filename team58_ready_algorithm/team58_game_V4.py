import pygame 
import sys
import random

pygame.init()

screen_width, screen_height = 800, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game with Alpha-Beta Pruning')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREY = (200, 70, 200)
DARK_GREY = (30, 30, 30)
BUTTON_COLOR = (160, 160, 160)
BUTTON_HOVER_COLOR = (230, 230, 230)
font = pygame.font.Font(None, 36)



#Draws a button with text on the screen and detects clicks
def draw_button(text, position, active_color, inactive_color):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(position[0], position[1], 150, 50)  
    pygame.draw.ellipse(screen, inactive_color if button_rect.collidepoint(mouse) else active_color, button_rect)  
    pygame.draw.rect(screen, inactive_color if button_rect.collidepoint(mouse) else active_color, button_rect)  # Основное тело кнопки

    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(position[0] + 75, position[1] + 25))  
    screen.blit(text_surf, text_rect)

    return button_rect.collidepoint(mouse) and click[0] == 1



#Displays the main menu and handles the algorithm selection.
def main_menu():
    screen.fill(DARK_GREY)  
    chosen_algorithm = None  
    running = True
    while running:
        start_button_clicked = draw_button('START', (325, 100), BUTTON_COLOR, BUTTON_HOVER_COLOR)
        quit_button_clicked = draw_button('EXIT', (325, 550), BUTTON_COLOR, BUTTON_HOVER_COLOR)

        
        if draw_button('Minimax', (325, 250), BUTTON_COLOR, BUTTON_HOVER_COLOR):
            chosen_algorithm = "minimax"
        elif draw_button('Alpha-Beta', (325, 350), BUTTON_COLOR, BUTTON_HOVER_COLOR):
            chosen_algorithm = "alphabeta"
        elif draw_button('Random', (325, 450), BUTTON_COLOR, BUTTON_HOVER_COLOR):
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
        screen.fill(BLACK)
        title_text = font.render('Choose a starting number (25 to 40): ' + input_number, True, WHITE)
        screen.blit(title_text, (200, 250))
        
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
    screen.fill(BLACK)
    result_text = f"Player points: {player_points}, AI points: {ai_points}, Bank: {game_bank}"
    result_msg = font.render(result_text, True, WHITE)
    screen.blit(result_msg, (screen_width // 2 - result_msg.get_width() // 2, 20))

    
    log_start_y = 60
    for i, log_message in enumerate(log_messages[-15:], start=1):  
        log_text = font.render(log_message, True, WHITE)
        screen.blit(log_text, (50, log_start_y + i * 20))

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False






#Evaluates the current state of the game for AI.                    
def evaluate(current_number, ai_points, player_points, game_bank):
    if current_number >= 5000:
        return float('inf')
    else:
        A = 1
        B = 1
        C = 0.001
        return A * (ai_points - player_points) + B * game_bank - C * abs(5000 - current_number)



# minimax algorithm    
def minimax(number, depth, ai_points, player_points, game_bank, is_maximizing):
    if number >= 5000 or depth == 0:
        return evaluate(number, ai_points, player_points, game_bank), None

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            new_ai_points, new_game_bank = update_points_and_bank(new_number)
            score, _ = minimax(new_number, depth-1, ai_points + new_ai_points, player_points, game_bank + new_game_bank, False)
            if score > best_score:
                best_score = score
                best_move = multiplier
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            new_player_points, new_game_bank = update_points_and_bank(new_number)
            score, _ = minimax(new_number, depth-1, ai_points, player_points + new_player_points, game_bank + new_game_bank, True)
            if score < best_score:
                best_score = score
                best_move = multiplier
        return best_score, best_move


# alphabeta algorithm 
def alphabeta(number, depth, alpha, beta, ai_points, player_points, game_bank, is_maximizing):
    if number >= 5000 or depth == 0:
        return evaluate(number, ai_points, player_points, game_bank), None

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            new_ai_points, new_game_bank = update_points_and_bank(new_number)  
            score, _ = alphabeta(new_number, depth-1, alpha, beta, ai_points + new_ai_points, player_points, game_bank + new_game_bank, False)
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
            new_number = number * multiplier
            new_player_points, new_game_bank = update_points_and_bank(new_number)
            score, _ = alphabeta(new_number, depth-1, alpha, beta, ai_points, player_points + new_player_points, game_bank + new_game_bank, True)
            if score < best_score:
                best_score = score
                best_move = multiplier
            beta = min(beta, score)
            if beta <= alpha:
                break 
        return best_score, best_move


    

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
        screen.fill(BLACK)

        # Tekst
        info_text = font.render(f'Pionts: {current_number} || Player: {player_points} | AI: {ai_points} ({algorithm_name}) || Bank {game_bank}', True, WHITE)
        screen.blit(info_text, (50, 50))

        # log
        log_y_start = 450
        for message in log_messages[-5:]:
            log_text = font.render(message, True, WHITE)
            screen.blit(log_text, (50, log_y_start))
            log_y_start += 30
        # player turn
        if is_player_turn and current_number < 5000:  
            
            choice_made = False
            while not choice_made:
                screen.fill(BLACK)  
                
                
                screen.blit(info_text, (50, 50))
                log_y_start = 500
                for message in log_messages[-5:]:
                    log_text = font.render(message, True, WHITE)
                    screen.blit(log_text, (50, log_y_start))
                    log_y_start += 30

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                
                button_y_offset = 0  
                button_spacing = 55  
                
                if draw_button('2', (screen_width // 2 - 75, 300 + button_y_offset), BUTTON_COLOR, BUTTON_HOVER_COLOR):
                    multiplier = 2
                    choice_made = True
                button_y_offset += button_spacing  
                
                if draw_button('3', (screen_width // 2 - 75, 300 + button_y_offset), BUTTON_COLOR, BUTTON_HOVER_COLOR):
                    multiplier = 3
                    choice_made = True
                button_y_offset += button_spacing  
                
                if draw_button('4', (screen_width // 2 - 75, 300 + button_y_offset), BUTTON_COLOR, BUTTON_HOVER_COLOR):
                    multiplier = 4
                    choice_made = True

                pygame.display.flip()

            pygame.time.wait(500)
            new_number = current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            log_messages.append(f"Player {multiplier}, Rezult: {new_number} (P: {points}, Bank: {bank})")
            current_number = new_number
            player_points += points
            game_bank += bank
            

        # AI turn
        elif not is_player_turn and current_number < 5000: 
            if algorithm == "minimax":
                _, multiplier = minimax(current_number, 3, ai_points, player_points, game_bank, True)
            elif algorithm == "alphabeta":
                _, multiplier = alphabeta(current_number, 3, float('-inf'), float('inf'), ai_points, player_points, game_bank, True)
            elif algorithm == "random":
                multiplier = random.choice([2, 3, 4])
            new_number = current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            log_messages.append(f"AI  {multiplier}, Result: {new_number} (P: {points}, Bank: {bank})")
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
