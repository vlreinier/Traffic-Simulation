import os
import matplotlib.pyplot as plt 
import pandas as pd
folders = os.listdir("./data")
sorts = {}
for f in folders:
    if f[:6] in sorts:
        sorts[f[:6]].append(f)
    else:
        sorts[f[:6]] = [f]


# Create the boxplot

for key, item in sorts.items():
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)
    data = []
    names = []
    item.sort()
    for i in item:
        name = i[7:]
        df = pd.read_csv("./data/{}/properties_1000.csv".format(i), delimiter=",")
        data.append(df["speed"])
        names.append(name)
    bp = ax.boxplot(data, labels=names)

    plt.show()

