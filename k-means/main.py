import numpy as np
import numpy.random as r
from plot_clusters import plot_data_and_centroids


class KMeans:
    def __init__(self, n_clusters: int, metric='euclidean', evaluation_function='', max_iter=5):
        self.metric = metric
        self.evaluation_function = evaluation_function
        self.n_clusters = n_clusters
        self.centers = []
        self.max_iter = max_iter

    def fit(self, x: np.ndarray):
        best_centers = None
        best_wcss = 0
        best_labels = []
        for i in range(3):
            self.centers = self._get_initial_centroids(x)
            labels = []
            for i in range(self.max_iter):
                labels = self._get_new_labels(x)
                self.centers = self._get_new_means(x, labels)

            current_wcss = self.compute_wcss(x, labels)
            if best_centers is None or best_wcss > current_wcss:
                best_centers = self.centers
                best_wcss = current_wcss
                best_labels = labels

        self.centers = best_centers
        return best_labels

    def _get_new_labels(self, data: np.ndarray):
        labels = ((data[:, None, :] - self.centers[None, :, :])**2).sum(axis=2).argmin(axis=1)
        return np.asarray(labels, dtype=int)

    def _get_new_means(self, x: np.ndarray, labels: np.ndarray):
        counts = np.bincount(labels, minlength=self.n_clusters)
        sums = np.zeros((self.n_clusters, x.shape[1]), dtype=x.dtype)
        np.add.at(sums, labels, x)

        return np.divide(sums, counts[:, None], out=np.zeros_like(sums), where=counts[:, None] != 0)

    def _get_initial_centroids(self, x: np.ndarray):
        centroids = np.array([x[r.choice(len(x))]])
        while len(centroids) < self.n_clusters:
            distances = np.sum((x[:, None, :] - centroids[None, :, :])**2, axis=2)
            min_distances = np.min(distances, axis=1)
            probs = min_distances / np.sum(min_distances)
            idx = r.choice(len(x), p=probs)
            centroids = np.append(centroids, np.array([x[idx]]), axis=0)

        return centroids

    def compute_wcss(self, x: np.ndarray, labels: np.ndarray):
        distances = np.sum((x - self.centers[labels])**2, axis=1)
        return np.sum(distances)


def main():
    path = "Datasets/unbalance/unbalance.txt"
    data: np.ndarray = np.loadtxt(path)
    k_means = KMeans(8)
    labels = k_means.fit(data)

    plot_data_and_centroids(data, k_means.centers, labels)


if __name__ == "__main__":
    main()