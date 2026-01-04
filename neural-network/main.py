import numpy as np
from NeuralNetwork import Layer


class MLP:
    def __init__(self, layer_sizes: list[int]):
        self.layers = [
            Layer(layer_sizes[i], layer_sizes[i + 1])
            for i in range(len(layer_sizes) - 1)
        ]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self):
        return [p for layer in self.layers
                    for p in layer.parameters()]


def train(model, X, y, learning_rate=0.5, epochs=20):
    for k in range(epochs):
        y_pred = [model(x) for x in X]
        loss = sum((y_out - y_true) ** 2 for y_true, y_out in zip(y, y_pred)) / len(X)

        for p in model.parameters():
            p.grad = 0.0
        loss.backward()

        for p in model.parameters():
            p.data -= learning_rate * p.grad


def main():
    x = np.array([[0, 1], [1, 1], [1, 0], [0, 0]])
    y = np.array([0, 1, 0, 0])

    model = MLP([2, 7, 1])
    train(model, x, y, epochs=1000)

    for t in x:
        print(model(t))


if __name__ == '__main__':
    main()