import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

results = pd.read_csv("../data/results.csv")
results = results[['obstacle_lane', 'vehicle_frequency', 'speed']]
data = {}
for freq in results.groupby('vehicle_frequency'):
    obstacle_lanes = []
    speeds = []
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    for lane in freq[1].groupby(['obstacle_lane']):
        obstacle_lanes.append(lane[0])
        speeds.append(list(lane[1]['speed']))
    print(obstacle_lanes)
    data[str(freq[0])] = speeds
    bp = ax.boxplot(speeds, labels=obstacle_lanes)
    plt.title('Voertuig frequency '+str(freq[0]))
    plt.xlabel('Obstakel op baan (-1 is nulmeting)')
    plt.ylabel('Snelheid')
    plt.savefig('../Data/'+str(freq[0])+ '.png')
    plt.clf()

for key, item in data.items():
    index = 0
    for k in item:
        d = np.array(k)
        print("==========lane {} freq {}============".format(index, key))
        print("STD: {}".format(d.std()))
        print("AVG: {}".format(d.mean()))
        index_1 = 0
        for i in item:
            if index_1 != index:
                st = stats.ttest_ind(i, k)
                print("P-value on lane {} op lane {}: {}".format(index, index_1, st.pvalue))
            index_1 += 1
        index += 1