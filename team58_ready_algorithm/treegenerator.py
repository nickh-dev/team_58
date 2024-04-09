from graphviz import Digraph

def minimax_visualize(current_number, depth, graph, parent_name="Root", action=None):
    node_name = f"{parent_name}_{action}_{current_number}" if action else f"Start_{current_number}"
    node_label = f"{action}*{current_number}" if action else f"Start: {current_number}"
    
    graph.node(node_name, label=node_label)

    if action:
        graph.edge(parent_name, node_name)
        
    if depth == 0 or current_number >= 5000:
        return

    for next_multiplier in [2, 3, 4]:
        next_number = current_number * next_multiplier
        minimax_visualize(next_number, depth-1, graph, node_name, f"*{next_multiplier}")

def create_decision_tree(start_number=25, depth=3):
    graph = Digraph(comment='Decision Tree for Game')
    minimax_visualize(start_number, depth, graph)
    graph.render('decision_tree', view=True, format='pdf')

create_decision_tree(25, 10)
