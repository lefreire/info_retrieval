import configparser
import csv
import json
import logging
from nltk.tokenize import RegexpTokenizer
import time


class QueriesSearch:

	def __init__(self):
		"""
			Constructor
		"""
		logging.basicConfig(level=logging.INFO)
		logging.info('INICIANDO: MÓDULO BUSCADOR')

	def read_file(self):
		"""
			Reading configuration file

			Returns
			-------
			path_model_file: string
			path_queries_file: string
			path_results_file: string
		"""
		logging.info('INICIANDO: leitura do arquivo de configuração BUSCA.CFG')
		config = configparser.ConfigParser()
		config.read('config/BUSCA.CFG')
		config.sections()
		logging.info('FINALIZADO: leitura do arquivo de configuração BUSCA.CFG')
		return config['INPUT']['MODELO'], config['INPUT']['CONSULTAS'], config['OUTPUT']['RESULTADOS']

	def read_csv_input(self, file_path):
		"""
			Reading csv input with query number and query text

			Parameters
			----------
			file_path: string with csv path

			Returns
			-------
			content: dictionary
		"""
		logging.info('INICIANDO: leitura do arquivo csv com as consultas')
		content = {}
		with open(file_path, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				content[int(row['QueryNumber'])]=row['QueryText']
		logging.info('FINALIZADO: leitura do arquivo csv com as consultas')
		return content

	def read_model_input(self, file_path):
		"""
			Reading model 

			Parameters
			----------
			file_path: string with json file path

			Returns
			-------
			data: dictionary
		"""
		logging.info('INICIANDO: leitura do arquivo json com o modelo')
		f = open(file_path,) 
		data = json.load(f)
		logging.info('FINALIZADO: leitura do arquivo json com o modelo') 
		return data

	def calculate_doc_weight(self, content, query):
		"""
			Calculating similarity terms between documents and query

			Parameters
			----------
			content: dictionary
			query: list of strings

			Returns
			-------
			docs: dictionary
			docs_power2: dictionary
		"""
		#peso da consulta = 1
		docs = {}
		docs_power2 = {}
		for key in content.keys():
			for doc in content[key]:
				docs[doc] = docs_power2[doc] = 0
		for word in content.keys():
			if word in query:
				for doc in content[word]:
					docs[doc] += content[word][doc]
					docs_power2[doc] += content[word][doc]**2
		return docs, docs_power2

	def calculate_query_vector_model(self, content, query):
		"""
			Calculating similarity between documents and query

			Parameters
			----------
			content: dictionary
			query: list of strings
			
			Returns
			-------
			res: dictionary
		"""
		res = {}
		docs_weight, docs_weight_power2 = self.calculate_doc_weight(content, query)
		for doc in docs_weight.keys():
			if docs_weight[doc] > 0:
				res[doc] = docs_weight[doc]/(docs_weight_power2[doc]*len(query))
		return sorted(res.items(), key=lambda x: x[1], reverse=True)

	def calculare_vector_model(self, content, queries):
		"""
			Calculating vector model to all queries

			Parameters
			----------
			content: dictionary
			queries: list

			Returns
			-------
			res: dictionary
		"""
		logging.info('INICIANDO: cálculo de similaridade entre as consultas e os documentos')
		res = {}
		start_time = time.time()
		for query_number in queries.keys():
			res[query_number] = self.calculate_query_vector_model(content, queries[query_number])[:10]
		logging.info('FINALIZADO: cálculo de similaridade entre as consultas e os documentos em '+str(time.time()-start_time))
		return res

	def write_results(self, content, output_path):
		"""
			Writing results in a csv file
			Each row in csv file has query number, retrieved document and 
			their position in the ranking 

			Parameters
			----------
			content: dictionary
			output_path: string with csv file path

			Returns
			-------
			csv_file
		"""
		logging.info('INICIANDO: escrita dos resultados no arquivo csv')
		count_queries = 1
		with open(output_path, 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=['QueryNumber', 'RankingDoc'])
			writer.writeheader()
			for key in content.keys():
				logging.info('Escrevendo resultados da consulta '+str(count_queries)+'/'+str(len(content)))
				for index in range(0, len(content[key])):
					writer.writerow({'QueryNumber': key, 'RankingDoc': [index+1, content[key][index][0], content[key][index][1]]})
				count_queries += 1
		logging.info('FINALIZADO: escrita dos resultados no arquivo csv')

	def queries_searcher(self):
		"""
			Main method
		"""
		model_path, queries_path, output_path = self.read_file()
		content = self.read_model_input(model_path)
		queries = self.read_csv_input(queries_path)
		res = self.calculare_vector_model(content, queries)
		self.write_results(res, output_path)
		logging.info('FINALIZADO: MÓDULO BUSCADOR')

