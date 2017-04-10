#!/usr/bin/env python

"""Defines methods to solve non-deterministic tables."""

from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from sklearn import svm


# TODO: remove from shatter.util import helpers

__author__ = 'juan pablo isaza'


def get_neural_network():

    dim = 1
    neuron_num = 1

    model = Sequential()

    layer = Dense(neuron_num, input_dim=dim, init='normal', activation='sigmoid')
    model.add(layer)

    return model


def get_model(table, all_inputs):
    """
    Output code of a model that will predict correct outcome with "high" probability
    :param table: list with tuples as rows.
    Example:
    >>> [(True,), (False,), (True,)]
    :param all_inputs: all possible function inputs.
    :return: a valid executable python code expression.
    """

    # train the model with a neural network
    nn = get_neural_network()

    # Compile model
    nn.compile(loss='mean_squared_error', optimizer='adam')

    x_train = [1, 0, 1, 0, 0]
    y_train = [1, 1, 1, 0, 0]
    epochs = 5000
    nn.fit(x_train, y_train, nb_epoch=epochs, batch_size=10, verbose=False)  #, callbacks=[early_stopping_call_back])

    # evaluate the model
    #scores = model.evaluate(x_test, y_test)

    for layer in nn.layers:
        weights = layer.get_weights()  # list of numpy arrays

    # weights per layer:
    #w1 = np.array([[1, -1], [-1, 1]])
    #w2 = np.array([[0], [0]])

    #model.set_weights([w1, np.array([0] * dim),
    #       w2, np.array([0] * 1)])

    return """
    from keras.models import Sequential
    from keras.layers import Dense
    from numpy import array
    from numpy import float32

    model = Sequential()
    layer = Dense(1, input_dim=1, init='normal', activation='sigmoid')
    model.add(layer)
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.set_weights({weights})

    prediction = model.predict([array([int(a)])])

    return bool(round(prediction[0][0]))""".format(weights=weights.__repr__())
