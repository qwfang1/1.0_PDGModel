import config 
import networkx as nx
import matplotlib.pyplot as plt
import random

def get_n_top_centrality_node(graph, centrality_type, num_seed):
    # rank node by centrality and return n-top nodes
    # param graph: a networkx graph
    # param centrality_type: centrality type
    # param num_seed: num of seed
    centrality = {}
    if centrality_type == 'eigenvector':
        eigen_centrality = nx.eigenvector_centrality(graph)
        centrality = sorted(eigen_centrality.items(), key=lambda x: x[1], reverse=True)
    elif centrality_type == 'closeness':
        closeness_centrality = nx.closeness_centrality(graph)
        centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
    elif centrality_type == 'betweenness':
        betweenness_centrality = nx.betweenness_centrality(graph)
        centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)
    return [value[0] for value in centrality[0:num_seed]]


def get_n_top_degree_node(graph, n=1):
    # Get the list of n node ID with the highest degree
    # :param graph: A networkx graph
    # :param n: The number of most top node that goes to return
    # :return: ID list of the node

    degree_dic = sorted(graph.degree, key=lambda x: x[1], reverse=True)

    return [value[0] for value in degree_dic[0:n]]


def get_n_top_core_node(graph, seed_num):
    core_dic = nx.core_number(graph)
    sorted_list = sorted(core_dic.items(), key=lambda x: x[1], reverse=True)
    
    return [value[0] for value in sorted_list[0:seed_num]]


def get_n_core_degree(graph, num_seed):
    core_dic = nx.core_number(graph)
    sorted_core = sorted(core_dic.items(), key=lambda x: x[1], reverse=True)    
    sorted_degree = sorted(nx.closeness_centrality(graph).items(), key=lambda x: x[1], reverse=True)
    new_list = []
    for c in sorted_core:
        for d in sorted_degree:
            if d[0] == c[0]:
                new_list.append([c[0], c[1], d[1]])
    new_list = sorted(new_list, key=lambda x: (x[1], x[2]), reverse=True)
    
    return [value[0] for value in new_list[0:num_seed]]


def getRandomNodes(graph, num_seed):
    nodes = graph.nodes()
    list_nodes = []
    for n in nodes:
        list_nodes.append(n)
    return random.sample(list_nodes, num_seed)

    