import csv


def result_file(content, field_names, file_name):
  with open("avalia/"+file_name, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    for query_number in content:
      # logging.info('Escrevendo resultados da consulta '+str(count_queries)+'/'+str(len(content)))
      writer.writerow({field_names[0]: query_number, field_names[1]: content[query_number]})


def to_markdown(query_number, item):
  return str(query_number) + " | " + str(item)+"\n"

def all_results_markdown(results):
  result_mark = []
  for query_number in results:
    result_mark.append(to_markdown(query_number, results[query_number]))
  return result_mark

def append_markdown(mark_tmp, result):
  result = all_results_markdown(result)
  for res in result:
    mark_tmp += res
  return mark_tmp

def calculate_mean(result):
  mean_res = 0
  for query_number in result:
    mean_res += result[query_number]
  return mean_res/len(result)

def calculate_dcg_mean(result):
  mean_res = 0
  for query_number in result:
    mean_res += result[query_number][-1]
  return mean_res/len(result)

def report(points_s, f1_s, prec5_s, prec10_s, r_prec_s, map_s, mrr_s, dcg_s, ndcg_s,
           points_ns, f1_ns, prec5_ns, prec10_ns, r_prec_ns, map_ns, mrr_ns, dcg_ns, ndcg_ns, diff_precision):
  
  text_md = '''
  # Report
  ## Using stemmer
  ### 11-points interpolated average precision
  | Recall | Precision | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, points_s)
  text_md += '''
  ![11points_stemmer](src/avalia/11pontos-stemmer-1.png)
  '''

  text_md += '''
  ### F1
  | Query Number | F1 | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, f1_s)
  text_md += '''
  \n**F1 average**: 
  '''
  text_md += str(calculate_mean(f1_s)) + '\n'
  text_md += '''
  ![f1_stemmer](src/avalia/f1-stemmer-3.png)
  '''

  text_md += '''
  \n ### Precision@5
  | Query Number | Precision@5 | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, prec5_s)
  text_md += '''
  \n**Precision@5 average**: 
  '''
  text_md += str(calculate_mean(prec5_s)) + '\n'
  text_md += '''
  ![prec5_stemmer](src/avalia/precision5-stemmer-5.png)
  '''

  text_md += '''
  \n ### Precision@10
  | Query Number | Precision@10 | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, prec10_s)
  text_md += '''
  \n**Precision@10 average**: 
  '''
  text_md += str(calculate_mean(prec10_s)) + '\n'
  text_md += '''
  ![prec10_stemmer](src/avalia/precision10-stemmer-7.png)
  '''

  text_md += '''
  \n ### R-Precision
  | Query Number | R-Precision | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, r_prec_s)
  text_md += '''
  \n**R-Precision average**: 
  '''
  text_md += str(calculate_mean(r_prec_s)) + '\n'

  text_md += '''
  \n ### MAP

  '''
  text_md += str(map_s)+'\n'

  text_md += '''
  \n ### MRR

  '''
  text_md += str(mrr_s)+'\n'

  text_md += '''
  \n ### DCG
  | Query Number | DCG | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, dcg_s)
  text_md += '''
  \n**DCG average@10**: 
  '''
  text_md += str(calculate_dcg_mean(dcg_s)) + '\n'
  text_md += '''
  ![dcg_stemmer](src/avalia/avgdcg-stemmer-10.png)
  '''

  text_md += '''
  \n ### nDCG
  | Query Number | nDCG | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, ndcg_s)
  text_md += '''
  \n**nDCG average**: 
  '''
  text_md += str(calculate_mean(ndcg_s)) + '\n'
  text_md += '''
  ![ndcg_stemmer](src/avalia/ndcg-stemmer-12.png)
  '''

  text_md += '''
  ## Without stemmer
  ### 11-points interpolated average precision
  | Recall | Precision | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, points_ns)
  text_md += '''
  ![11points_stemmer](src/avalia/11pontos-nostemmer-2.png)
  '''

  text_md += '''
  ### F1
  | Query Number | F1 | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, f1_ns)
  text_md += '''
  \n**F1 average**: 
  '''
  text_md += str(calculate_mean(f1_ns)) + '\n'
  text_md += '''
  ![f1_nostemmer](src/avalia/f1-nostemmer-4.png)
  '''

  text_md += '''
  \n ### Precision@5
  | Query Number | Precision@5 | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, prec5_ns)
  text_md += '''
  \n**Precision@5 average**: 
  '''
  text_md += str(calculate_mean(prec5_ns)) + '\n'
  text_md += '''
  ![prec5_nostemmer](src/avalia/precision5-nostemmer-6.png)
  '''

  text_md += '''
  \n ### Precision@10
  | Query Number | Precision@10 | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, prec10_ns)
  text_md += '''
  \n**Precision@10 average**: 
  '''
  text_md += str(calculate_mean(prec10_ns)) + '\n'
  text_md += '''
  ![prec10_nostemmer](src/avalia/precision10-nostemmer-8.png)
  '''

  text_md += '''
  \n ### R-Precision
  | Query Number | R-Precision | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, r_prec_ns)
  text_md += '''
  \n**R-Precision average**: 
  '''
  text_md += str(calculate_mean(r_prec_ns)) + '\n'

  text_md += '''
  \n ### MAP

  '''
  text_md += str(map_ns)+'\n'

  text_md += '''
  \n ### MRR

  '''
  text_md += str(mrr_ns)+'\n'

  text_md += '''
  \n ### DCG
  | Query Number | DCG | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, dcg_ns)
  text_md += '''
  \n**DCG average@10**: 
  '''
  text_md += str(calculate_dcg_mean(dcg_ns)) + '\n'
  text_md += '''
  ![dcg_nostemmer](src/avalia/avgdcg-nostemmer-11.png)
  '''

  text_md += '''
  \n ### nDCG
  | Query Number | nDCG | 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, ndcg_ns)
  text_md += '''
  \n**nDCG average**: 
  '''
  text_md += str(calculate_mean(ndcg_ns)) + '\n'
  text_md += '''
  ![ndcg_nostemmer](src/avalia/ndcg-nostemmer-13.png)
  '''

  text_md += '''
  \n ### R-Precision comparation
  | Query Number | R-Precision_stemmer -   R-Precision_nostemmer| 
  ------------ | -------------
  '''
  text_md = append_markdown(text_md, diff_precision)
  text_md += '''
  ![r_prec](src/avalia/r-precision-comparison-9.png)
  '''
  md_file = "../relatorio.md"
  with open(md_file, 'w+') as f:
      f.write(text_md)

  f.close()


  
				
