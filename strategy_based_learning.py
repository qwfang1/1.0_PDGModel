import config
import random
import graph_based_functions as gf
import networkx as nx
import matplotlib.pyplot as plt
import data_process as dp
import ranking_functions as rf

def q_function_init(graph):
    nodes = graph.nodes()
    config.q_function = [{"C": float(0.0000), "D": float(0.0000)} for i in range(0, len(nodes) + 1)]

def arg_max(q_list):
    """
    return the max strategy
    :param q_list: q value for a node
    :return: the strategy either cooperation or cooperation
    """
    expected_value_c = q_list["C"]
    expected_value_d = q_list["D"]
    if expected_value_c > expected_value_d:
        return "C"
    elif expected_value_c < expected_value_d:
        return "D"
    else:
        return config.strategy[random.randint(0, 1)]


def max_q_value(q_list):
    """
    return the largest expected value
    :param q_list: a dictionary for strategy - value items
    :return: the largest expected value
    """
    expected_value_c = q_list["C"]
    expected_value_d = q_list["D"]
    if expected_value_c >= expected_value_d:
        return expected_value_c
    elif expected_value_c < expected_value_d:
        return expected_value_d


def update_q_value(i, nodes):
    """
    update expected value(Q value) for given node
    :param i: the id of given node
    :param nodes: nodes list for given graph
    :return: none
    """
    current_node = nodes[i]
    config.q_function[i][current_node["Strategy"]] += config.alpha * (float(current_node["Payoff"]) +
                config.gamma * max_q_value(config.q_function[i]) - config.q_function[i][current_node["Strategy"]])


def learning(graph):
    nodes = graph.nodes()
    for i in nodes:
        if not nodes[i]["IsSeed"]:
            random_number = random.uniform(0, 1)
            if random_number < config.eps:  # exploration
                selected_strategy = config.strategy[random.randint(0, 1)]
                nodes[i]["Strategy"] = selected_strategy
            else:  # exploitation
                selected_strategy = arg_max(config.q_function[i])
                nodes[i]["Strategy"] = selected_strategy      
    gf.play_game(graph)
    nodes = graph.nodes()
    for i in nodes:
        if not nodes[i]["IsSeed"]:
            update_q_value(i, nodes)


def color_and_show_graph(graph):
    color_map = gf.set_colors_to_nodes(graph)
    nx.draw(graph, node_color=color_map, with_labels=True)
    plt.show()

def main():
    # config.is_seed_on = False
    # new_graph = gf.import_graph_from_txt('dolphins.txt')
    # new_graph = gbf.import_graph_from_txt('simple_graph.txt')
    # new_graph = nx.watts_strogatz_graph(100, 7, 0.3, seed=5)
    # new_graph = nx.erdos_renyi_graph(1000, 0.01)
    # new_graph = graph_models.get_star_graph(6)
    new_graph = nx.barabasi_albert_graph(1000,6) 
    y = []
    x = []
    gf.init_nodes_with_attributes(new_graph)
    q_function_init(new_graph)
    most_top_node = rf.get_n_top_degree_node(new_graph, 50)
    gf.set_seeds(most_top_node, new_graph)
    gf.print_nodes_information(new_graph)
    for i in range(1000):
        learning(new_graph)
        y.append(gf.get_number_of_c(new_graph) / config.num_of_nodes)
        x.append(i)
    # gf.print_nodes_information(new_graph)
    # print(config.q_function)
  
    # log_info_import()
    # color_and_show_graph(new_graph)
    dp.vis_rate_vs_round(y)
   

# main()

