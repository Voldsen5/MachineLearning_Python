"""
Created on Wed Mar 3 16:39:18 2021
@author: Sila
"""

# Gettting started methods for TSP GA algorithm
# - Read cities from file
#

import pandas as pd
import random
import math

data = pd.read_csv('TSPcities1000.txt', sep='\s+', header=None)
data = pd.DataFrame(data)

import matplotlib.pyplot as plt
x = data[1]
y = data[2]
plt.plot(x, y,'r.')
plt.show()


def createRandomRoute():
    tour = [[i] for i in range(1000)]
    random.shuffle(tour)
    return tour

# plot the tour - Adjust range 0..len, if you want to plot only a part of the tour.
def plotCityRoute(route):
    for i in range(0, len(route)):
        plt.plot(x[i:i + 2], y[i:i + 2], 'ro-')
    plt.show()

# Alternativ kode:
#  for i in range(0, len(route)-1):              
#     plt.plot([x[route[i]],x[route[i+1]]], [y[route[i]],y[route[i+1]]], 'ro-')

tour = createRandomRoute()
print(tour)
plotCityRoute(tour)

# calculate distance between cities
def distancebetweenCities(city1x, city1y, city2x, city2y):
    xDistance = abs(city1x-city2x)
    yDistance = abs(city1y-city2y)
    distance = math.sqrt((xDistance * xDistance) + (yDistance * yDistance))
    return distance

# distance between city number 100 and city number 105
dist= distancebetweenCities(x[100], y[100], x[105], y[105])
print('Distance, % target: ', dist)

best_score_progress = []  # Tracks progress

# replace with your own calculations
fitness_gen0 = 1000 # replace with your value
print('Starting best score, % target: ', fitness_gen0)

best_score = fitness_gen0
# Add starting best score to progress tracker
best_score_progress.append(best_score)

# Here comes your GA program...
best_score = 980
best_score_progress.append(best_score)
best_score = 960
best_score_progress.append(best_score)


# GA has completed required generation
print('End best score, % target: ', best_score)

plt.plot(best_score_progress)
plt.xlabel('Generation')
plt.ylabel('Best Fitness - route length - in Generation')
plt.show()
