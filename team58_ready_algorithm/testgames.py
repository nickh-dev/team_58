import random

def update_points_and_bank(number):
    points, bank = 0, 0
    if number % 2 == 0:
        points -= 1
    else:
        points += 1
    if number % 10 == 0 or number % 10 == 5:
        bank += 1
    return points, bank

def evaluate(current_number, ai_points, player_points, game_bank):
    if current_number >= 5000:
        return float('inf')
    else:
        A = 1
        B = 1
        C = 0.001
        return A * (ai_points - player_points) + B * game_bank - C * abs(5000 - current_number)

def minimax(number, depth, ai_points, player_points, game_bank, is_maximizing):
    if number >= 5000 or depth == 0:
        return evaluate(number, ai_points, player_points, game_bank), None
    
    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_ai_points = ai_points + points if points > 0 else ai_points
            new_game_bank = game_bank + bank
            score, _ = minimax(new_number, depth - 1, new_ai_points, player_points, new_game_bank, False)
            if score > best_score:
                best_score = score
                best_move = multiplier
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_player_points = player_points + points if points > 0 else player_points
            new_game_bank = game_bank + bank
            score, _ = minimax(new_number, depth - 1, ai_points, new_player_points, new_game_bank, True)
            if score < best_score:
                best_score = score
                best_move = multiplier
        return best_score, best_move

# Эту функцию нужно будет реализовать аналогично minimax, но с дополнительными проверками альфа и бета.
def alphabeta(number, depth, alpha, beta, ai_points, player_points, game_bank, is_maximizing):
    if number >= 5000 or depth == 0:
        return evaluate(number, ai_points, player_points, game_bank), None

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            # Предполагаем, что функция update_points_and_bank возвращает изменение очков ИИ и изменение банка
            new_ai_points, new_game_bank = update_points_and_bank(new_number)  
            # Обновляем очки ИИ и банка для следующего состояния
            score, _ = alphabeta(new_number, depth-1, alpha, beta, ai_points + new_ai_points, player_points, game_bank + new_game_bank, False)
            if score > best_score:
                best_score = score
                best_move = multiplier
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Применение альфа-обрезки
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = number * multiplier
            # Аналогично предполагаем изменение очков игрока и банка
            new_player_points, new_game_bank = update_points_and_bank(new_number)
            # Обновляем очки игрока и банка для следующего состояния
            score, _ = alphabeta(new_number, depth-1, alpha, beta, ai_points, player_points + new_player_points, game_bank + new_game_bank, True)
            if score < best_score:
                best_score = score
                best_move = multiplier
            beta = min(beta, score)
            if beta <= alpha:
                break  # Применение бета-обрезки
        return best_score, best_move

def play_game(algorithm):
    current_number = random.randint(25, 40)
    ai_points = player_points = game_bank = 0
    is_player_turn = True

    while current_number < 5000:
        if is_player_turn:  # Имитация хода игрока
            multiplier = random.choice([2, 3, 4])
        else:  # Ход ИИ
            if algorithm == "minimax":
                _, multiplier = minimax(current_number, 2, ai_points, player_points, game_bank, True)
            elif algorithm == "alphabeta":
                _, multiplier = alphabeta(current_number, 2, float('-inf'), float('inf'), ai_points, player_points, game_bank, True)
        
        new_number = current_number * multiplier
        points, bank = update_points_and_bank(new_number)
        if is_player_turn:
            player_points += points
        else:
            ai_points += points
        game_bank += bank

        current_number = new_number
        is_player_turn = not is_player_turn

    if ai_points > player_points:
        return "AI"
    else:
        return "Player"

def test_algorithm(algorithm, games=1000):
    ai_wins = sum(1 for _ in range(games) if play_game(algorithm) == "AI")
    print(f"{algorithm}: AI wins {ai_wins}/{games} games.")

test_algorithm("minimax")
test_algorithm("alphabeta")
