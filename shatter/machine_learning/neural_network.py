#!/usr/bin/env python

"""
Defines the neural network architecture, weights and any other specifics.
"""

__author__ = 'juan pablo isaza'


def get_layer_sequence(n):
    """
    1
    1, 2
    1, 2, 2, 3, 3
    1, 2, 2, 2, 3, 3, 3, 4, 4, 4?
    :param n: integer
    :return: [n, n, n-1, n-1, n-2, n-2... 2, 2, 1]
    """
    if n == 1:
        return [1]
    if n == 2:
        return [2, 1]
    if n == 3:
        return [3, 3, 2, 2, 1]
    if n == 4:
        return [4, 4, 4, 3, 3, 3, 2, 2, 2, 1]

    # TODO: generalize, this formula is a little bit off:
    #return [math.ceil((x+2)/2) for x in reversed(range(n*2 - 1))]


def set_weights(model, first_layer_dim):
    """
    weights per layer:
    :param model: neural network
    :param first_layer_dim: a int for the dimension of the base layer.
    :return: modified network with preset weights.
    """
    import numpy as np

    if first_layer_dim == 1:
        w1 = np.array([[1]])
        b1 = np.array([0] * first_layer_dim)
        model.set_weights([w1, b1])

    if first_layer_dim == 2:
        # weights per layer:
        w1 = np.array([[1, -1], [-1, 1]])
        w2 = np.array([[0], [0]])

        model.set_weights([w1, np.array([0] * first_layer_dim),
           w2, np.array([0] * 1)])

    if first_layer_dim == 3:
        w1 = np.array([[1, 1, -1],
           [1, -1, 1],
           [-1, 1, 1]])
        w2 = np.array([[-1, 1, 1],
           [1, -1, 1],
           [1, 1, -1]])
        w3 = np.array([[0, 0], [0, 0], [0, 0]])
        w4 = np.array([[1, -1], [-1, 1]])
        w5 = np.array([[0], [0]])

        model.set_weights([w1, np.array([0]*3),
           w2, np.array([0]*3),
           w3, np.array([0]*2),
           w4, np.array([0]*2),
           w5, np.array([0]*1),])

    if first_layer_dim == 4:
        w1 = np.array([[-1, -1, 1, 1],
           [1, -1, -1, 1],
           [1, 1, -1, -1],
           [-1, 1, 1, -1]])
        w2 = np.array([[-1, 1, 1, -1],
           [1, 1, -1, -1],
           [1, -1, -1, 1],
           [-1, -1, 1, 1]])
        w3 = np.array([[-1, -1, 1, 1],
           [1, -1, -1, 1],
           [1, 1, -1, -1],
           [-1, 1, 1, -1]])
        w4 = np.array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]])
        w5 = np.array([[-1, 1, 1],
           [1, -1, 1],
           [1, 1, -1]])
        w6 = np.array([[1, 1, -1],
           [1, -1, 1],
           [-1, 1, 1]])
        w7 = np.array([[0, 0], [0, 0], [0, 0]])
        w8 = np.array([[1, -1], [-1, 1]])
        w9 = np.array([[1, -1], [-1, 1]])
        w10 = np.array([[0], [0]])

        model.set_weights([w1, np.array([0]*4),
                           w2, np.array([0]*4),
                           w3, np.array([0]*4),
                           w4, np.array([0]*3),
                           w5, np.array([0]*3),
                           w6, np.array([0]*3),
                           w7, np.array([0]*2),
                           w8, np.array([0]*2),
                           w9, np.array([0]*2),
                           w10, np.array([0]*1), ])

    return model


def add_layers(model, first_layer_dim):
    """
    Adds the layers of the sequence to the model
    :param model:
    :param first_layer_dim: dimension as a int.
    :return: net model
    """
    from keras.layers import Dense

    for neuron_num in get_layer_sequence(first_layer_dim):

        if len(model.layers) == 0 and first_layer_dim > 1:
            activation = 'relu'
        else:
            activation = 'sigmoid'

        layer = Dense(neuron_num, input_dim=first_layer_dim, init='normal', activation=activation)
        model.add(layer)

    return model


def get_neural_network(data):
    """
    Returns a model.
    :param data: Data object.
    :return: a Keras neural network model
    """
    from keras.models import Sequential

    first_layer_dim = define_first_layer_dim(data.x)

    model = Sequential()

    model = add_layers(model, first_layer_dim)

    model = set_weights(model, first_layer_dim)

    return model


def round_neural_predictions(predictions):
    """
    Nets don't give precise values. Will round and convert to Boolean
    :param predictions: nested list with values between 0 and 1
    :return: Boolean array
    """
    return [bool(round(y[0])) for y in predictions]


def define_first_layer_dim(x):
    """
    Defines the dimension of the first neural network layer.
    :param x: list with input data. Where each row is a tuple.
    :return: int
    """
    # TODO: go to higher dimensions
    max_dim = 4

    if len(x[0]) <= max_dim:
        return len(x[0])
    else:
        return max_dim
