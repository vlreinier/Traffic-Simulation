import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv("C:\\GitHub\\Traffic-Simulation\\Data\\results.csv")
results = results[['obstacle_lane', 'vehicle_frequency', 'speed']]

for freq in results.groupby('vehicle_frequency'):
    obstacle_lanes = []
    speeds = []
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)

    for lane in freq[1].groupby(['obstacle_lane']):
        obstacle_lanes.append(lane[0])
        speeds.append(list(lane[1]['speed']))

    bp = ax.boxplot(speeds, labels=obstacle_lanes)
    plt.title('Voertuig frequency '+str(freq[0]))
    plt.xlabel('Obstakel op baan (-1 is nulmeting)')
    plt.ylabel('Snelheid')
    plt.savefig('C:\\GitHub\\Traffic-Simulation\\Data\\'+str(freq[0])+ '.png')
    plt.clf()

