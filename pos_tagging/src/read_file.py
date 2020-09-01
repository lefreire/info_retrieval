import logging
import numpy as np
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split


class ReadWriteFile:

  def __init__(self):
    """
      Constructor
    """
    logging.basicConfig(level=logging.INFO)

  def read_file(self, file_path):
    """
      Reading file in file_path

      Parameters
      ----------
      file_path: string

      Returns
      -------
      sentences: list of string
    """ 
    logging.info('Lendo arquivo de {0}'.format(file_path))
    file_with_tags = open(file_path, "r", encoding='utf-8')
    return file_with_tags.readlines()

  def split_corpus_tags(self, corpus):
    """
      Reading file in file_path

      Parameters
      ----------
      file_path: string

      Returns
      -------
      sentences: list of string
    """
    logging.info('Dividindo texto das tags')
    sentences = []
    tags = []
    dict_tags = {}
    for sentence in corpus:
      sentence_tmp = sentence.replace("\n", '')
      words_tmp = []
      tags_tmp = []
      words = sentence_tmp.split(" ")
      for word in words:
        tag_word = word.split("_")
        if tag_word[0] == "": pass
        else:
          words_tmp.append(tag_word[0])
          tags_tmp.append(tag_word[1])
          if not tag_word[1] in dict_tags.keys(): 
            dict_tags[tag_word[1]] = {}
            dict_tags[tag_word[1]]['right'] = 0
            dict_tags[tag_word[1]]['pred'] = 0
            dict_tags[tag_word[1]]['pres'] = 1
          else: dict_tags[tag_word[1]]['pres'] += 1
      sentences.append(words_tmp)
      tags.append(tags_tmp)
    return sentences, tags, dict_tags

  def divide_train_test(self, sentences, tags):
    """
      Splitting sentences and tags in train and test

      Parameters
      ----------
      sentences: list of lists
      tags: list of lists

      Returns
      -------
      train: list with indexes
      test: list with indexes
    """
    logging.info('Dividindo dataset em 10 folds')
    kf = KFold(n_splits=10)
    train, test = [], []
    for train_index, test_index in kf.split(sentences):
      train.append(train_index)
      test.append(test_index)
    return train, test

  def write_file(self, file_path, acc, dict_tags):
    """
      Writing file with accuracy and informations about the tags

      Parameters
      ----------
      file_path: string
      acc: list with floats
      dict_tags: dictionary

      Returns
      -------
      file: file in file_path
    """
    logging.info('Escrevendo arquivo em {0}'.format(file_path))
    file_write = open(file_path, "w")
    file_write.write("Taxa de acerto geral: {0:.2f}%\n".format(np.mean(acc)*100))
    for key in dict_tags.keys():
      if dict_tags[key]['right'] > 0:
        file_write.write("Taxas de acerto para a classe '{0}': {1:.2f}% Total da classe '{0}': {2:.2f}%\n".format(key, 
                                                                                                    (dict_tags[key]['pred']/dict_tags[key]['right'])*100, 
                                                                                                    (dict_tags[key]['right']/dict_tags[key]['pres'])*100))
      else:
        file_write.write("Taxas de acerto para a classe '{0}': Nao presente no corpus de teste\n".format(key))

    file_write.close()

  def read_and_split(self, file_path):
    """
        Main method
    """
    corpus = self.read_file(file_path)
    sentences, tags, dict_tags = self.split_corpus_tags(corpus)
    train, test = self.divide_train_test(sentences, tags)
    sentences_train, sentences_test, tags_train, tags_test = [], [], [], []
    for train_index, test_index in zip(train, test):
      sentences_train.append(np.array(sentences)[train_index])
      sentences_test.append(np.array(sentences)[test_index])
      tags_train.append(np.array(tags)[train_index])
      tags_test.append(np.array(tags)[test_index])
    return dict_tags, sentences_train, tags_train, sentences_test, tags_test

