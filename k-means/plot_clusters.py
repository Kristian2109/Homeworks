import matplotlib.pyplot as plt
import seaborn as sns
import sys


def plot_data_and_centroids(data, centroids, labels):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=labels, palette='Set1', s=100, legend='full')

    plt.scatter(centroids[:, 0], centroids[:, 1], c='black', s=300, marker='X', label='Centroids')
    
    plt.title('Data and Centroids Visualization')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python plot_clusters.py <data_file> <centroids_file> <labels_file>")
        sys.exit(1)

    data_file = sys.argv[1]
    centroids_file = sys.argv[2]
    labels_file = sys.argv[3]
    plot_data_and_centroids(data_file, centroids_file, labels_file)
