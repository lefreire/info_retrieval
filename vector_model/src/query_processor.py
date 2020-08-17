import configparser
import csv
import logging
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import xml.dom.minidom
from xml.dom.minidom import parse
from stemmer import StemmingWords


class QueryProcessor:

	def __init__(self):
		"""
			Constructor
		"""
		logging.basicConfig(level=logging.INFO)
		logging.info('INICIANDO: MÓDULO PROCESSADOR DE CONSULTAS')

	def read_config_file(self):
		"""
			Reading configuration file

			Returns
			-------
			path_input_file: string
			path_queries_file: string
			path_expected_file: string
		"""
		logging.info('INICIANDO: leitura do arquivo de configuração PC.CFG')
		config = configparser.ConfigParser()
		config.read('config/pc.cfg')
		config.sections()
		logging.info('FINALIZADO: leitura de arquivo de configuração PC.CFG')
		return config.has_section('STEMMER'), config['INPUT']['LEIA'], config['OUTPUT']['CONSULTAS'], config['OUTPUT']['ESPERADOS']

	def tokenize_query(self, query_text):
		"""
			Gets a text and remove unwanted characters and stopwords

			Parameters
			----------
			query_text: string

			Returns
			-------
			tokenized_query: string
		"""
		tokenizer = RegexpTokenizer(r'\w+')
		stop_words = set(stopwords.words('english')) 
		abstract = tokenizer.tokenize(query_text.upper()) 
		final_sentence = [w for w in abstract if not w.lower() in stop_words]
		return " ".join(final_sentence).upper()

	def define_score(self, votes_string):
		"""
			Defining score according votes

			Parameters
			----------
			votes_string: string with 4 chars

			Returns
			-------
			score: integer, calculated according to votes, using weights:
				2: REW (one of the authors)
				1: faculty colleagues of REW
				1: post-doctorate associate of REW
				2: JBW (other author and a medical bibliographer). 
				and added up at the end
		"""
		#2*REW + colleagues + post-doctorate associate + 2* JBW
		votes = [int(x) for x in votes_string] 
		weights = [2,1,1,2]
		score = 0
		for i in range(0, 4):
			if votes[i] >= 0 and votes[i] <= 2:
				score += votes[i]*weights[i]
		return score

	def read_xml(self, xml_name):
		"""
			Reading xml file and getting content from 
			QueryNumber, QueryText, Results and Records tags

			Parameters
			----------
			xml_name: path to xml

			Returns
			-------
			content: dictionary with keys QueryNumber, QueryText, Results and Records
		"""
		logging.info('INICIANDO: leitura do arquivo xml de consultas')
		doc = xml.dom.minidom.parse(xml_name)
		query_number = doc.getElementsByTagName("QueryNumber")
		query_text = doc.getElementsByTagName("QueryText")
		results = doc.getElementsByTagName("Results")
		records = doc.getElementsByTagName("Records")
		content = {'QueryNumber':[], 'QueryText':[], 'Results':[], 'Records':[]}
		for nquery in query_number: content['QueryNumber'].append(nquery.firstChild.nodeValue)
		for tquery in query_text: content['QueryText'].append(tquery.firstChild.nodeValue)
		for res in results: content['Results'].append(res.firstChild.nodeValue)
		for rec in records: 
			docs_results = []
			for item in rec.getElementsByTagName("Item"):
				score = self.define_score(item.getAttribute("score"))
				docs_results.append([int(item.firstChild.nodeValue), score])
			content['Records'].append(docs_results)
		logging.info('FINALIZADO: leitura do arquivo xml de consultas')
		return content

	def generate_query_file(self, query_file, xml_name, apply_stemmer):
		"""
			Writing xml file in the query file
			In the resulting file, it is possible to find all the queries

			Parameters
			----------
			query_file: string with file path 
			xml_name: string with file path

			Returns
			-------
			csv_file: file with headers [QueryNumber, QueryText]
		"""
		logging.info('INICIANDO: geração de arquivo de consultas')

		content = self.read_xml(xml_name)
		if apply_stemmer:
				query_file = query_file.split(".")[0] + "_stemmer." + query_file.split(".")[1]
		else:
			query_file = query_file.split(".")[0] + "_nostemmer." + query_file.split(".")[1]

		with open(query_file, 'w', newline='') as csvfile:
			fieldnames = ['QueryNumber', 'QueryText']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			for index in range(0, len(content['QueryNumber'])):
				query_text = self.tokenize_query(content['QueryText'][index])
				if apply_stemmer:
					query_text = StemmingWords().stemming_tokens(query_text)
				logging.info('Escrevendo consulta '+str(index+1)+'/'+str(len(content['QueryNumber'])))
				writer.writerow({'QueryNumber': content['QueryNumber'][index], 'QueryText': query_text})
		logging.info('FINALIZADO: geração de arquivo de consultas')

	def generate_expected_file(self, expected_file, xml_name):
		"""
			Writing xml file in the expected file
			In the resulting file, it is possible to find all retrieved documents
			for the queries

			Parameters
			----------
			expected_file: string with file path 
			xml_name: string with file path

			Returns
			-------
			csv_file: file with headers [QueryNumber, DocNumber, DocVotes]
		"""
		logging.info('Gerando arquivo de documentos esperados')
		content = self.read_xml(xml_name)

		with open(expected_file, 'w', newline='') as csvfile:
			fieldnames = ['QueryNumber', 'DocNumber', 'DocVotes']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			for index in range(0, len(content['QueryNumber'])):
				count_results = 0
				logging.info('Escrevendo documentos da consulta '+str(index+1)+'/'+str(len(content['QueryNumber'])))
				for result in content['Records'][index]:
					writer.writerow({'QueryNumber': content['QueryNumber'][index], 'DocNumber': result[0], 
									 'DocVotes': result[1]})
					count_results += 1
					if count_results == int(content['Results'][index]): break

	def generate_files(self):
		"""
			Main method
			Reads all files and generate a file with queries 
			and a file with expected documents to each query
		"""
		apply_stemmer, xml_file, query_file, expected_file = self.read_config_file()
		self.generate_query_file(query_file, xml_file, apply_stemmer)
		self.generate_expected_file(expected_file, xml_file)
		logging.info('FINALIZADO: MÓDULO PROCESSADOR DE CONSULTAS')
