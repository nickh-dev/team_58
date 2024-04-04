from graphviz import Digraph

def minimax_visualize(current_number, depth, graph, parent_name="Root", action=None):
    # Генерируем имя узла без использования символа "-"
    node_name = f"{parent_name}_{action}_{current_number}" if action else f"Start_{current_number}"
    node_label = f"{action}*{current_number}" if action else f"Start: {current_number}"
    
    graph.node(node_name, label=node_label)  # Указываем имя и метку для узла

    if action:  # Если действие задано, добавляем ребро к графу
        graph.edge(parent_name, node_name)

    # Условие остановки: достигли максимальной глубины или число превысило 5000
    if depth == 0 or current_number >= 5000:
        return

    for next_multiplier in [2, 3, 4]:
        next_number = current_number * next_multiplier
        # Делаем последний шаг, даже если число превысит 5000
        minimax_visualize(next_number, depth-1, graph, node_name, f"*{next_multiplier}")

def create_decision_tree(start_number=25, depth=3):
    graph = Digraph(comment='Decision Tree for Game')
    minimax_visualize(start_number, depth, graph)
    # Указываем формат вывода 'pdf' и включаем просмотр после генерации
    graph.render('decision_tree', view=True, format='pdf')

create_decision_tree(25, 10)  # Указываете начальное число и глубину поиска
