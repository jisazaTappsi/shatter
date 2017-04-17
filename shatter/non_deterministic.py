#!/usr/bin/env python

"""
Defines methods to solve non-deterministic tables.
Notice: Keras and Numpy imports are defined withing functions, this is done in order to keep these libraries plus
TensorFlow as optional (only necessary for neural computing) and to shorten loading time as TensorFlow is very slow to
load.
"""

from shatter.util.code_dict import CodeDict

__author__ = 'juan pablo isaza'


def get_neural_network():

    from keras.models import Sequential
    from keras.layers import Dense
    import numpy as np

    dim = 1
    neuron_num = 1

    model = Sequential()

    layer = Dense(neuron_num, input_dim=dim, init='normal', activation='sigmoid')
    model.add(layer)

    # weights per layer:
    w1 = np.array([[1]])
    b1 = np.array([0] * dim)

    model.set_weights([w1, b1])

    return model


class LabeledData:
    """
    Suitable for Supervised Machine learning problem.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


def from_dict_to_lists(truth_tables):
    """
    This is the inverse function of
    >>> def from_lists_to_dict(x, y):

    Changes data representation from a dict to 2 arrays one with inputs and the other one with outputs
    (the x and y in machine learning).
    :param truth_tables: tables with possible contradictions.
    Table object Example:
    >>> {True: [(True,), (False,), (True,)], False: [(False,), (False,)]}
    :return: A LabeledData object suitable for machine learning.
    """
    x = []
    y = []
    for k, v in truth_tables.items():
        x += v
        y += [k] * len(v)

    return LabeledData(x, y)


def from_lists_to_dict(x, y):
    """
    This is the inverse function of
    >>> def from_dict_to_lists(truth_tables):

    Changes data representation from a machine learning representation (x, y pairs)
    to a truth_tables representation (dict with each output as key and values the truth table.)
    :param x: machine learning inputs.
    :param y: machine learning outputs.
    Table object Example:
    >>> {True: [(True,), (False,), (True,)], False: [(False,), (False,)]}
    :return: Tables dictionary, contains tables (see ProcessedRules class definition in shatter/processed_rules.py).
    """
    d = CodeDict()
    s = set(y)

    for out in s:
        y_indices = [idx for idx, e in enumerate(y) if e == out]
        x_values = [x[idx] for idx in y_indices]
        d[out] = x_values

    return d


def refining_neural_predictions(predictions):
    """
    Nets don't give precise values. Will round and convert to Boolean
    :param predictions: nested list with values between 0 and 1
    :return: Boolean array
    """
    return [bool(round(y[0])) for y in predictions]


def correct_truth_table(truth_tables):
    """
    Output code of a model that will predict correct outcome with "high" probability
    :param truth_tables: tables with possible contradictions.

    The type is CodeDict (see shatter/util/code_dict.py for details)

    CodeDict object Example:
    >>> {True: [(True,), (False,), (True,)], False: [(False,), (False,)]}
    :return: corrected truth table
    """
    from numpy import array

    print("""Solving non-deterministic problem (with possible contradictions), will use neural networks,
     can take a few minutes ...""")

    # train the model with a neural network
    nn = get_neural_network()

    # Compile model
    nn.compile(loss='mean_squared_error', optimizer='adam')

    data = from_dict_to_lists(truth_tables)

    epochs = 5000

    from keras.callbacks import EarlyStopping
    early_stopping_call_back = EarlyStopping(monitor='loss', min_delta=0, patience=100, verbose=0, mode='auto')

    nn.fit(data.x, data.y, nb_epoch=epochs, batch_size=10, verbose=True, callbacks=[early_stopping_call_back])

    possible_inputs = list(set(data.x))
    prediction = refining_neural_predictions(nn.predict([array(possible_inputs)]))

    return from_lists_to_dict(possible_inputs, prediction)

    # evaluate the model
    #scores = model.evaluate(x_test, y_test)

    #for layer in nn.layers:
    #    weights = layer.get_weights()  # list of numpy arrays

    # weights per layer:
    #w1 = np.array([[1, -1], [-1, 1]])
    #w2 = np.array([[0], [0]])

    #model.set_weights([w1, np.array([0] * dim),
    #       w2, np.array([0] * 1)])

    #return """
    #from keras.models import Sequential
    #from keras.layers import Dense
    #from numpy import array
    #from numpy import float32
#
    #model = Sequential()
    #layer = Dense(1, input_dim=1, init='normal', activation='sigmoid')
    #model.add(layer)
    #model.compile(loss='mean_squared_error', optimizer='adam')
    #model.set_weights({weights})
#
    #prediction = model.predict([array([int(a)])])
#
    #return bool(round(prediction[0][0]))""".format(weights=weights.__repr__())
