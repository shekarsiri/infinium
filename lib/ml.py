"""
Utilities for creating and manipulating machine learning models.

Copyright 2014, 2015 Jerrad M. Genson

This file is part of Infinium.

Infinium is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Infinium is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Infinium.  If not, see <http://www.gnu.org/licenses/>.

"""

# Third-party library imports
from sklearn.linear_model import SGDClassifier

# Infinium library imports
from lib.data import Developer
from lib.ui.config import get_config


__maintainer__ = Developer.JERRAD_GENSON
__contact__ = Developer.EMAIL[__maintainer__]


def construct_model():
    configuration = get_config()
    classifier = create_classifier()
    training_data = extract_training_data(database)
    train_classifier(classifier, training_data)

    return classifier


def create_classifier():
    configuration = get_config()
    return SGDClassifier(loss=configuration.sgd_loss,
                         penalty=configuration.sgd_penalty,
                         alpha=configuration.sgd_alpha,
                         l1_ratio=configuration.sgd_l1_ratio,
                         fit_intercept=configuration.sgd_fit_intercept,
                         n_iter=configuration.sgd_n_iter,
                         shuffle=configuration.sgd_shuffle,
                         verbose=configuration.sgd_verbose,
                         n_jobs=configuration.sgd_n_jobs,
                         learning_rate=configuration.sgd_learning_rate,
                         eta0=configuration.sgd_eta0,
                         power_t=configuration.sgd_power_t)


def extract_training_data(database):
    """
    Extract training data from database.
    """

    raise NotImplementedError('`extract_training_data` not yet implemented.')


def train_classifier(classifier, training_data):
    """
    Train classifier using the provided training data.
    """

    raise NotImplementedError('`train_classifier` not yet implemented.')


def load_model(path):
    raise NotImplementedError('`load_valuation_model` operation not yet implemented.')


def save_model(valuation_model, path):
    raise NotImplementedError('`save_valuation_model` operation not yet implemented.')


def evaluate_model(valuation_model, testing_data):
    raise NotImplementedError('`evaluate_model` operation not yet implemented.')