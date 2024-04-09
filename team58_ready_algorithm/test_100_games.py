import random
import time

def update_points_and_bank(number):
    points, bank = 0, 0
    if number % 2 == 0:
        points -= 1
    else:
        points += 1
    if number % 10 == 0 or number % 10 == 5:
        bank += 1
    return points, bank

class Node:
    def __init__(self, current_number, ai_points, player_points, game_bank, depth, is_maximizing, multiplier=None,is_ai_turn=True):
        self.current_number = current_number
        self.ai_points = ai_points
        self.player_points = player_points
        self.game_bank = game_bank
        self.depth = depth
        self.is_maximizing = is_maximizing
        self.multiplier = multiplier
        self.children = []
        self.is_ai_turn = is_ai_turn
    def add_child(self, child):
        self.children.append(child)

def evaluate(current_number, ai_points, player_points, game_bank,  is_ai_turn):
    A = 1
    B = 1
    C = 0.0001
    base_score = A * (ai_points - player_points) + B * game_bank - C * abs(5000 - current_number)

    if current_number >= 5000:
        return float('inf') if is_ai_turn else float('-inf')
    else:
        return base_score

# minimax algorithm    
def minimax(node, depth, is_maximizing, visited_nodes=0):
    visited_nodes += 1
    if node.current_number >= 5000 or depth == 0:
        score = evaluate(node.current_number, node.ai_points, node.player_points, node.game_bank,  node.is_ai_turn)

        #print(f"Minimax: Depth {depth}, Score: {score}, Maximizing: {is_maximizing}")
        return score, None, visited_nodes
    
    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = node.current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_node = Node(new_number, node.ai_points + points, node.player_points, node.game_bank + bank, node.depth + 1, False, multiplier)
            #print(f"Minimax: Creating node at depth {new_node.depth} with current_number {new_node.current_number}, ai_points {new_node.ai_points}, player_points {new_node.player_points}, game_bank {new_node.game_bank}, is_maximizing {new_node.is_maximizing}, multiplier {new_node.multiplier}")
            score, _, visited_nodes = minimax(new_node, depth-1, False, visited_nodes)
            if score > best_score:
                best_score = score
                best_move = multiplier
        #print(f"Minimax: Depth {depth}, Best Score: {best_score}, Best Move: {best_move}, Maximizing: {is_maximizing}")
        return best_score, best_move, visited_nodes
    else:
        best_score = float('inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = node.current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_node = Node(new_number, node.ai_points, node.player_points + points, node.game_bank + bank, node.depth + 1, True, multiplier)
            score, _, visited_nodes = minimax(new_node, depth-1, True, visited_nodes) 
            if score < best_score:
                best_score = score
                best_move = multiplier
        #print(f"Minimax: Depth {depth}, Best Score: {best_score}, Best Move: {best_move}, Maximizing: {is_maximizing}")
        return best_score, best_move, visited_nodes
    



# alphabeta algorithm 
def alphabeta(node, depth, alpha, beta, is_maximizing,visited_nodes=0):
    visited_nodes += 1
    if node.current_number >= 5000 or depth == 0:
        score = evaluate(node.current_number, node.ai_points, node.player_points, node.game_bank, node.is_ai_turn)
        return score, None, visited_nodes
    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = node.current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_node = Node(new_number, node.ai_points + points, node.player_points, node.game_bank + bank, node.depth + 1, False, multiplier)
            #print(f"AlphaBeta: Creating node at depth {new_node.depth} with current_number {new_node.current_number}, ai_points {new_node.ai_points}, player_points {new_node.player_points}, game_bank {new_node.game_bank}, is_maximizing {new_node.is_maximizing}, multiplier {new_node.multiplier}")
            score, _, visited_nodes = alphabeta(new_node, depth-1, alpha, beta, False, visited_nodes)
            if score > best_score:
                best_score = score
                best_move = multiplier
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score, best_move, visited_nodes
    else:
        best_score = float('inf')
        best_move = None
        for multiplier in [2, 3, 4]:
            new_number = node.current_number * multiplier
            points, bank = update_points_and_bank(new_number)
            new_node = Node(new_number, node.ai_points, node.player_points + points, node.game_bank + bank, node.depth + 1, True, multiplier)
            score, _, visited_nodes = alphabeta(new_node, depth-1, alpha, beta, True, visited_nodes)
            if score < best_score:
                best_score = score
                best_move = multiplier
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score, best_move, visited_nodes



def play_game(algorithm):
    current_number = random.randint(25, 40)
    ai_points = player_points = game_bank = 0
    is_player_turn = True
    ai_turn_times = [] 
    visited_nodes = 0

    while current_number < 5000:
        if is_player_turn: 
            multiplier = random.choice([2, 3, 4])
        else:  
            start_time = time.perf_counter() 
            initial_node = Node(current_number, ai_points, player_points, game_bank, 0, True)
            if algorithm == "minimax":
                _, multiplier, visited_nodes = minimax(initial_node, 5, True)
            elif algorithm == "alphabeta":
                _, multiplier, visited_nodes = alphabeta(initial_node, 5, float('-inf'), float('inf'), True)
            
            end_time = time.perf_counter() 
            ai_turn_time_ms = (end_time - start_time) * 1000  
            ai_turn_times.append(ai_turn_time_ms)  
            #print(f"Visited nodes: {visited_nodes}")
        new_number = current_number * multiplier
        points, bank = update_points_and_bank(new_number)
        if is_player_turn:
            player_points += points
        else:
            ai_points += points
        game_bank += bank

        current_number = new_number
        is_player_turn = not is_player_turn

    avg_turn_time_ms = sum(ai_turn_times) / len(ai_turn_times) if ai_turn_times else 0
    #print(f"Average AI turn time: {avg_turn_time_ms:.5f} milliseconds") 
    total_ai_turn_time_ms = sum(ai_turn_times)
    if ai_points > player_points:
        return "AI", visited_nodes, total_ai_turn_time_ms
    else:
        return "Player", visited_nodes, total_ai_turn_time_ms
def test_algorithm(algorithm, games=100):
    total_visited_nodes = 0
    total_time_ms = 0
    ai_wins = 0
    for _ in range(games):
        result, visited_nodes, ai_turn_time_ms = play_game(algorithm)
        if result == "AI":
            ai_wins += 1
        total_visited_nodes += visited_nodes
        total_time_ms += ai_turn_time_ms

    average_visited_nodes = total_visited_nodes / games
    average_turn_time_ms = total_time_ms / games
    print(f"{algorithm}: AI wins {ai_wins}/{games} games.")
    print(f"Average visited nodes per game: {average_visited_nodes}")
    print(f"Average AI turn time: {average_turn_time_ms:.4f} ms")

test_algorithm("minimax")
test_algorithm("alphabeta")
