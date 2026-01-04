import numpy as np
import random

SIGMOID = 'sigmoid'
TANH = 'tanh'


class Layer:
    def __init__(self, input_size: int, output_size: int, activation=''):
        self.neurons = [Neuron(input_size, activation) for _ in range(output_size)]

    def __call__(self, x):
        outs = [n(x) for n in self.neurons]
        return outs[0] if len(outs) == 1 else outs

    def parameters(self):
        return [p for neuron in self.neurons for p in neuron.parameters()]


class Neuron:
    def __init__(self, input_size, activation=SIGMOID):
        self.w = [Value(random.uniform(-1, 1)) for _ in range(input_size)]
        self.b = Value(random.uniform(-1, 1))
        self.activation = activation

    def __call__(self, x):
        act = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        if self.activation == TANH:
            return act.tanh()

        return act.sigmoid()

    def parameters(self):
        return self.w + [self.b]


class Value:
    def __init__(self, data, prev=(), _op="", label=""):
        self.data = data
        self.grad = 0.0
        self.compute_backward = lambda: None
        self.prev = set(prev)
        self._op = _op
        self.label = label

    def __repr__(self):
        return f"Value(data={self.data})"

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad

        out.compute_backward = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out.compute_backward = _backward

        return out

    def __pow__(self, other):
        out = Value(self.data ** other, (self,), f"**{other}")

        def _backward():
            self.grad += other * (self.data ** (other - 1)) * out.grad

        out.compute_backward = _backward

        return out

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * other ** -1

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __radd__(self, other):
        return self + other

    def exp(self):
        x = self.data
        out = Value(np.exp(x), (self,), "exp")

        def _backward():
            self.grad += out.data * out.grad

        out.compute_backward = _backward

        return out

    def log(self, base=np.e):
        x = self.data
        out = Value(np.log(x), (self,), f"log (base={base})")

        def _backward():
            self.grad += 1/(x*np.log(base)) * out.grad

        out.compute_backward = _backward

        return out

    def sigmoid(self):
        x = self.data
        t = 1 / (1 + np.exp(-x))
        out = Value(t, (self,), "sigmoid")

        def _backward():
            self.grad += (t * (1-t)) * out.grad

        out.compute_backward = _backward

        return out

    def tanh(self):
        x = self.data
        t = (np.exp(2 * x) - 1) / (np.exp(2 * x) + 1)
        out = Value(t, (self,), "tanh")

        def _backward():
            self.grad += (1 - t ** 2) * out.grad

        out.compute_backward = _backward

        return out

    def backward(self):
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v.prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        self.grad = 1.0
        for node in reversed(topo):
            node.compute_backward()



