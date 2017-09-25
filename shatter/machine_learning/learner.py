#!/usr/bin/env python

"""
Defines methods to solve non-deterministic tables.
Notice: Keras and Numpy imports are defined withing functions, this is done in order to keep these libraries plus
TensorFlow as optional (only necessary for neural computing) and to shorten loading time as TensorFlow is very slow to
load.
"""

import numpy as np

from shatter.machine_learning.labeled_data import from_lists_to_dict, from_dict_to_lists
from shatter.machine_learning.neural_network import get_neural_network, round_neural_predictions

__author__ = 'juan pablo isaza'

EPOCHS = 1
BATCH_SIZE = 500
DATA_SIZE_MUTIPLIER = 5000


def correct_truth_table(truth_tables):
    """
    Output code of a model that will predict correct outcome with "high" probability
    :param truth_tables: tables with possible contradictions.

    The type is CodeDict (see shatter/util/code_dict.py for details)

    CodeDict object Example:
    >>> {True: [(True,), (False,), (True,)], False: [(False,), (False,)]}
    :return: corrected truth table
    """
    print("""Solving non-deterministic problem (with possible contradictions), will use neural networks,
     can take a few minutes ...""")

    data = from_dict_to_lists(truth_tables)

    # multiplies data to use big batch_size and speed up training.
    data.x = [e for e in data.x * DATA_SIZE_MUTIPLIER]
    data.y = [e for e in data.y * DATA_SIZE_MUTIPLIER]

    # train the model with a neural network
    nn = get_neural_network(data)

    # Compile model
    nn.compile(loss='mean_squared_error', optimizer='adam')

    from keras.callbacks import EarlyStopping
    early_stopping_call_back = EarlyStopping(monitor='loss', min_delta=0, patience=100, verbose=0, mode='auto')

    nn.fit(data.x, data.y, nb_epoch=EPOCHS, batch_size=BATCH_SIZE, verbose=True, callbacks=[early_stopping_call_back])

    possible_inputs = list(set(data.x))
    prediction = round_neural_predictions(nn.predict([np.array(possible_inputs)]))

    return from_lists_to_dict(possible_inputs, prediction)
