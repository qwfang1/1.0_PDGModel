import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame
from datetime import datetime
import openpyxl
import pandas as pd
import os
from matplotlib import style

path = "C:/Users/Tommy/Desktop/1.0_PDGModel/dataset/Experiment1-models/combine-seed-off-random/"
fileName = "combined_data.xlsx"
excel = pd.ExcelFile(path + fileName) 
frame = DataFrame(excel.parse(excel.sheet_names[0], header=None,index_col=None))
line1 = list(frame[0])[1:]
line2 = list(frame[1])[1:]
line3 = list(frame[2])[1:]

style.use('seaborn-bright')
x = [i for i in range(len(line1))]
ax1 = plt.subplot2grid((1,1),(0,0))
for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(45)
plt.xlabel("Round")
plt.ylabel("Frequency of Cooperation")
ax1.plot(x[0:2000], line1[0:2000], linestyle=':', marker='v', markevery=100, label='SR', color='black')
ax1.plot(x[0:2000], line2[0:2000], linestyle=':', marker='D', markevery=100, label='IL', color='blue')
ax1.plot(x[0:2000], line3[0:2000], linestyle=':', marker='o', markevery=100, label='NBL', color='red')
plt.title("Performance of different models under random-based selection and scale-free network without seed")
plt.subplots_adjust(bottom=0.2)
plt.legend(loc='lower right')
plt.show()