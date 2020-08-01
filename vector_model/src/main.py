import logging
logging.basicConfig(level=logging.INFO)
from indexer import Indexer
from list_generator import ListGenerator
from queries_search import QueriesSearch
from query_processor import QueryProcessor


query_process = QueryProcessor()
list_gen = ListGenerator()
index = Indexer()
query_search = QueriesSearch()

logging.info('INICIANDO: BUSCA E RECUPERAÇÃO DE DOCUMENTOS')
query_process.generate_files()
list_gen.generate_list()
index.index_tf_idf()
query_search.queries_searcher()
logging.info('FINALIZADO: BUSCA E RECUPERAÇÃO DE DOCUMENTOS')