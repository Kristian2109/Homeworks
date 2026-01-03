import numpy as np
from KMeans import KMeans, K_MEANS, K_MEANS_PLUS_PLUS, SILHOUETTE, WCSS
from plot_clusters import plot_data_and_centroids


def main():
    args = input().strip().split()
    file_name, alg_name, metric, n_clusters = args[0], args[1], args[2], int(args[3])
    random_restart = 3
    alg_name = K_MEANS_PLUS_PLUS
    metric = SILHOUETTE if metric == 1 else WCSS
    data: np.ndarray = np.loadtxt(file_name)
    k_means = KMeans(n_clusters, algorithm=alg_name, random_restart_iter=random_restart, metric=metric)
    labels = k_means.fit(data)

    plot_data_and_centroids(data, k_means.centroids, labels)


if __name__ == "__main__":
    main()