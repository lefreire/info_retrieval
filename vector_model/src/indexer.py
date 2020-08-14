import configparser
import csv
import json
import logging
import numpy as np


class Indexer:

	def __init__(self):
		"""
			Constructor
		"""
		logging.basicConfig(level=logging.INFO)
		logging.info('INICIANDO: MÓDULO INDEXADOR')

	def read_config_file_index(self):
		"""
			Reading configuration file

			Returns
			-------
			path_input_file: string
			path_output_file: string
		"""
		logging.info('INICIANDO: leitura do arquivo de configuração INDEX.CFG')
		config = configparser.ConfigParser()
		config.read('config/index.cfg')
		config.sections()
		logging.info('FINALIZADO: leitura do arquivo de configuração INDEX.CFG')
		return config['INPUT']['LEIA'], config['OUTPUT']['ESCREVA']

	def calculate_tf_term(self, content):
		"""	
			Calculating tf to each term

			Parameters
			----------
			content: dictionary with keys = words in the documents

			Returns
			------
			tf_dict: dictionary with tf to each word in each document
		"""
		logging.info('INICIANDO: Cálculo de tf dos termos')
		tf_dict = {}
		count_words = 1
		for word in content.keys():
			if count_words%1000 == 0:
				logging.info('Calculando tf de termo '+str(count_words)+'/'+str(len(content)))
			if len(word) >= 2 and word.isalpha():
				tf_dict[word] = {}
				docs_in = set(content[word])
				for doc in docs_in:
					if content[word].count(doc) > 0: 
						tf_dict[word][doc] = 1+np.log2(content[word].count(doc))
					else: 
						tf_dict[word][doc] = 0
			count_words += 1
		logging.info('FINALIZADO: Cálculo de tf dos termos')
		return tf_dict

	def calculate_num_docs(self, content):
		"""
			Calcuting number of documents in the collection

			Parameters
			----------
			content: dictionary with keys = words in the documents and, in each key,
						a list with documents where the key appears

			Returns
			------
			number_documents: int
		"""
		docs = []
		for i in content.keys():
			docs.extend(content[i])
		docs_int = []
		for i in docs:
			docs_int.append(int(i))
		return len(set(docs_int))

	def calculate_idf_term(self, content):
		"""	
			Calculating idf to each term

			Parameters
			----------
			content: dictionary with keys = words in the documents

			Returns
			------
			tf_dict: dictionary with idf to each word
		"""
		logging.info('INICIANDO: Cálculo de idf dos termos')
		num_docs = self.calculate_num_docs(content)
		idf_dict = {}
		count_words = 1
		for word in content.keys():
			if count_words%1000 == 0:
				logging.info('Calculando idf de termo '+str(count_words)+'/'+str(len(content)))
			if len(word) >= 2 and word.isalpha():
				docs_in = set(content[word])
				idf_dict[word] = np.log2(num_docs/len(docs_in))
			count_words += 1
		logging.info('FINALIZADO: Cálculo de idf dos termos')
		return idf_dict

	def calculate_tf_idf(self, tf, idf):
		"""
			Calculating tf-idf to each term

			Parameters
			----------
			tf: dictionary
			idf: dictionary

			Returns
			-------
			tf_idf_dict: dictionary
		"""
		logging.info('INICIANDO: Cálculo de tf-idf dos termos')
		tf_idf_dict = {}
		count_words = 1
		for word in tf:
			if count_words%1000 == 0:
				logging.info('Calculando idf de termo '+str(count_words)+'/'+str(len(tf)))
			tf_idf_dict[word] = {}
			for doc in tf[word]:
				tf_idf_dict[word][doc] = tf[word][doc]*idf[word]
			count_words += 1
		logging.info('FINALIZADO: Cálculo de tf-idf dos termos')
		return tf_idf_dict

	def read_csv_input(self, file_path):
		"""
			Reading csv file with words and documents where each word appears

			Parameters
			----------
			file_path: string with csv file path

			Returns
			-------
			content: dictionary
		"""
		logging.info('INICIANDO: Leitura de arquivo csv com palavras e documentos onde aparece cada palavra')
		content = {}
		with open(file_path, newline='') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				content[row['WORD']] =json.loads(row['DOCS'])
		logging.info('FINALIZADO: Leitura de arquivo csv com palavras e documentos onde aparece cada palavra')
		return content

	def write_output_file(self, file_path, content):
		"""
			Writing a json file with the tf-idf correspondent to each term and document

			Parameters
			----------
			content: dictionary

			Returns
			-------
			json_file
		"""
		logging.info('INICIANDO: Escrita de arquivo json com tf-idf')
		with open(file_path, 'w') as f:
			json.dump(content, f)
		logging.info('FINALIZADO: Escrita de arquivo json com tf-idf')

	def index_tf_idf(self):
		"""
			Main method
		"""
		input_path, output_path = self.read_config_file_index()
		content = self.read_csv_input(input_path)
		idf = self.calculate_idf_term(content)
		tf = self.calculate_tf_term(content)
		res = self.calculate_tf_idf(tf, idf)
		self.write_output_file(output_path, res)
		return content, idf, tf, res
		logging.info('FINALIZADO: MÓDULO INDEXADOR')

