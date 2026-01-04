import numpy as np
from Layer import SIGMOID, TANH
from SimpleNeuralNetwork import SimpleNeuralNetwork


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


def train_for_function(layers_sizes, act_function, data):
    model = SimpleNeuralNetwork(layers_sizes, act_function)
    model.train(data['x'], data['y'], epochs=2000)

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
            print(f"{k}:")
            train_for_function(layers_sizes, act_function, DATA_PER_FUNCTION[k])
    else:
        print(f"{func_name}:")
        data = DATA_PER_FUNCTION.get(func_name, 'AND')
        train_for_function(layers_sizes, act_function, data)


if __name__ == '__main__':
    main()