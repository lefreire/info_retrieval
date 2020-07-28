import configparser
import csv
import json
import logging
import numpy as np


class Indexer:

	def __init__(self):
		logging.basicConfig(level=logging.INFO)

	def read_config_file_index(self):
		logging.info('Lendo arquivo de configuração')
		config = configparser.ConfigParser()
		config.read('INDEX.CFG')
		config.sections()
		return config['INPUT']['LEIA'], config['OUTPUT']['ESCREVA']

	def calculate_tf_term(self, content):
		tf_dict = {}
		for word in content.keys():
			if len(word) > 2 and word.isalpha():
				tf_dict[word] = {}
				docs_in = set(content[word])
				for doc in docs_in:
					if content[word].count(doc) > 0: tf_dict[word][doc] = 1+np.log2(content[word].count(doc))
					else: tf_dict[word][doc] = 0
		return tf_dict

	def calculate_num_docs(self, content):
		docs = []
		for i in content.keys():
			docs.extend(content[i])
		docs_int = []
		for i in docs:
			docs_int.append(int(i))
		return len(set(docs_int))

	def calculate_idf_term(self, content):
		num_docs = self.calculate_num_docs(content)
		idf_dict = {}
		for word in content.keys():
			if len(word) > 2 and word.isalpha():
				docs_in = set(content[word])
				idf_dict[word] = np.log2(num_docs/len(docs_in))
		return idf_dict

	def calculate_tf_idf(self, tf, idf):
		tf_idf_dict = {}
		for word in tf:
			tf_idf_dict[word] = {}
			for doc in tf[word]:
				tf_idf_dict[word][doc] = tf[word][doc]*idf[word]
		return tf_idf_dict

	def read_csv_input(self, file_path):
		content = {}
		with open(file_path, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				content[row['WORD']] =json.loads(row['DOCS'])
		return content

	def write_output_file(self, file_path, content):
		with open(file_path, 'w') as f:
			json.dump(content, f)

	def index_tf_idf(self):
		input_path, output_path = self.read_config_file_index()
		content = self.read_csv_input(input_path)
		idf = self.calculate_idf_term(content)
		tf = self.calculate_tf_term(content)
		res = self.calculate_tf_idf(tf, idf)
		self.write_output_file(output_path, res)
