import ranking_functions as rf
import graph_based_functions as gf
import networkx as nx
import config
import strategy_based_learning as il
config.is_seed_on = False
def experiment():
    new_graph = nx.barabasi_albert_graph(1000,6) 
    y = []
    gf.init_nodes_with_attributes(new_graph)
    il.q_function_init(new_graph)
    most_top_node = rf.get_n_top_degree_node(new_graph, 50)
    gf.set_seeds(most_top_node, new_graph)
    gf.print_nodes_information(new_graph)
    for _ in range(1000):
        il.learning(new_graph)
        y.append(gf.get_number_of_c(new_graph) / config.num_of_nodes)
        
    print(gf.get_number_of_c(new_graph) / config.num_of_nodes)

experiment()
# with seed 0.282 | 0.272 | 0.279 | 0.3 | 0.3 |
# no seed: 0.285 | 0.32 | 0.303 | 0.288 | 0.289