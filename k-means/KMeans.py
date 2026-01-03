import numpy as np
import numpy.random as r

K_MEANS_PLUS_PLUS = 'k-means++'
K_MEANS = 'k-means'
WCSS = 'wcss'
SILHOUETTE = 'silhouette'


class KMeans:
    def __init__(self,
                 n_clusters: int,
                 algorithm=K_MEANS_PLUS_PLUS,
                 metric='wcss',
                 max_iter=5,
                 random_restart_iter=3):
        self.metric = metric
        self.n_clusters = n_clusters
        self.centroids = []
        self.max_iter = max_iter
        self.random_restart_iter = random_restart_iter
        self.algorithm = algorithm
        self.evaluation_function = self._compute_silhouette_score if metric == SILHOUETTE else self._compute_wcss

    def fit(self, x: np.ndarray):
        best_centers = None
        best_score = 0
        best_labels = []
        for _ in range(self.random_restart_iter):
            self.centroids = self._get_initial_centroids(x)
            for __ in range(self.max_iter):
                labels = self._get_new_labels(x)
                self.centroids = self._get_new_means(x, labels)

            current_score = self.evaluation_function(x, labels)
            if self.is_better(current_score, best_score) or best_centers is None:
                best_centers = self.centroids
                best_score = current_score
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

    def _compute_wcss(self, x: np.ndarray, labels: np.ndarray) -> np.float32:
        distances = np.sum((x - self.centroids[labels]) ** 2, axis=1)
        return np.sum(distances)

    def _compute_silhouette_score(self, x: np.ndarray, labels: np.ndarray) -> np.float32:
        distances_matrix = np.sum((x[:, None, :] - x[None, :, :])**2, axis=2)

        a = np.zeros(len(x))
        for i in range(len(x)):
            same_cluster = labels == labels[i]
            same_cluster[i] = False
            a[i] = np.mean(distances_matrix[i, same_cluster])

        b = np.full(len(x), np.inf)
        for i in range(len(x)):
            unique_clusters = range(self.n_clusters)
            for cluster in unique_clusters:
                if cluster == labels[i]:
                    continue
                current_mean = np.mean(distances_matrix[i, labels == cluster])
                b[i] = np.minimum(b[i], current_mean)

        return np.mean((b - a) / np.maximum(a, b))

    def is_better(self, f, s):
        if self.metric == SILHOUETTE:
            return f > s
        if self.metric == WCSS:
            return f < s

        return f < s