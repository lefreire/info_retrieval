import configparser
import csv
import json
import logging
from nltk.tokenize import RegexpTokenizer


class QueriesSearch:

	def __init__(self):
		logging.basicConfig(level=logging.INFO)

	def read_file(self):
		logging.info('Lendo arquivo de configuração')
		config = configparser.ConfigParser()
		config.read('config/BUSCA.CFG')
		config.sections()
		return config['INPUT']['MODELO'], config['INPUT']['CONSULTAS'], config['OUTPUT']['RESULTADOS']

	def read_csv_input(self, file_path):
		content = {}
		# tokenizer = RegexpTokenizer(r'\w+')
		with open(file_path, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				# content_row = tokenizer.tokenize(row['QueryText'].upper())
				content[int(row['QueryNumber'])]=row['QueryText']
		return content

	def read_model_input(self, file_path):
		f = open(file_path,) 
		data = json.load(f) 
		return data

	def calculate_doc_weight(self, content, query):
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
		res = {}
		docs_weight, docs_weight_power2 = self.calculate_doc_weight(content, query)
		for doc in docs_weight.keys():
			if docs_weight[doc] > 0:
				res[doc] = docs_weight[doc]/(docs_weight_power2[doc]*len(query))
		return sorted(res.items(), key=lambda x: x[1])

	def calculare_vector_model(self, content, queries):
		res = {}
		for query_number in queries.keys():
			res[query_number] = self.calculate_query_vector_model(content, queries[query_number])[:10]
		return res

	def write_results(self, content, output_path):
		with open(output_path, 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=['QueryNumber', 'RankingDoc'])
			writer.writeheader()
			for key in content.keys():
				for index in range(0, len(content[key])):
					writer.writerow({'QueryNumber': key, 'RankingDoc': [index+1, content[key][index][0], content[key][index][1]]})

	def queries_searcher(self):
		model_path, queries_path, output_path = self.read_file()
		content = self.read_model_input(model_path)
		queries = self.read_csv_input(queries_path)
		res = self.calculare_vector_model(content, queries)
		self.write_results(res, output_path)
