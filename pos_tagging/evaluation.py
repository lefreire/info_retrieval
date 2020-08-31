import logging
import numpy as np
from sklearn.metrics import accuracy_score


class Evaluation:

  def __init__(self):
    """
      Constructor
    """
    logging.basicConfig(level=logging.INFO)

  def calculate_accuracy(self, tag_true, tag_pred):
    """
        Calculating accuracy

        Parameters
        ----------
        tag_true: list strings
        tag_pred: list of strings

        Returns
        -------
        accuracy_score: float
    """
    return accuracy_score(tag_true, tag_pred)

  def count_right_tags(self, y_true, y_pred, dict_tags):
    """
        Counting how many tags were predicted correctly

        Parameters
        ----------
        y_true: list of strings
        y_pred: list of strings
        dict_tags: dictionary, in format {tag: {right: # tags, pred: # predicted correctly}}

        Returns
        -------
        dict_tags: dictionary
    """
    tmp_tags = list(set(y_true))
    for tag in tmp_tags:
      occ_tag = np.where(np.array(y_true) == tag)[0] 
      occ_pred = np.where(np.array(y_pred) == tag)[0] 
      dict_tags[tag]['right'] += len(occ_tag)
      dict_tags[tag]['pred'] += len(list(set(occ_tag).intersection(set(occ_pred))))
    return dict_tags

  def get_accuracy(self, y_test, y_pred, dict_tags):
    """
        Main method
    """
    logging.info('Calculando acurácia')
    acc = []
    for index in range(0, len(y_test)):
      acc.append(self.calculate_accuracy(y_test[index], y_pred[index]))
      dict_tags = self.count_right_tags(y_test[index], y_pred[index], dict_tags)
    return np.mean(acc), dict_tags

