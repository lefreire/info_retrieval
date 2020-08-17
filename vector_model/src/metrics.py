import csv
import math
import numpy as np

class Metrics:

  def __init__(self, results_file):
    self.results_file = results_file

  def read_csv_input(self):
    """
      Reading csv input with query number and query text

      Parameters
      ----------
      file_path: string with csv path

      Returns
      -------
      content: dictionary
    """
    # logging.info('INICIANDO: leitura do arquivo csv com as resultados e resultados esperados')
    expected_results = {}
    results = {}
    with open("result/resultados_esperados.csv", newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        if int(row['QueryNumber']) in expected_results:
          expected_results[int(row['QueryNumber'])].append((int(row['DocNumber']), int(row['DocVotes'])))
        else:
          expected_results[int(row['QueryNumber'])] = [(int(row['DocNumber']), int(row['DocVotes']))]
    with open(self.results_file, newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader: 
        doc_ranking = row['RankingDoc'].replace('[', '').replace(']', '').split(",")
        ranking = int(doc_ranking [1])
        score = float(doc_ranking[2])
        if int(row['QueryNumber']) in results:
          results[int(row['QueryNumber'])].append((ranking, score))
        else:
          results[int(row['QueryNumber'])]=[(ranking, score)]  
    # logging.info('FINALIZADO: leitura do arquivo csv com as consultas')
    return expected_results, results

  def res_without_score(self, expected_res_query, res_query):
    exp_res_without_score = {}
    res_without_score = {}

    for query_number in expected_res_query:
      exp_res_without_score[query_number] = [ranking[0] for ranking in expected_res_query[query_number]]
      res_without_score[query_number] = [ranking[0] for ranking in res_query[query_number]]
    return exp_res_without_score, res_without_score

  def precision_query(self, expected_res_query, res_query):
    return len(set(res_query) & set(expected_res_query))/len(res_query)

  def precision_k(self, k, expected_results, results):
    # k primeiros relevantes/recuperados
    precision_query = {}
    for query_number in results:
      query_results = results[query_number][:k]
      # print("oi", self.precision_query(expected_results[query_number], query_results))
      # return
      precision_query[query_number] = self.precision_query(expected_results[query_number], query_results)
    return precision_query

  def precision(self, expected_results, results):
    precision_query = {}
    for query_number in results:
      precision_query[query_number] = len(set(results) & set(expected_results))/len(results)
    return precision_query

  def recall_query(self, expected_res_query, res_query):
    return len(set(res_query) & set(expected_res_query))/len(expected_res_query)

  def recall(self, expected_results, results):
    recall_query = {}
    for query_number in results:
      recall_query[query_number] = self.recall_query(expected_results[query_number], results[query_number])
    return recall_query

  def f1(self, expected_results, results):
    recall = self.recall(expected_results, results)
    precision = self.precision(expected_results, results)
    f1_query = {}
    for query_number in recall:
      if precision[query_number] == 0 and recall[query_number] == 0:
        f1_query[query_number] = 0
      else:
        f1_query[query_number] = (2*precision[query_number]*recall[query_number])/(precision[query_number]+recall[query_number])
    return f1_query

  def mean_ap(self, expected_results, results):
    avg_precision = {}
    for query_number in results:
      relevant_docs = 0
      precision_query = 0
      for doc_index in range(0, len(results[query_number])):
        if results[query_number][doc_index] in expected_results[query_number]:
          relevant_docs += 1
          precision_query += self.precision_query(expected_results[query_number], results[query_number][:doc_index+1])
      if relevant_docs == 0: avg_precision[query_number] = 0
      else: avg_precision[query_number] = precision_query/relevant_docs
    map_query = sum(avg_precision.values())/len(expected_results)
    return map_query

  def mrr(self, expected_results, results):
    rr = []
    for query_number in results:
      for doc_index in range(0, len(results[query_number])):
        if results[query_number][doc_index] in expected_results:
          rr.append(1/(doc_index+1))
          break
    return sum(rr)/len(expected_results)

  def dcg(self, expected_results, results):
    # usando pos = 10
    dcg_query = {}
    for query_number in results:
      dcg_query[query_number] = [0]
      exp_res = [ranking[0] for ranking in expected_results[query_number]]
      for doc_index in range(0, 10):
        if results[query_number][doc_index][0] in exp_res:
          rel_index = exp_res.index(results[query_number][doc_index][0])
          if doc_index == 0: dcg_query[query_number][0] += expected_results[query_number][rel_index][1]
          else: dcg_query[query_number].append(dcg_query[query_number][doc_index-1] + expected_results[query_number][rel_index][1]/np.log2(doc_index+1))
        else:
          if doc_index == 0: pass
          else: dcg_query[query_number].append(dcg_query[query_number][doc_index-1])
    return dcg_query

  def avg_dcg(self, expected_results, results):
    dcg = self.dcg(expected_results, results)
    avg_dcg = np.array([0.0]*len(dcg[list(dcg.keys())[0]]))  
    for query_number in dcg:
      avg_dcg += np.array(dcg[query_number])
    return avg_dcg/len(dcg)

  def idcg(self, expected_results, results):
    idcg_query = {}
    for query_number in results:
      score_rel_docs = []
      exp_res = [ranking[0] for ranking in expected_results[query_number]]
      for doc_index in range(0, 10):
        if results[query_number][doc_index][0] in exp_res:
          rel_index = exp_res.index(results[query_number][doc_index][0])
          score_rel_docs.append(expected_results[query_number][rel_index][1])
      score_rel_docs.sort(reverse=True) 
      if len(score_rel_docs) > 0:
        idcg_query[query_number] = score_rel_docs[0]
        for pos in range(1, len(score_rel_docs)):
          idcg_query[query_number] += score_rel_docs[pos]/np.log2(pos+1)
      else: idcg_query[query_number] = 0
    return idcg_query

  def ndcg(self, expected_results, results):
    #ndcg = dcg/idcg
    dcg = self.dcg(expected_results, results)
    idcg = self.idcg(expected_results, results)
    ndcg_query = {}
    for query_number in dcg:
      if idcg[query_number] == 0: ndcg_query[query_number] = 0
      else: ndcg_query[query_number] = dcg[query_number][-1]/idcg[query_number]
    return ndcg_query

  def r_precision(self, expected_results, results):
    prec_query = {}
    for query_number in results:
      res = results[query_number][:len(expected_results[query_number])]
      prec_query[query_number] = self.precision_query(expected_results[query_number], res)
    return prec_query

  def prec_rec(self, expected_results, results):
    r_prec_query = {}
    for query_number in results:
      recall = []
      prec = []
      for doc_index in range(0, len(results[query_number])):
        if results[query_number][doc_index] in expected_results[query_number]:
          tmp_res = results[query_number][:doc_index+1]
          recall.append(self.recall_query(expected_results[query_number], tmp_res))
          prec.append(self.precision_query(expected_results[query_number], tmp_res))
      r_prec_query[query_number] = [recall, prec]
    return r_prec_query

  def eleven_points(self, expected_results, results):
    r_prec = self.prec_rec(expected_results, results)
    points = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    points_r_p = {}
    for query_number in r_prec:
      recall = r_prec[query_number][0]
      precision = r_prec[query_number][1]
      points_r_p[query_number] = []
      recall_points = []
      precision_points = []
      if len(recall) == 0 and len(precision) == 0:
        pass
      else:
        for id in range(0, len(points)):
          if True not in (np.array(recall) >= points[id]):
            for id_continue in range(id, len(points)):
              recall_points.append(points[id_continue])
              precision_points.append(precision_points[-1]) 
            break
          else:
            index_recall = np.argwhere(np.array(recall[:]) >= points[id])  
            recall_points.append(points[id])
            precision_points.append(max(precision[index_recall.min():])) 
        points_r_p[query_number] = (recall_points,  precision_points)
    
    avg_precision_points = np.array([0.0]*11)
    recall_points = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    for query_number in points_r_p:
      if len(points_r_p[query_number]) > 0:
        avg_precision_points += np.array(points_r_p[query_number][1])
    avg_precision_points = avg_precision_points/len(points_r_p)
    final_points = {}
    for i in range(0, len(recall_points)):
      final_points[recall_points[i]] = avg_precision_points[i]
    return final_points

  def r_precision_comparison(self, file_stemmer, file_nostemmer):
    self.results_file = file_stemmer
    exp_res, res = self.read_csv_input()
    exp_res_without_score , res_without_score = self.res_without_score(exp_res, res)
    r_prec_stemmer = self.r_precision(exp_res_without_score, res_without_score)

    self.results_file = file_nostemmer
    exp_res, res = self.read_csv_input()
    exp_res_without_score , res_without_score = self.res_without_score(exp_res, res)
    r_prec_nostemmer = self.r_precision(exp_res_without_score, res_without_score)

    diff_precision = {}
    for query_number in r_prec_stemmer:
      diff_precision[query_number] = r_prec_stemmer[query_number] - r_prec_nostemmer[query_number]

    return diff_precision

  def all_metrics(self):
    exp_res, res = self.read_csv_input()
    exp_res_without_score , res_without_score = self.res_without_score(exp_res, res)

    prec5 = self.precision_k(5, exp_res_without_score, res_without_score)
    prec10 = self.precision_k(10, exp_res_without_score, res_without_score)
    f1 = self.f1(exp_res_without_score, res_without_score)
    map = self.mean_ap(exp_res_without_score, res_without_score)
    mrr = self.mrr(exp_res_without_score, res_without_score)
    dcg = self.dcg(exp_res, res)
    avg_dcg = self.avg_dcg(exp_res, res)
    ndcg = self.ndcg(exp_res, res)
    r_prec = self.r_precision(exp_res_without_score, res_without_score)
    eleven_points = self.eleven_points(exp_res_without_score, res_without_score)

    return eleven_points, f1, prec5, prec10, r_prec, map, mrr, dcg, avg_dcg, ndcg 

  
