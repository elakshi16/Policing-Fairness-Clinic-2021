import graph
import matplotlib.pyplot as plt
from matplotlib import cm
# make the data

myG = graph.Graph()
myG.createNodes(save_file="usr/src/out/nodes.pkl")
myG.populateNodes()
myG.saveNodes("usr/src/out/populated_nodes.pkl")


x = []
y = []
scalval = []
for key, node in myG.nodes.items():
  if (key[0] > 200 and key[1] < 200):
    x.append(key[0])
    y.append(key[1])
    scalval.append(len(node.pd_reports))
# size and color:

# plot
fig, ax = plt.subplots()

fig.set_size_inches(20,20)

# ax.scatter(x, y, s=arrCnt, alpha=0.2)
ax.scatter(x, y, s=1, c=scalval, cmap=cm.get_cmap('plasma')) # color instead of size 

ax.set(xlim=(0, 350), xticks=np.arange(1, 8),
       ylim=(0, 475), yticks=np.arange(1, 8))

plt.savefig("usr/out/graphics/pd_reports.png")
