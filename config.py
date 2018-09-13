num_of_c = float(0)  # number of nodes that are cooperation
num_of_nodes = float(0)  # number of nodes that are in given graph
alpha = float(0.1)  # learning rate
eps = 0.1  # greedy - exploration or exploitation
gamma = 0.9  # discount factor, determines the importance of future rewards. Close to 1, it may diverge

###################### strategy based learning related #######################################
q_function = []  # the first index refers to cooperation, the second refers to defection.
strategy = ["C", "D"]  # strategy set

is_seed_on = True # If turn it to false, the seed node will not be turned "IsSeed" attribut
# to true.
