from queries_search import QueriesSearch
from indexer import Indexer
from list_generator import ListGenerator
from query_processor import QueryProcessor

qs = QueriesSearch()
ind = Indexer()
lg = ListGenerator()
qp = QueryProcessor()

qp.generate_files()
lg.generate_list()
ind.index_tf_idf()
qs.queries_searcher()