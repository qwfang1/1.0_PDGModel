# payoff table for prisoner's delimma game
payoff_table_PDG = {('D', 'D'): 0, ('D', 'C'): 1.2, ('C', 'D'): 0, ('C', 'C'): 1}
# agent may defect out of greedy
payoff_table_Chicken = {('D', 'D'): 0, ('D', 'C'): 1.2, ('C', 'D'): 0.2, ('C', 'C'): 0.7}
# agent may defect out of fear of no-cooperative partner
payoff_table_stag_hunt = {('D', 'D'): 0.2, ('D', 'C'): 1.0, ('C', 'D'): 0, ('C', 'C'): 1.2}


def get_payoff(my_strategy, the_other_strategy, game_type="PDG"):
    if game_type == "chicken":
        return payoff_table_Chicken[(my_strategy, the_other_strategy)]
    elif game_type == "stag_hunt":
        return payoff_table_stag_hunt[(my_strategy, the_other_strategy)]
    return payoff_table_PDG[(my_strategy, the_other_strategy)]
