import graph_based_functions as gf
import networkx as nx
import random
import config
import data_process as dp
import ranking_functions as rf
x = []
y = []

def init_neighbour_q_dict(graph):
    """initial state value for each node with each neighbour as a dictionary
    Example: the graph (1 --- 2 ---- 3) will be initialised as {1:{2:0}, 2:{1:0, 3:0}, 3:{2:0}}

    param: graph: a networkx graph
    """
    q_dict = {}
    nodes = graph.nodes()
    for node in nodes:
        neighbour_q_value_dict = {}
        neighbours = gf.get_neighbors_list(graph, node)
        if len(neighbours) == 0:
            neighbours = [node]
        for n in neighbours:
            neighbour_q_value_dict[n] = float(0)
        q_dict[node] = neighbour_q_value_dict
    return q_dict


def update_q_value(graph, q_dict, node, neighbour):
    """update state value according to formula: 
    v = current_value + learning_rate(reward + discounter_factor * old_max - current_value)

    param: graph: a networkx graph
    param: node: a node that we want to update its value
    param: neighbour: select neighbour
    """
    node_list = graph.nodes()
    cur_qvalue = q_dict[node][neighbour] # current q value for the neighbour
    max_q = q_dict[node][get_greatest_qvalue_nei(q_dict[node])]
    new_val = float(cur_qvalue) + config.alpha * (float(node_list[node]["Payoff"]) + config.gamma * max_q - cur_qvalue)
    q_dict[node][neighbour] = new_val
    # print("%.4f"% new_val)

def get_greatest_qvalue_nei(q_dict):
    """return a neighbour of node that gives the highest expected payoff
    
    # param: q_dict: a dictionary that key is neighbour id and the value is expected payoff
    """
    res = []
    try:
        max_val = max(q_dict, key=q_dict.get)
        res = [key for key in q_dict.keys() if q_dict[key]==q_dict[max_val]]
    except ValueError:
        pass
    return random.choice(res)


def update_newStr(graph, strategy_dict):
    # all node have to update there strategy at same time. Therefore, when they
    # have learned new strategy, the strategy will be stored in an intermediate
    # dictionary. This function is to update the strategy base on intermediate dictionary.
    # Meanwhile, the number of nodes whose strategy is cooperation is updated.
    # param: strategy_dict: it refers to intermediate dictionary
    
    nodes = graph.nodes()
    for n in nodes:
        cur_node = nodes[n]
        if not cur_node["IsSeed"]: 
            if strategy_dict[n] != cur_node['Strategy']:
                if strategy_dict[n] == "C":
                    config.num_of_c += 1
                else:
                    config.num_of_c -= 1

            cur_node['Strategy'] = strategy_dict[n]


def learning_nei_approach(graph, q_dict):
    # A reinforcement learning approach is implemented. 
    # In each iteration, node will behave either exploration or exploitation based on 
    # given rondom number. 
    #
    # If doing the exploration, node/agent randomly selects a neighbour and will copy its
    # strategy.
    # If doing the exploitation, node/agent select the neighbour that retruns the greatest
    # expected value. 
    # 
    # After getting intermediate dictionary, then update it and play pdg.
    temp_strategy_dict = {} # record the intermediate strategies
    selected_nei_dict = {} # record the neighbour that has been selected in current round
    nodes = graph.nodes()
    for i in nodes:
        if not nodes[i]["IsSeed"]:
            random_number = random.uniform(0, 1)
            if random_number < config.eps:  # exploration
                
                # print('exploration')
                neighbour_list = gf.get_neighbors_list(graph, i)
                if len(neighbour_list) == 0:
                    neighbour_list = [i]
                secure_random = random.SystemRandom()
                random_nei = secure_random.choice(neighbour_list)
                temp_strategy_dict[i] = nodes[random_nei]["Strategy"]
                selected_nei_dict[i] = random_nei
                
            else: # exploitation
                # print('exploitation') 
                random_nei = get_greatest_qvalue_nei(q_dict[i])
                temp_strategy_dict[i] = nodes[random_nei]["Strategy"]
                selected_nei_dict[i] = random_nei
            
    update_newStr(graph, temp_strategy_dict) # change the strategy
    gf.play_game(graph)
    nodes = graph.nodes()
    for i in nodes:
        if not nodes[i]["IsSeed"]:
            update_q_value(graph, q_dict, i, selected_nei_dict[i])
          


def run_learning(graph, round, num_seed,game_type="PDG"):
    # Experiment entry
    # :param round: number of runs
    # :param num_seed: number of nodes that are needed to be cooperative
    # :param game_type: game type

    gf.init_nodes_with_attributes(graph) # initail graph
    # seed_set = rf.get_n_top_degree_node(graph, 50)
    # seed_set = rf.getRandomNodes(graph, 50)
    seed_set = [1,2]
    gf.set_seeds(seed_set, graph)
    gf.print_nodes_information(graph)
    q_dict = init_neighbour_q_dict(graph) # initial q table for every node with its neighbours
    i = 0
    # test starts here
    while(i < round):
        x.append(i)
        learning_nei_approach(graph, q_dict) # learning approach based on neighbours' choices
        gf.play_game(graph, game_type) # update payoff for each nodes
        y.append(config.num_of_c / config.num_of_nodes)
        i += 1

    
    


def main():
    data_path = '.\\res\\'
    config.is_seed_on = True
    # path = 'dolphins.txt'
    # graph = gf.import_graph_from_txt(path)
    # graph = nx.erdos_renyi_graph(1000,0.01) 
    graph = nx.barabasi_albert_graph(1000,6) 
    graph = gf.import_graph_from_txt('simpleGraph.txt')
    run_learning(graph, 3, 1)
    #dp.vis_rate_vs_round(x,y)  
    #dp.export_to_excel(y, data_path, "nei_learning", "scale_free_random", "PDG")
    
    
    #########################Test############################
    # print(init_neighbour_q_dict(graph))
    # print(rf.get_n_top_degree_node(graph,10))
# main()