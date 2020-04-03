# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from os import walk
import matplotlib
matplotlib.use('Agg')

fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=10
fig_size[1]=8
#plt.rcParams["figure.figsize"] = fig_size


for (dirpath, dirnames, filenames) in walk("./output"):
    for file in filenames:
        list_from = []
        list_to = []
        with open ('./output/'+file, 'r+') as f:
            lis = [line.split(",") for line in f]
            for l in lis:
                if len(l) > 1:
                    list_from.append(file.replace(".csv",""))
                    list_to.append(l[3].replace('\n', ''))


        # Build a dataframe with your connections
        df = pd.DataFrame({'from': list_from, 'to': list_to})


        # Build your graph
        G = nx.from_pandas_edgelist(df, 'from', 'to')
        # Graph with Custom nodes:
        nx.draw(G, with_labels=True, node_size=1000, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40, scale = 10)
        plt.show()
        plt.savefig("./layouts/"+file.replace("csv","png"))
        plt.close()

