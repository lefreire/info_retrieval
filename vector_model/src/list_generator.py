import configparser
import csv
import logging
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
import unicodedata
from xml.dom.minidom import parse
import xml.dom.minidom


class ListGenerator:

	def __init__(self):
		logging.basicConfig(level=logging.INFO)

	def read_config_file_xml(self):
	  logging.info('Lendo arquivo de configuração')
	  config = configparser.ConfigParser()
	  config.read('config/GLI.CFG')
	  config.sections()
	  return config['INPUT']['LEIA'].split(" "), config['OUTPUT']['ESCREVA']

	def read_xml_files(self, xml_files):
	  content = {'recordnum':[], 'abstract':[]}
	  for xml_name in xml_files:
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
	  return content

	def tokenize_abstract(self, abstract):
		tokenizer = RegexpTokenizer(r'\w+')

		abstract = unicodedata.normalize('NFD', abstract)
		abstract = str(abstract.encode('ascii', 'ignore').decode("utf-8"))
		return tokenizer.tokenize(abstract.upper())

	def get_words_doc(self, xml_content):
		xml_content['new_abstract'] = []
		words_dict = {}

		for index in range(0, len(xml_content['abstract'])):
			abstract = self.tokenize_abstract(xml_content['abstract'][index])
			while '' in abstract: abstract.remove('')
			fdist = FreqDist(abstract)
			for word in fdist.keys(): 
				if word in words_dict:
					words_dict[word].extend(fdist[word]*[int(xml_content['recordnum'][index])])
				else:
					words_dict[word] = fdist[word]*[int(xml_content['recordnum'][index])]
		return words_dict

	def create_csv_words(self, csv_file, words_content):
	  with open(csv_file, 'w', newline='') as csvfile:
	    writer = csv.DictWriter(csvfile, fieldnames=['WORD', 'DOCS'])
	    writer.writeheader()
	    for key in words_content.keys():
	      writer.writerow({'WORD': key, 'DOCS': words_content[key]})

	def generate_list(self):
	  read_files, write_file = self.read_config_file_xml()
	  content = self.read_xml_files(read_files)
	  words_content = self.get_words_doc(content)
	  self.create_csv_words(write_file, words_content)
