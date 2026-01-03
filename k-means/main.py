import numpy as np
from KMeans import KMeans, K_MEANS, K_MEANS_PLUS_PLUS
from plot_clusters import plot_data_and_centroids


def main():
    # args = input().strip().split()
    # file_name, alg_name, metric, n_clusters = args[0], args[1], args[2], int(args[3])
    file_name = 'Datasets/unbalance/unbalance.txt'
    n_clusters = 8
    random_restart = 3
    alg_name = K_MEANS_PLUS_PLUS
    data: np.ndarray = np.loadtxt(file_name)
    k_means = KMeans(n_clusters, algorithm=alg_name, random_restart_iter=random_restart)
    labels = k_means.fit(data)

    plot_data_and_centroids(data, k_means.centroids, labels)


if __name__ == "__main__":
    main()