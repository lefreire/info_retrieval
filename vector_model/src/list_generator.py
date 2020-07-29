import configparser
import csv
import logging
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
	  config.read('GLI.CFG')
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

	def get_words_doc(self, xml_content):
	  xml_content['new_abstract'] = []
	  words_dict = {}
	  for index in range(0, len(xml_content['abstract'])):
	    abstract = unicodedata.normalize('NFD', xml_content['abstract'][index])
	    abstract = str(abstract.encode('ascii', 'ignore').decode("utf-8"))
	    tokenizer = RegexpTokenizer(r'\w+')
	    xml_content['new_abstract'].append(tokenizer.tokenize(abstract.upper()))
	  for index in range(0, len(xml_content['new_abstract'])):
	    while '' in xml_content['new_abstract'][index]: xml_content['new_abstract'][index].remove('')
	  for index in range(0, len(xml_content['new_abstract'])):
	    for word in xml_content['new_abstract'][index]:
	      docs_number = []
	      for next_index in range(index, len(xml_content['new_abstract'])):
	        while word in xml_content['new_abstract'][next_index]:
	          docs_number.append(int(xml_content['recordnum'][next_index]))
	          xml_content['new_abstract'][next_index].remove(word)
	      words_dict[word] = docs_number   
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
