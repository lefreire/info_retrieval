class Decoder:

  def __init__(self):
    """
      Constructor
    """
    pass

  def return_tag_tokens(self, tags_indexes, observations):
    """
        Getting index and returning the correspondent tag

        Parameters
        ----------
        tag_indexes: list of string
        observations: pandas.DataFrame

        Returns
        -------
        tag_pred: list of string
    """
    tag_pred = []
    for tag_index in tags_indexes:
      tag_pred.append(observations.T.index[tag_index])
    return tag_pred

  def decode_tags(self, y_pred, observations):
    """
        Main method
    """
    tag_pred = []
    for y in y_pred:
      tag_pred.append(self.return_tag_tokens(y, observations))
    return tag_pred