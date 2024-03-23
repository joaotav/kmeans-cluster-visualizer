#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

import warnings
import matplotlib.patches as mpatches
from random import randint
from math import sqrt
from matplotlib import pyplot as plt
import copy

plt.ion()

def initialize_dataset(filename):
    """
    Initialize the dataset by reading coordinates from the input file and assigning points
    to random clusters.
    """
    dataset = []
    with open(filename) as f:
        data = f.readlines()
        for line in data:
            x, y = map(float, line.strip().split())
            cluster = randint(0, 3)
            dataset.append([x, y, cluster])
    return dataset

def update_membership(dataset):
    """
    Update the membership of each data point by assigning it to the nearest cluster centroid.
    """
    centroids = []
    for centroid in range(4):
        pos_x, pos_y, members = 0, 0, 0
        for item in dataset:
            if item[2] == centroid:
                pos_x += item[0]
                pos_y += item[1]
                members += 1
        if members > 0:
            centroid_position = (pos_x / members, pos_y / members)
            centroids.append(centroid_position)
        else:
            print("Warning: Empty cluster found during centroid update.")
            centroids.append((0, 0))  # Placeholder centroid for empty clusters

    for i in range(len(dataset)):
        distances = [sqrt((dataset[i][0] - centroids[centroid][0])**2 + (dataset[i][1] - centroids[centroid][1])**2) for centroid in range(4)]
        dataset[i][2] = distances.index(min(distances))

def write_to_file(dataset, filename):
    """
    Write the final clustering result to a file.
    """
    with open(filename, 'w') as file:
        for line in dataset:
            file.write('{} {} {}\n'.format(line[0], line[1], line[2]))

def plot_clusters(dataset):
    """
    Plot the clusters.
    """
    colors = ['red', 'green', 'blue', 'black']
    patches = [mpatches.Patch(color=color, label=f'Cluster {i+1}') for i, color in enumerate(colors)]
    plt.legend(handles=patches)

    for centroid in range(4):
        plt.scatter([c[0] for c in dataset if c[2] == centroid], [c[1] for c in dataset if c[2] == centroid], c=colors[centroid])

def kmeans_clustering(filename):
    """
    Perform K-Means clustering on the given dataset.
    """
    dataset = initialize_dataset(filename)
    plot_clusters(dataset)
    plt.pause(0.1)

    iterations = 0
    while True:
        iterations += 1
        old_dataset = copy.deepcopy(dataset)
        update_membership(dataset)
        if dataset == old_dataset:
            print(f"Iterations: {iterations}")
            print("Image saved in 'clusters.png' and clusters info saved in 'result.dat'.")
            break
        plot_clusters(dataset)
        plt.pause(0.1)

    write_to_file(dataset, 'result.dat')
    plt.savefig('clusters.png')

if __name__ == "__main__":
    warnings.filterwarnings("ignore")  # Suppress matplotlib warnings
    kmeans_clustering('dataset.txt')
