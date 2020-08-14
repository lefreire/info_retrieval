from nltk.stem import PorterStemmer


class StemmingWords:

  def __init__(self):
    self.porter = PorterStemmer()

  def stemming_tokens(self, tokens):
    tokens = tokens.split(" ")
    stemming_tokens = []
    for token in tokens:
      stemming_tokens.append(self.porter.stem(token).upper())
    return " ".join(stemming_tokens)