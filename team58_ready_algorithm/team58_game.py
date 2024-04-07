import pygame
import sys
import random

pygame.init()

screen_width, screen_height = 850, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game with Alpha-Beta Pruning')

BACKGROUND_COLOR = (41, 47, 54)
BUTTON_COLOR = (255, 87, 34)
BUTTON_HOVER_COLOR = (255, 138, 101)
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0, 100)

font = pygame.font.Font(None, 36)

def draw_button(text, position, active_color, inactive_color, screen):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_rect = pygame.Rect(position[0], position[1], 200, 80)
    shadow_rect = button_rect.move(6, 6)
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect)
    pygame.draw.rect(screen, inactive_color if button_rect.collidepoint(mouse) else active_color, button_rect, border_radius=10)  # Main body of button with rounded corners

    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=button_rect.center)  # Center text
    screen.blit(text_surf, text_rect)

    return button_rect.collidepoint(mouse) and click[0] == 1


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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False






#Evaluates the current state of the game for AI.
def evaluate(number):
    if number >= 5000:
        return float('inf')
    else:
        return -abs(5000 - number)


# minimax algorithm
def minimax(number, depth, is_maximizing):
    if number >= 5000 or depth == 0:
        return evaluate(number), None

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            score, _ = minimax(new_number, depth-1, False)
            if score > best_score:
                best_score = score
                best_move = multiplier
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            score, _ = minimax(new_number, depth-1, True)
            if score < best_score:
                best_score = score
                best_move = multiplier
        return best_score, best_move


# alphabeta algorithm
def alphabeta(number, depth, alpha, beta, is_maximizing):
    if number >= 5000 or depth == 0:
        return evaluate(number), None

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            score, _ = alphabeta(new_number, depth-1, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = multiplier
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Alpha pruning
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            score, _ = alphabeta(new_number, depth-1, alpha, beta, True)
            if score < best_score:
                best_score = score
                best_move = multiplier
            beta = min(beta, score)
            if beta <= alpha:
                break  # Beta pruning
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
        screen.fill(BACKGROUND_COLOR)

        # Text
        info_text = font.render(f'Points: {current_number} || Player: {player_points} | AI: {ai_points} ({algorithm_name}) || Bank {game_bank}', True, TEXT_COLOR)
        screen.blit(info_text, (50, 50))

        # Log
        log_y_start = 450
        for message in log_messages[-5:]:
            log_text = font.render(message, True, TEXT_COLOR)
            screen.blit(log_text, (50, log_y_start))
            log_y_start += 30
        # Player turn
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

            new_number = current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            log_messages.append(f"Player x{multiplier}, Result: {new_number} (P: {points}, Bank: {bank})")
            current_number = new_number
            player_points += points
            game_bank += bank


        # AI turn
        elif not is_player_turn and current_number < 5000:
            pygame.time.wait(500)  # Pause to avoid errors and misclicks
            if algorithm == "minimax":
                _, multiplier = minimax(current_number, 3, True)
            elif algorithm == "alphabeta":
                _, multiplier = alphabeta(current_number, 3, float('-inf'), float('inf'), True)
            elif algorithm == "random":
                multiplier = random.choice([2, 3, 4])
            new_number = current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            log_messages.append(f"AI x{multiplier}, Result: {new_number} (P: {points}, Bank: {bank})")
            current_number = new_number
            ai_points += points
            game_bank += bank


        # Check for end
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
