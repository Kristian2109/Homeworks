import numpy as np
from NeuralNetwork import Layer, SIGMOID, TANH


DATA_PER_FUNCTION = {
    'AND': {
        'x': np.array([[0, 0], [0, 1], [1, 0], [1, 1], [1, 1]]),
        'y': np.array([0, 1, 0, 0, 1])
    },
    'OR': {
        'x': np.array([[0, 0], [0, 1], [1, 0], [1, 1], [0, 0]]),
        'y': np.array([0, 1, 1, 1, 0])
    },
    'XOR': {
        'x': np.array([[0, 0], [0, 1], [1, 0], [1, 1]]),
        'y': np.array([0, 1, 1, 0])
    }
}


class SimpleNeuralNetwork:
    def __init__(self, layer_sizes: list[int], activation=''):
        self.layers = [
            Layer(layer_sizes[i], layer_sizes[i + 1], activation)
            for i in range(len(layer_sizes) - 1)
        ]

    def predict(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

    def parameters(self):
        return [p for layer in self.layers
                    for p in layer.parameters()]

    def train(self, x, y, learning_rate=0.5, epochs=20):
        for k in range(epochs):
            y_pred = [self.predict(v) for v in x]
            loss = sum((y_out - y_true) ** 2 for y_true, y_out in zip(y, y_pred)) / len(x)

            for p in self.parameters():
                p.grad = 0.0
            loss.backward()

            for p in self.parameters():
                p.data -= learning_rate * p.grad


def train_for_function(layers_sizes, act_function, data):
    model = SimpleNeuralNetwork(layers_sizes, act_function)
    model.train(data['x'], data['y'], epochs=1000)

    for t in data['x']:
        print(f"{(t[0], t[1])} -> {model.predict(t):.4f}")


def main():
    inp = input().strip().split()
    func_name = inp[0]
    act_function = TANH if inp[1] == 1 else SIGMOID
    hidden_layers_count = int(inp[2])
    neurons_per_hidden_layer = int(inp[3])

    hidden_layers = [neurons_per_hidden_layer for _ in range(hidden_layers_count)]
    layers_sizes = [2] + hidden_layers + [1]

    if func_name == 'ALL':
        for data in DATA_PER_FUNCTION.values():
            train_for_function(layers_sizes, act_function, data)
    else:
        data = DATA_PER_FUNCTION.get(func_name, 'AND')
        train_for_function(layers_sizes, act_function, data)


if __name__ == '__main__':
    main()