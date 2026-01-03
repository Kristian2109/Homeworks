import numpy as np
import numpy.random as r

K_MEANS_PLUS_PLUS = 'k-means++'
K_MEANS = 'k-means'


class KMeans:
    def __init__(self,
                 n_clusters: int,
                 algorithm=K_MEANS_PLUS_PLUS,
                 metric='euclidean',
                 evaluation_function='',
                 max_iter=5,
                 random_restart_iter=3):
        self.metric = metric
        self.evaluation_function = evaluation_function
        self.n_clusters = n_clusters
        self.centroids = []
        self.max_iter = max_iter
        self.random_restart_iter = random_restart_iter
        self.algorithm = algorithm

    def fit(self, x: np.ndarray):
        best_centers = None
        best_wcss = 0
        best_labels = []
        for i in range(self.random_restart_iter):
            self.centroids = self._get_initial_centroids(x)
            labels = []
            for i in range(self.max_iter):
                labels = self._get_new_labels(x)
                self.centroids = self._get_new_means(x, labels)

            current_wcss = self._compute_wcss(x, labels)
            if best_wcss > current_wcss or best_centers is None:
                best_centers = self.centroids
                best_wcss = current_wcss
                best_labels = labels

        self.centroids = best_centers
        return best_labels

    def _get_new_labels(self, data: np.ndarray):
        labels = ((data[:, None, :] - self.centroids[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        return np.asarray(labels, dtype=int)

    def _get_new_means(self, x: np.ndarray, labels: np.ndarray):
        counts = np.bincount(labels, minlength=self.n_clusters)
        sums = np.zeros((self.n_clusters, x.shape[1]), dtype=x.dtype)
        np.add.at(sums, labels, x)

        return np.divide(sums, counts[:, None], out=np.zeros_like(sums), where=counts[:, None] != 0)

    def _get_initial_centroids(self, x: np.ndarray):
        if self.algorithm == K_MEANS:
            idx = r.choice(len(x), size=self.n_clusters, replace=False)
            return x[idx]

        centroids = np.array([x[r.choice(len(x))]])
        while len(centroids) < self.n_clusters:
            distances = np.sum((x[:, None, :] - centroids[None, :, :])**2, axis=2)
            min_distances = np.min(distances, axis=1)
            probs = min_distances / np.sum(min_distances)
            idx = r.choice(len(x), p=probs)
            centroids = np.append(centroids, np.array([x[idx]]), axis=0)

        return centroids

    def _compute_wcss(self, x: np.ndarray, labels: np.ndarray):
        distances = np.sum((x - self.centroids[labels]) ** 2, axis=1)
        return np.sum(distances)
