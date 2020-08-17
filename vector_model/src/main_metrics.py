import logging
logging.basicConfig(level=logging.INFO)
from diagram import Diagram
from metrics import Metrics
from results_file import *


logging.info('INICIANDO: CÁLCULO DAS MÉTRICAS E CONSTRUÇÃO DOS DIAGRAMAS E RELATÓRIO')
metrics = Metrics("result/resultados_stemmer.csv")
eleven_points, f1, prec5, prec10, r_prec, mean_ap, mrr, dcg, avg_dcg, ndcg  = metrics.all_metrics()

metrics = Metrics("result/resultados_nostemmer.csv")
eleven_points_no, f1_no, prec5_no, prec10_no, r_prec_no, mean_ap_no, mrr_no, dcg_no, avg_dcg_no, ndcg_no  = metrics.all_metrics()
diff_precision = metrics.r_precision_comparison("result/resultados_stemmer.csv", "result/resultados_nostemmer.csv")

diag = Diagram()
#11 points stemmer
diag.diagram_eleven_points(eleven_points, "11pontos-stemmer-1.png")
result_file(eleven_points, ['Recall', 'Precision'], "11pontos-stemmer-1.csv")
#11 points without stemmer
diag.diagram_eleven_points(eleven_points_no, "11pontos-nostemmer-2.png")
result_file(eleven_points_no, ['Recall', 'Precision'], "11pontos-nostemmer-2.csv")

#f1 stemmer
diag.diagram_f1(f1, "f1-stemmer-3.png")
result_file(f1, ['QueryNumber', 'F1'], "f1-stemmer-3.csv")
#f1 nostemmer
diag.diagram_f1(f1_no, "f1-nostemmer-4.png")
result_file(f1_no, ['QueryNumber', 'F1'], "f1-nostemmer-4.csv")

#precision5 stemmer
diag.diagram_precision(prec5_no, 5, "precision5-stemmer-5.png")
result_file(prec5_no, ['QueryNumber', 'Precision@5'], "precision5-stemmer-5.csv")
#precision5 nostemmer
diag.diagram_precision(prec5_no, 5, "precision5-nostemmer-6.png")
result_file(prec5_no, ['QueryNumber', 'Precision@5'], "precision5-nostemmer-6.csv")

#precision5 stemmer
diag.diagram_precision(prec10_no, 10, "precision10-stemmer-7.png")
result_file(prec10_no, ['QueryNumber', 'Precision@10'], "precision10-stemmer-7.csv")
#precision5 nostemmer
diag.diagram_precision(prec10_no, 10, "precision10-nostemmer-8.png")
result_file(prec10_no, ['QueryNumber', 'Precision@10'], "precision10-nostemmer-8.csv")

#r precision - diff between stemmer and no stemmer
diag.diagram_r_precision(diff_precision, "r-precision-comparison-9.png")
result_file(diff_precision, ['QueryNumber', 'Stemmer/Nostemmer'], "r-precision-comparison-9.csv")

#avg dcg stemmer
diag.diagram_avg_dcg(avg_dcg, "avgdcg-stemmer-10.png")
result_file(dcg, ['QueryNumber', 'DCG'], "dcg-stemmer-10.csv")
#avg dcg nostemmer
diag.diagram_avg_dcg(avg_dcg_no, "avgdcg-nostemmer-11.png")
result_file(dcg_no, ['QueryNumber', 'DCG'], "dcg-nostemmer-11.csv")

#avg ndcg stemmer
diag.diagram_ndcg(ndcg, "ndcg-stemmer-12.png")
result_file(ndcg, ['QueryNumber', 'nDCG'], "ndcg-stemmer-12.csv")
#avg ndcg nostemmer
diag.diagram_ndcg(ndcg_no, "ndcg-nostemmer-13.png")
result_file(ndcg_no, ['QueryNumber', 'nDCG'], "ndcg-nostemmer-13.csv")

report(eleven_points, f1, prec5, prec10, r_prec, mean_ap, mrr, dcg, ndcg, eleven_points_no, f1_no, prec5_no, prec10_no, r_prec_no, mean_ap_no, mrr_no, dcg_no, ndcg_no, diff_precision)
logging.info('FINALIZADO: CÁLCULO DAS MÉTRICAS E CONSTRUÇÃO DOS DIAGRAMAS E RELATÓRIO')

