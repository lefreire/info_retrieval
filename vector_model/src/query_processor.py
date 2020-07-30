import configparser
import csv
import logging
from xml.dom.minidom import parse
import xml.dom.minidom
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer, word_tokenize 

class QueryProcessor:

	def __init__(self):
		logging.basicConfig(level=logging.INFO)
		logging.info('Iniciando PROCESSADOR DE CONSULTAS')

	def read_config_file(self):
		logging.info('Lendo arquivo de configuração PC.CFG')
		config = configparser.ConfigParser()
		config.read('config/PC.CFG')
		config.sections()
		return config['INPUT']['LEIA'], config['OUTPUT']['CONSULTAS'], config['OUTPUT']['ESPERADOS']

	def tokenize_query(self, query_text):
		tokenizer = RegexpTokenizer(r'\w+')
		stop_words = set(stopwords.words('english')) 
		word_tokens = word_tokenize(query_text) 
		final_sentence = [w for w in word_tokens if not w in stop_words]
		return " ".join(tokenizer.tokenize(" ".join(final_sentence).upper()))   

	def define_score(self, votes):
		#2*REW + colleagues + post-doctorate associate + 2* JBW
		weights = [2,1,1,2]
		score = 0
		for i in range(0, 4):
			if votes[i] >= 0 and votes[i] <= 2:
				score += votes[i]*weights[i]
		return score

	def read_xml(self, xml_name):
		logging.info('Lendo arquivo xml de consultas')
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
				votes = [int(x) for x in item.getAttribute("score")] 
				score = self.define_score(votes)
				docs_results.append([int(item.firstChild.nodeValue), score])
			content['Records'].append(docs_results)
		return content

	def generate_query_file(self, query_file, xml_name):
		content = self.read_xml(xml_name)

		with open(query_file, 'w', newline='') as csvfile:
			fieldnames = ['QueryNumber', 'QueryText']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			for index in range(0, len(content['QueryNumber'])):
				logging.info('Escrevendo consulta '+str(index+1)+'/'+str(len(content['QueryNumber'])))
				writer.writerow({'QueryNumber': content['QueryNumber'][index], 'QueryText': self.tokenize_query(content['QueryText'][index])})

	def generate_expected_file(self, expected_file, xml_name):
		content = self.read_xml(xml_name)

		with open(expected_file, 'w', newline='') as csvfile:
			fieldnames = ['QueryNumber', 'DocNumber', 'DocVotes']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			writer.writeheader()
			for index in range(0, len(content['QueryNumber'])):
				for result in content['Records'][index]:
					writer.writerow({'QueryNumber': content['QueryNumber'][index], 'DocNumber': result[0], 
									 'DocVotes': result[1]})

	def generate_files(self):
		logging.info('Iniciando geração dos arquivos de processamento de consultas')
		xml_file, query_file, expected_file = self.read_config_file()
		logging.info('Gerando arquivo de consultas')
		self.generate_query_file(query_file, xml_file)
		logging.info('Gerando arquivo de documentos esperados')
		self.generate_expected_file(expected_file, xml_file)
