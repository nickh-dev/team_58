import pygame 
import sys
import random

pygame.init()

screen_width, screen_height = 800, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Spēle ar Alfa-Beta Apgriešanu')


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

LIGHT_GREY = (200, 70, 200)
DARK_GREY = (30, 30, 30)
BUTTON_COLOR = (160, 160, 160)
BUTTON_HOVER_COLOR = (230, 230, 230)

font = pygame.font.Font(None, 36)

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


def main_menu():
    screen.fill(DARK_GREY)  
    running = True
    while running:
        start_button_clicked = draw_button('START', (325, 250), BUTTON_COLOR, BUTTON_HOVER_COLOR)
        quit_button_clicked = draw_button('EXIT', (325, 350), BUTTON_COLOR, BUTTON_HOVER_COLOR)

        if start_button_clicked:
            start_number = start_menu()
            game_loop(start_number)
            running = False
        if quit_button_clicked:
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()


def start_menu():
    input_number = ''  
    running = True
    while running:
        screen.fill(BLACK)
        title_text = font.render('Izvēlies sākuma skaitli (25 līdz 40): ' + input_number, True, WHITE)
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

def display_end_game_screen(player_points, ai_points, game_bank, log_messages):
    screen.fill(BLACK)
    result_text = f"Player points: {player_points}, AI points: {ai_points}, Bank: {game_bank}"
    result_msg = font.render(result_text, True, WHITE)
    screen.blit(result_msg, (screen_width // 2 - result_msg.get_width() // 2, 20))

    # Вывод лога ниже результатов
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

                    
def evaluate(number):
    # Примерная оценочная функция
    if number >= 5000:
        return float('inf')  # Максимально положительное значение для победы
    else:
        return -abs(5000 - number)  # Приближение к 5000 считается положительным

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
    

def game_loop(start_number):
    current_number = start_number
    player_points = 0
    ai_points = 0
    game_bank = 0
    is_player_turn = True

    
    log_messages = []

    running = True
    while running:
        screen.fill(BLACK)

        # Tekst
        info_text = font.render(f'Pionts: {current_number} || Player: {player_points} | AI:{ai_points} || Bank {game_bank}', True, WHITE)
        screen.blit(info_text, (50, 50))

        # log
        log_y_start = 450
        for message in log_messages[-5:]:
            log_text = font.render(message, True, WHITE)
            screen.blit(log_text, (50, log_y_start))
            log_y_start += 30

        if is_player_turn and current_number < 5000:  
            
            choice_made = False
            while not choice_made:
                screen.fill(BLACK)  
                
                # Повторно отрисовываем информацию о текущем состоянии игры
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

                # Вертикальное расположение кнопок
                button_y_offset = 0  # Начальное смещение для первой кнопки
                button_spacing = 55  # Расстояние между кнопками
                
                if draw_button('2', (screen_width // 2 - 75, 300 + button_y_offset), BUTTON_COLOR, BUTTON_HOVER_COLOR):
                    multiplier = 2
                    choice_made = True
                button_y_offset += button_spacing  # Смещаем позицию следующей кнопки
                
                if draw_button('3', (screen_width // 2 - 75, 300 + button_y_offset), BUTTON_COLOR, BUTTON_HOVER_COLOR):
                    multiplier = 3
                    choice_made = True
                button_y_offset += button_spacing  # Смещаем позицию следующей кнопки
                
                if draw_button('4', (screen_width // 2 - 75, 300 + button_y_offset), BUTTON_COLOR, BUTTON_HOVER_COLOR):
                    multiplier = 4
                    choice_made = True

                pygame.display.flip()

            # Применение выбора игрока
            new_number = current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            log_messages.append(f"Player {multiplier}, Rezult: {new_number} (P: {points}, Bank: {bank})")
            current_number = new_number
            player_points += points
            game_bank += bank
            

        # Логика хода ИИ
        elif not is_player_turn and current_number < 5000:  # Проверяем, что игра не окончена
            pygame.time.wait(500)  # Пауза для ИИ
            _, multiplier = minimax(current_number, 100, True)  # Использование минимакса для выбора множителя
            if multiplier is None:  # Если минимакс не возвращает множитель, используем резервный
                multiplier = random.choice([2, 3, 4])
            new_number = current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            log_messages.append(f"AI  {multiplier}, Result: {new_number} (P: {points}, Bank: {bank})")
            current_number = new_number
            ai_points += points
            game_bank += bank
            

        # Проверка на окончание игры
        if current_number >= 5000:
            if not is_player_turn:
                ai_points += game_bank
                log_messages.append(f"Game over: AI reached {current_number}. Bank points ({game_bank}) added to AI.")
            else:
                player_points += game_bank
                log_messages.append(f"Game over: Player reached {current_number}. Bank points ({game_bank}) added to Player.")
            break

        # Смена очереди хода только если игра не закончилась
        is_player_turn = not is_player_turn

    display_end_game_screen(player_points, ai_points, game_bank, log_messages)  




def main():
    main_menu()

if __name__ == "__main__":
    main()