import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from datetime import datetime
import openpyxl
import pandas as pd
import os
from matplotlib import style
def vis_rate_for_nodes(dict):
    keys = []
    values = []
    for key, value in dict.items():
        keys.append(key)
        values.append(value)
    objects = keys
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Rate')
    plt.title('Node')
    plt.show()


def vis_rate_vs_round(y):
    style.use('seaborn-bright')
    x = [i for i in range(len(y))]
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1),(0,0))
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.xlabel("Round")
    plt.ylabel("Frequence of Cooperation")
    ax1.plot(x, y)
    plt.legend()
    plt.subplots_adjust(bottom=0.2)
    plt.show()


def export_to_excel(y , target_path, alg_name, graph_name, extra_info):
    file_name = target_path + alg_name + '_' + graph_name + '_' + extra_info + '_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.xlsx'
    df = DataFrame({'Rate': y})
    df.to_excel(file_name, sheet_name='sheet1')

def combine_files(path):
    file_names = os.listdir(path) # "./dataset/random_1000-SF_SR_seed_on/"
    excels = [pd.ExcelFile(path + name) for name in file_names]
    frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]
    for frame in frames:
        frame.drop(frame.columns[[0]], axis=1, inplace=True)
    combined = pd.concat(frames,axis=1)
    cols = combined.iloc[0, 0:]
    combined.drop(0, inplace=True)
    combined.columns = cols
    combined['mean'] = combined.mean(axis=1)
    vis_rate_vs_round(combined['mean'])
    # print(combined)
    combined.to_excel(path + 'combined.xlsx', header=True, index=False)

combine_files("C:/Users/Tommy/Desktop/1.0_PDGModel/dataset/Experiment1-models/random_1000-SF_SR_seed_off/")
