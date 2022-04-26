import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os

def basic_plot(node_dict, save_file=False):
    """
    Takes in dictionary of {(x,y): scalar_value}
    """
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

def final_plot(node_dict, prec=False, spath=False,fname=False, title=False, mean=False, stddev=False, similarity=False):
    x = []
    y = []
    scalval = []

    for key, value in node_dict.items():
        x.append(key[0])
        y.append(key[1])
        scalval.append(value)


    fig, ax = plt.subplots()
    
    if prec is True:
        pc = ax.scatter(x,y, c=scalval, cmap='viridis', marker='s',edgecolor='none')
    else:
        pc = ax.scatter(x,y,s=1.75, c=scalval, cmap='viridis', marker='s',edgecolor='none')
        
    fig.colorbar(pc, ax=ax)

    if title:
        ax.set_title(title)
    
    output_str = ''
    
    if mean:
        output_str += r'$\mu = $' + "{:.4f}".format(mean)
    if stddev:
        output_str += '\n' +  r'$\sigma=$' + "{:.4f}".format(stddev)
    if similarity:
        output_str += '\n similarity = ' + "{:.4f}".format(similarity)
    
    ax.text(min(x), min(y), output_str)


    fig.set_size_inches(10,10)

    if spath:
        if not os.path.exists(spath):
            os.makedirs(spath)
        
        plt.savefig(spath + fname, dpi=500)
        plt.close()


def imshow_plot(node_dict, spath=False,fname=False, title=False, mean=False, stddev=False, similarity=False):
    xi = []
    yi = []
    scalval = []
    for key, value in node_dict.items():
        xi.append(key[0])
        yi.append(key[1])
        scalval.append(value)

    wd = max(xi) - min(xi) + 1
    ht = max(yi) - min(yi) + 1

    arr = np.empty([wd, ht])
    arr[:] = np.nan

    for key, value in node_dict.items():
        arr[key[0]-min(xi),key[1]-min(yi)] = value

    fig, ax = plt.subplots()
    
    arr = np.rot90(arr)
    pc = ax.imshow(arr, cmap='viridis')
    
    fig.colorbar(pc, ax=ax)
    plt.xticks([])
    plt.yticks([])

    if title:
        ax.set_title(title)
    
    output_str = ''
    
    if mean:
        output_str += r'$\mu = $' + "{:.4f}".format(mean)
    if stddev:
        output_str += '\n' +  r'$\sigma=$' + "{:.4f}".format(stddev)
    if similarity:
        output_str += '\n similarity = ' + "{:.4f}".format(similarity)
    
    ax.set_xlabel(output_str)

    fig.set_size_inches(10,10)

    if spath:
        if not os.path.exists(spath):
            os.makedirs(spath)
        
        plt.savefig(spath + fname, dpi=500)
        plt.close()