import configparser
import csv
import logging
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
import time
import unicodedata
from xml.dom.minidom import parse
import xml.dom.minidom


class ListGenerator:

	def __init__(self):
		"""
			Constructor
		"""
		logging.basicConfig(level=logging.INFO)
		logging.info('INICIANDO: MÓDULO GERADOR DE LISTA INVERTIDA')

	def read_config_file_xml(self):
		"""
			Reading configuration file

			Returns
			-------
			path_input_file: list of strings
			path_output_file: string
		"""
		logging.info('INICIANDO: leitura de arquivo de configuração GLI.CFG')
		config = configparser.ConfigParser()
		config.read('config/gli.cfg')
		config.sections()
		logging.info('FINALIZADO: leitura de arquivo de configuração GLI.CFG')
		return config['INPUT']['LEIA'].split(" "), config['OUTPUT']['ESCREVA']

	def read_xml_files(self, xml_files):
		"""
			Reading xml files to get the content in the tags RECORD, RECORDNUM, 
			ABSTRACT/EXTRACT

			Parameters
	        ----------
			xml_files: list with the xml files to read

			Returns
			-------

			content: dictionary with keys recordnum, abstract
		"""	
		logging.info('INICIANDO: leitura de arquivos xml')
		content = {'recordnum':[], 'abstract':[]}
		count_files = 1
		for xml_name in xml_files:
			logging.info('Lendo arquivo xml '+str(count_files)+'/'+str(len(xml_files)))
			doc = xml.dom.minidom.parse(xml_name).documentElement
			records = doc.getElementsByTagName("RECORD")
			for record in records:
				content['recordnum'].append(record.getElementsByTagName("RECORDNUM")[0].firstChild.nodeValue)
				if len(record.getElementsByTagName("ABSTRACT")) == 0:
					if len(record.getElementsByTagName("EXTRACT")) > 0:
						content['abstract'].append(record.getElementsByTagName("EXTRACT")[0].firstChild.nodeValue)
					else:
						content['abstract'].append(" ")    
				else:
					content['abstract'].append(record.getElementsByTagName("ABSTRACT")[0].firstChild.nodeValue)
			count_files += 1
		logging.info('FINALIZADO: leitura de arquivos xml')
		return content

	def tokenize_abstract(self, abstract):
		"""
			Gets a text, remove unwanted characters and stopwords

			Parameters
			----------
			abstract: string

			Returns
			-------
			tokenized_abstract: string
		"""
		tokenizer = RegexpTokenizer(r'\w+')
		stop_words = set(stopwords.words('english')) 

		abstract = unicodedata.normalize('NFD', abstract)
		abstract = str(abstract.encode('ascii', 'ignore').decode("utf-8"))
		abstract = tokenizer.tokenize(abstract.upper()) 
		return [w for w in abstract if not w.lower() in stop_words]

	def get_words_doc(self, xml_content):
		"""
			Counts how many times a word appears in the document
			Each document is represented by recordnum

			Parameters
			----------
			xml_content: dictionary with keys recordnum and abstract

			Returns
			-------
			words_dict: dictionary with keys = words in the text
		"""
		logging.info('INICIANDO: contagem de ocorrência das palavras nos documentos')
		start_time = time.time()
		xml_content['new_abstract'] = []
		words_dict = {}

		for index in range(0, len(xml_content['abstract'])):
			abstract = self.tokenize_abstract(xml_content['abstract'][index])
			fdist = FreqDist(abstract)
			for word in fdist.keys(): 
				if word in words_dict:
					words_dict[word].extend(fdist[word]*[int(xml_content['recordnum'][index])])
				else:
					words_dict[word] = fdist[word]*[int(xml_content['recordnum'][index])]
		logging.info('FINALIZADO: contagem de ocorrência das palavras nos documentos em '+str(time.time()-start_time))
		return words_dict

	def create_csv_words(self, csv_file, words_content):
		"""
			Creating csv file in path csv_file with content equals words_content

			Parameters
			----------
			csv_file: string
			words_content: dictionary

			Returns
			-------
			csv_file: file with headers [WORD, DOCS]
		"""
		logging.info('INICIANDO: criação de arquivo csv com lista invertida')
		with open(csv_file, 'w', newline='') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=['WORD', 'DOCS'])
			writer.writeheader()
			count_words = 1
			for key in words_content.keys():
				if count_words%1000 == 0:
					logging.info('Escrevendo palavra '+str(count_words)+'/'+str(len(words_content)))
				writer.writerow({'WORD': key, 'DOCS': words_content[key]})
				count_words += 1
		logging.info('FINALIZADO: criação de arquivo csv com lista invertida')

	def generate_list(self):
	  """
	  	Main method
	  	Reads all files and generate a list with words 
	  	and frequency in each document contained in read_files
	  """
	  read_files, write_file = self.read_config_file_xml()
	  content = self.read_xml_files(read_files)
	  words_content = self.get_words_doc(content)
	  self.create_csv_words(write_file, words_content)
	  logging.info('FINALIZADO: MÓDULO GERADOR DE LISTA INVERTIDA')
