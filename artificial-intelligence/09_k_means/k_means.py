#!/usr/bin/env python3

"""CLI Tool for calculating clusters of 2d data."""

import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt


def read_2d_data(file_name):
    """Read data from csv as 2d vectors."""
    with open(file_name) as file_descriptor:
        data = csv.reader(file_descriptor,
                          delimiter='\t', quotechar='\n')
        return np.array([[float(digit) for digit in row]
                         for row in data])


def get_classes(data, centers):
    """Calculate data classes."""
    return [np.argmin([(xd - x) ** 2 + (yd - y) ** 2
                       for x, y in centers])
            for xd, yd in data]


def get_medians(data, k, classes):
    """Calculate the new positions of the centers."""
    return [np.mean(data[[idx for idx, c in enumerate(classes)
                          if c == cls]], axis=0) for cls in range(k)]


def k_means(data, k):
    """Implementation of k-means."""
    rand_indexes = np.random.randint(len(data), size=k)
    old_centers = []
    centers = data[rand_indexes]

    while not np.array_equal(old_centers, centers):
        classes = get_classes(data, centers)
        old_centers = centers
        centers = get_medians(data, k, classes)

    return centers, get_classes(data, centers)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Cluster 2d data from csv file.'
    )

    parser.add_argument(
        '--input_file', type=str, nargs='?',
        help='The name of the output file - ex.: data/normal.txt.',
        default='data/normal.txt'
    )
    parser.add_argument(
        '--k', type=int, nargs='?',
        help='The number of desired clusters.',
        default=4
    )

    args = parser.parse_args()

    data = read_2d_data(args.input_file)
    k = args.k

    # Apply k-means to our data.
    cluster_centers, assigned_centers = k_means(data, k)

    # Print some info about the clustering.
    print('Cluster centers:', cluster_centers)
    print('Data has length:', len(data))
    print('Assigned cluster centers list has length:', len(assigned_centers))
    print('Sample of assigned centers:', assigned_centers[:5])

    # Display the clusters.
    plt.scatter(data[:, 0], data[:, 1],
                c=[(float(i) / 10) for i in assigned_centers])
    plt.show()


if __name__ == '__main__':
    main()
