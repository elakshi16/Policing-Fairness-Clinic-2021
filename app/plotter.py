import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

def basic_plot(node_dict, save_file=False):
    ## Plot and save both outputs
    x = []
    y = []
    scalval = []
    for key, value in node_dict.items():
        x.append(key[0])
        y.append(key[1])
        scalval.append(value)
    # size and color:
    # plot
    fig, ax = plt.subplots()
    fig.set_size_inches(20,20)
    # ax.scatter(x, y, s=arrCnt, alpha=0.2)
    ax.scatter(x, y, s=1, c=scalval, cmap=cm.get_cmap('plasma')) # color instead of size 
    ax.set(xlim=(0, 350), xticks=np.arange(1, 8),
        ylim=(0, 475), yticks=np.arange(1, 8))

    if save_file:
        plt.savefig(save_file)
        plt.close()
    