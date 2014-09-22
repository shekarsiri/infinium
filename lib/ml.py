"""
Utilities for creating and manipulating machine learning models.

Copyright 2014 Jerrad M. Genson

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


__maintainer__ = Developer.JERRAD_GENSON
__contact__ = Developer.EMAIL[__maintainer__]


def construct_model(configuration):
    classifier = create_classifier(configuration)
    training_data = extract_training_data(database)
    train_classifier(classifier, training_data, configuration)

    return classifier


def create_classifier(configuration):
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


def load_model(path):
    raise NotImplementedError('`load_valuation_model` operation not yet implemented.')


def save_model(valuation_model, path):
    raise NotImplementedError('`save_valuation_model` operation not yet implemented.')