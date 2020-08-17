import logging
import matplotlib.pyplot as plt


class Diagram:

  def __init__(self):
    """
      Constructor
    """
    logging.basicConfig(level=logging.INFO)
    logging.info('INICIANDO: MÓDULO DIAGRAMAS')

  def diagram_eleven_points(self, points, file_name):
    """
      Diagram to eleven points Interpolated Average Precision

      Parameters
      ----------
      points: dictionary
      file_name: path to save the diagram

      Returns
      -------
      diagram: figure
    """ 
    logging.info('INICIANDO: construção do diagrama de 11 pontos de precisão e recall')
    avg_precision_points = []
    recall_points = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for point in points:
        avg_precision_points.append(points[point])
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(recall_points, avg_precision_points, 'C0o', color='red')
    ax.step(recall_points, avg_precision_points, color='pink')
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("11-Points Interpolated Average Precision")
    plt.savefig("avalia/"+file_name)
    logging.info('FINALIZADO: construção do diagrama de 11 pontos de precisão e recall')

  def diagram_r_precision(self, diff_precision, file_name):
    """
      Diagram to R-precision

      Parameters
      ----------
      diff_precision: dictionary
      file_name: path to save the diagram

      Returns
      -------
      diagram: figure
    """ 
    logging.info('INICIANDO: construção do diagrama de R-precision')
    query_numbers = []
    r_prec_array = []
    for query_number in diff_precision:
      r_prec_array.append(diff_precision[query_number])
      query_numbers.append(query_number)
    plt.figure(figsize=(12,8))
    plt.bar(query_numbers, r_prec_array)
    plt.xlabel("Query Number")
    plt.ylabel("R-Precision Stemmer/Nostemmer")
    plt.title("R-Precision comparation (stemmer and nostemmer)")
    plt.savefig("avalia/"+file_name)
    logging.info('FINALIZADO: construção do diagrama de R-precision')
  
  def diagram_avg_dcg(self, avg_dcg, file_name):
    """
      Diagram to avg DCG

      Parameters
      ----------
      avg_dcg: array
      file_name: path to save the diagram

      Returns
      -------
      diagram: figure
    """ 
    logging.info('INICIANDO: construção do diagrama de DCG médio')
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(avg_dcg, '--bo', color='green')
    plt.xlabel("Number of documents")
    plt.ylabel("Average DCG")
    plt.title("Average DCG with rank=10")
    plt.savefig("avalia/"+file_name)
    logging.info('FINALIZADO: construção do diagrama de DCG médio')

  def diagram_ndcg(self, ndcg, file_name):
    """
      Diagram to nDCG

      Parameters
      ----------
      ndcg: dictionary
      file_name: path to save the diagram

      Returns
      -------
      diagram: figure
    """ 
    logging.info('INICIANDO: construção do diagrama de nDCG')
    query_numbers = []
    ndcg_array = []
    for query_number in ndcg:
      ndcg_array.append(ndcg[query_number])
      query_numbers.append(query_number)
    fig, ax = plt.subplots(figsize=(12,8))
    plt.bar(query_numbers, ndcg_array, color='pink')
    plt.xlabel("Query number")
    plt.ylabel("nDCG")
    plt.title("nDCG with rank=10")
    plt.savefig("avalia/"+file_name)
    logging.info('FINALIZADO: construção do diagrama de nDCG')

  def diagram_f1(self, f1, file_name):
    """
      Diagram to F1

      Parameters
      ----------
      f1: dictionary
      file_name: path to save the diagram

      Returns
      -------
      diagram: figure
    """ 
    logging.info('INICIANDO: construção do diagrama da métrica F1')
    query_numbers = []
    f1_array = []
    for query_number in f1:
      f1_array.append(f1[query_number])
      query_numbers.append(query_number)
    fig, ax = plt.subplots(figsize=(12,8))
    plt.bar(query_numbers, f1_array)
    plt.xlabel("Query number")
    plt.ylabel("F1")
    plt.title("F1 metric")
    plt.savefig("avalia/"+file_name)
    logging.info('FINALIZADO: construção do diagrama da métrica F1')

  def diagram_precision(self, precision, k, file_name):
    """
      Diagram to Precision@k

      Parameters
      ----------
      precision: dictionary
      k: int
      file_name: path to save the diagram

      Returns
      -------
      diagram: figure
    """ 
    logging.info('INICIANDO: construção do diagrama de Precision@'+str(k))
    query_numbers = []
    precision_array = []
    for query_number in precision:
      precision_array.append(precision[query_number])
      query_numbers.append(query_number)
    fig, ax = plt.subplots(figsize=(12,8))
    plt.bar(query_numbers, precision_array)
    plt.xlabel("Query number")
    plt.ylabel("Precision")
    plt.title("Precision@"+str(k)+" metric")
    plt.savefig("avalia/"+file_name)
    logging.info('FINALIZADO: construção do diagrama de Precision@'+str(k))
    
