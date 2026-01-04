from Layer import Layer


class SimpleNeuralNetwork:
    def __init__(self, layer_sizes: list[int], activation=''):
        self.layers = [
            Layer(layer_sizes[i], layer_sizes[i + 1], activation)
            for i in range(len(layer_sizes) - 1)
        ]

    def train(self, x, y, learning_rate=1, epochs=20):
        for k in range(epochs):
            y_pred = [self.predict(v) for v in x]
            loss = mean_squared_loss(y, y_pred)

            for p in self.parameters():
                p.grad = 0.0
            loss.backward()

            for p in self.parameters():
                p.data -= learning_rate * p.grad

    def predict(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]


def mean_squared_loss(y_true, y_pred):
    return sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / len(y_true)