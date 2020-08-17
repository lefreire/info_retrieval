import logging
from nltk.stem import PorterStemmer


class StemmingWords:

  def __init__(self):
    """
      Constructor
    """
    self.porter = PorterStemmer()
    logging.basicConfig(level=logging.INFO)
	  logging.info('INICIANDO: MÓDULO STEMMER')

  def stemming_tokens(self, tokens):
    """
      Applying Porter stemmer in the tokens

      Parameters
      ----------
      tokens: string

      Returns
      -------
      stemming_tokens: string
    """
  	logging.info('INICIANDO: uso de stemmer')
    tokens = tokens.split(" ")
    stemming_tokens = []
    for token in tokens:
      stemming_tokens.append(self.porter.stem(token).upper())
    logging.info('FINALIZADO: uso de stemmer')
    return " ".join(stemming_tokens)