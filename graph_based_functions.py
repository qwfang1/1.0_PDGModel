import xlrd
import matplotlib.pyplot as plt
import networkx as nx
import matrix_payoff
import random
import config


def import_graph_from_txt(path):
    # Get a networkxx graph from a .txt file. Text file have to follow in a fixed order
    # :param path: the path of the file
    # :return: a networkxx graph
    graph = nx.Graph()
    file = open(path, "r")
    for line in file:
        nodes = line.split()
        graph.add_edge(int(nodes[0]), int(nodes[1]))
    return graph


def init_nodes_with_attributes(graph):
    # Give nodes attributes and initialise constants in config.py 
    #:param graph: a networkx graph
    #:return: none
    nodes = graph.nodes()
    config.num_of_nodes = len(nodes)
    # config.q_function = [{"C": float(0), "D": float(0)} for i in range(0, len(nodes) + 1)]
    print(config.num_of_nodes)
    for n in nodes:
        nodes[n]["Strategy"] = "D"
        nodes[n]["Payoff"] = float(0)
        nodes[n]["IsSeed"] = bool(False)
    config.num_of_c = 0


def print_nodes_information(graph):
    # print node one by one with its attributes' value
    nodes = graph.nodes()
    number_of_nodes = len(nodes)
    for n in nodes:
        print('ID: ' + str(n) + " " * (len(str(number_of_nodes)) - len(str(n))), '| Strategy: ' + nodes[n]['Strategy'],
              '| Payoff: ' + str(nodes[n]['Payoff']), "| neighbours: ", get_neighbors_list(graph, n))
    print()


def get_neighbors_list(graph, node):
    # get node's neighbours as a list
    # :param graph: a given networkx graph
    # :param node: a specific node(ID)
    # :return: a node list
    
    neighbors = []
    for n in graph.neighbors(node):
        neighbors.append(n)
    return neighbors


def get_number_of_c(graph):
    # return the number of cooperative nodes
    count = 0
    nodes = graph.nodes()
    for i in nodes:
        current_node = nodes[i]
        if current_node["Strategy"] == "C":
            count += 1
    return count


def set_seeds(node_id_list, graph):
    node_list = graph.nodes()
    for i in node_id_list:
        node_list[i]['Strategy'] = 'C'
        if config.is_seed_on:
            node_list[i]['IsSeed'] = True
    config.num_of_c = len(node_id_list)



def set_colors_to_nodes(graph):
    color_map = []
    nodes = graph.nodes
    for i in nodes:
        if nodes[i]["Strategy"] == "C":
            color_map.append("yellow")
            config.num_of_c += 1
        else:
            color_map.append("blue")
    return color_map

########################################################################################################################
def play_game(graph, game_type="PDG"):
    """
    Each node plays PDG with its neighbours and update its payoff
    :param graph:
    :return:
    """
    nodes = graph.nodes()
    for n in nodes:
        current_node = nodes[n]
        neighbours_index = get_neighbors_list(graph, n)
        total_payoff = 0
        for n_1 in neighbours_index:
            current_neighbour = nodes[n_1]
            total_payoff += matrix_payoff.get_payoff(current_node['Strategy'], current_neighbour['Strategy'], game_type)
        current_node['Payoff'] = "{0:.1f}".format(total_payoff)


def judge_current_strategy(graph):
    """
    Each node play PDG with its adjacent nodes and update the potential new strategy
    :param graph: A networkx graph
    :return: A dictionary that contains new strategy for each node
    """
    nodes = graph.nodes()
    new_value_dictionary = {-1: "D"}
    for n in nodes:
        current_node = nodes[n]
        neighbours = get_neighbors_list(graph, n)
        my_nei_length = len(neighbours)
        if len(neighbours) == 0:
            neighbours.append(current_node)
        random_neighbour_index = neighbours[random.randint(0, len(neighbours) - 1)]
        random_neighbour = nodes[random_neighbour_index]
        payoff = float(current_node['Payoff'])
        new_payoff = float(random_neighbour['Payoff'])
        if new_payoff > payoff and (not current_node["IsSeed"]) and \
                current_node['Strategy'] != random_neighbour['Strategy']:
            new_length = len(get_neighbors_list(graph, random_neighbour_index))

            probability = (new_payoff - payoff)/(max(my_nei_length, new_length) * 1.2)
            random_number = random.uniform(0, 1)
            if random_number < probability:
                new_value_dictionary[n] = random_neighbour['Strategy']
                if random_neighbour['Strategy'] == 'C':
                    config.num_of_c += 1
                else:
                    config.num_of_c -= 1
            else:
                new_value_dictionary[n] = current_node['Strategy']
        else:
            new_value_dictionary[n] = current_node['Strategy']
    return new_value_dictionary


def update_strategy(strategy_dictionary, graph):
    nodes = graph.nodes()
    for n in nodes:
        current_node = nodes[n]
        current_node['Strategy'] = strategy_dictionary[n]

