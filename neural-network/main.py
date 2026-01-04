import numpy as np
from NeuralNetwork import Layer, SIGMOID, TANH


DATA_PER_FUNCTION = {
    'AND': {
        'x': np.array([[0, 0], [0, 1], [1, 0], [1, 1], [1, 1]]),
        'y': np.array([0, 0, 0, 1, 1])
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
        return [p for layer in self.layers for p in layer.parameters()]


def train(model, x, y, learning_rate=1, epochs=20):
    for k in range(epochs):
        y_pred = [model.predict(v) for v in x]
        loss = sum((y_out - y_true) ** 2 for y_true, y_out in zip(y, y_pred)) / len(x)

        for p in model.parameters():
            p.grad = 0.0
        loss.backward()

        for p in model.parameters():
            p.data -= learning_rate * p.grad


def train_for_function(layers_sizes, act_function, data):
    model = SimpleNeuralNetwork(layers_sizes, act_function)
    train(model, data['x'], data['y'], epochs=2000)

    for t in data['x'][:4]:
        print(f"{(int(t[0]), int(t[1]))} -> {model.predict(t).data:.4f}")


def main():
    inp = input().strip().split()
    func_name = inp[0]
    act_function = TANH if inp[1] == 1 else SIGMOID
    hidden_layers_count = int(inp[2])
    neurons_per_hidden_layer = int(inp[3])

    hidden_layers = [neurons_per_hidden_layer for _ in range(hidden_layers_count)]
    layers_sizes = [2] + hidden_layers + [1]

    if func_name == 'ALL':
        for k in DATA_PER_FUNCTION.keys():
            print(k)
            train_for_function(layers_sizes, act_function, DATA_PER_FUNCTION[k])
    else:
        data = DATA_PER_FUNCTION.get(func_name, 'AND')
        train_for_function(layers_sizes, act_function, data)


if __name__ == '__main__':
    main()