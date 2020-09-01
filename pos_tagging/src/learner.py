import logging
import numpy as np 
import pandas as pd
import random


class Learner:

  def __init__(self):
    """
      Constructor
    """
    self.observations_mtx = None
    self.transitions_mtx = None
    self.pi_mtx = None
    logging.basicConfig(level=logging.INFO)

  def count_tags(self, tag_target, tags):
    """
      Counting how many times tag_target appears in the corpus

      Parameters
      ----------
      tag_target: string
      tags: list of string

      Returns
      -------
      total_tags: int
    """ 
    total_tags = 0
    for tag in tags:
      total_tags += tag.count(tag_target)
    return total_tags

  def initial_tags(self, tag_target, tags):
    """
        Counting how many times tag_target starts the sentence

        Parameters
        ----------
        tag_target: string
        tags: list of string

        Returns
        -------
        total_initial_tag: int
    """ 
    total_initial_tag = 0
    for tag in tags:
      if tag[0] == tag_target: total_initial_tag += 1
    return total_initial_tag

  def calculate_pi_probs(self, tag_target, tags):
    """
        Calculating tag_target initial probability

        Parameters
        ----------
        tag_target: string
        tags: list of string

        Returns
        -------
        pi_prob: float
    """ 
    total_initial_tag = self.initial_tags(tag_target, tags)
    return total_initial_tag/len(tags)

  def get_all_tags(self, tags):
    """
        Getting all tags in corpus

        Parameters
        ----------
        tags: list of lists

        Returns
        -------
        all_tags: list
    """
    all_tags = []
    for tag_list in tags:
      all_tags.extend(tag_list)
    return np.unique(all_tags)

  def get_all_words(self, sentences):
    """
        Getting all words in corpus

        Parameters
        ----------
        sentences: list of lists

        Returns
        -------
        all_words: list
    """
    all_words = []
    for sentence in sentences:
      all_words.extend(sentence)
    return np.unique(all_words)

  def matrix_obs(self, tags, sentences):
    """
        Calculating observations probabilities

        Parameters
        ----------
        tags: list of lists
        sentences: list of lists

        Returns
        -------
        matrix_prob_obs: pandas.DataFrame, with columns = tags and lines = words
    """
    logging.info('Calculando matriz de probabilidades de observações')
    all_words = self.get_all_words(sentences)
    all_tags = self.get_all_tags(tags)
    matrix_prob_obs = {}
    for tag in all_tags:
      matrix_prob_obs[tag] = {}
      for word in all_words:
        matrix_prob_obs[tag][word] = 0.0
    for index in range(0, len(sentences)):
      for word, tag in zip(sentences[index], tags[index]):
        matrix_prob_obs[tag][word] += 1.0
    matrix_prob_obs = pd.DataFrame(data=matrix_prob_obs)
    for tag in all_tags:
      total_tag = self.count_tags(tag, tags)
      matrix_prob_obs[tag] = matrix_prob_obs[tag]/total_tag
    return matrix_prob_obs

  def matrix_trans(self, tags):
    """
        Calculating transitions probabilities between tags

        Parameters
        ----------
        tags: list of lists

        Returns
        -------
        matrix_prob_trans: pandas.DataFrame, with columns = previous tags and lines = current tags
    """
    logging.info('Calculando matriz de probabilidades de transição')
    all_tags = self.get_all_tags(tags)
    matrix_prob_trans = {}
    for tag in all_tags:
      matrix_prob_trans[tag] = {}
      for tag_target in all_tags:
        matrix_prob_trans[tag][tag_target] = 0.0
    for tag_list in tags:
      for index in range(1, len(tag_list)):
        matrix_prob_trans[tag_list[index]][tag_list[index-1]] += 1.0
    matrix_prob_trans = pd.DataFrame(data=matrix_prob_trans)
    matrix_prob_trans = matrix_prob_trans.T
    for tag_prev in all_tags:
      total_tag = self.count_tags(tag_prev, tags)
      matrix_prob_trans[tag_prev] = matrix_prob_trans[tag_prev]/total_tag
    return matrix_prob_trans.T

  def initial_probs(self, tags):
    """
        Calculating initial probabilities for all tags

        Parameters
        ----------
        tags: list of lists

        Returns
        -------
        initial_prob: pandas.DataFrame, with columns = tags and lines = probability
    """
    logging.info('Calculando matriz de probabilidades inicial (pi)')
    all_tags = self.get_all_tags(tags)
    initial_prob = {}
    for tag in all_tags:
      initial_prob[tag] = {}
      initial_prob[tag]['pi'] = self.calculate_pi_probs(tag, tags)
    return pd.DataFrame(data=initial_prob)

  def get_index(self, observations, word):
    """
        Getting the index of each word in the observations DataFrame
        If the word doesn't exist there, a random index will be attributed to this word

        Parameters
        ----------
        observations: pandas.DataFrame, with columns = words and lines = tags
        word: string

        Returns
        -------
        index: int 
    """
    columns = observations.columns
    if not word in observations.columns.tolist():
      return random.randint(0, len(columns)-1) 
    return columns.get_loc(word)
    
  def obs_column(self, obs, obs_array):
    """
        Getting the column in a numpy array, giving the obs index

        Parameters
        ----------
        obs: int
        obs_array: numpy.array

        Returns
        -------
        obs_array[:]: numpy.array, with 1 column 
    """
    return obs_array[:, obs, None]
    
  def viterbi(self, data, transitions, observations, pi_probs):
    """
        Calculating Viterbi algorithm

        Parameters
        ----------
        data: list of string
        transitions: pandas.DataFrame, with columns = previous tags and lines = current tags
        observations: pandas.DataFrame, with columns = words and lines = tags
        pi_probs: numpy.array, with 1 column

        Returns
        -------
        tokens: list with indexes, indicating the tag index of each word in data
    """
    obs = np.array(observations)
    transitions = np.array(transitions)
    index_words = []
    for word in data:
      index_words.append(self.get_index(observations, word))

    N = len(transitions)
    trellis = np.zeros((N, len(data)))
    backpt = np.ones((N, len(data)), 'int32') * -1
    
    # initialization
    trellis[:, 0] = np.squeeze(pi_probs *self.obs_column(index_words[0], obs))

    # steps
    for t in range(1, len(index_words)):
      trellis[:, t] = (trellis[:, t-1, None].dot(self.obs_column(index_words[t], obs).T) *
                              transitions).max(0)
      backpt[:, t] = (np.tile(trellis[:, t-1, None], [1, N]) *
                      transitions).argmax(0)

    # termination
    tokens = [trellis[:, -1].argmax()]
    for i in range(len(data)-1, 0, -1):
      tokens.append(backpt[tokens[-1], i])

    return tokens[::-1]

  def calculate_viterbi(self, x, y, x_test):
    """
      Main method
    """
    self.observations_mtx  = self.matrix_obs(y, x)
    self.transitions_mtx = self.matrix_trans(y)
    self.pi_mtx = self.initial_probs(y)
    pi_probs = np.array(self.pi_mtx ).T
    pred_tags = []
    logging.info('Calculando Viterbi para cada observação')
    for index in range(0, len(x_test)):
      pred_tags.append(self.viterbi(x_test[index], self.transitions_mtx, self.observations_mtx.T, pi_probs))
    return pred_tags
