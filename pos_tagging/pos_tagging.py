import logging
logging.basicConfig(level=logging.INFO)
from decoder import Decoder
from evaluation import Evaluation
from learner import Learner
from read_file import ReadWriteFile


decoder_obj = Decoder()
learner_obj = Learner()
evaluation_obj = Evaluation()
read_obj = ReadWriteFile()
acc_geral = []

logging.info('Iniciando aprendizado...')
dict_tags, sentences_train, tags_train, sentences_test, tags_test = read_obj.read_and_split('data/completo_corpus100.txt')
for index in range(0, len(sentences_train)):
	logging.info('INICIANDO FOLD {0}'.format(index+1))
	y_pred = learner_obj.calculate_viterbi(sentences_train[index], 
											 tags_train[index], sentences_test[index])
	tag_pred = decoder_obj.decode_tags(y_pred, learner_obj.observations_mtx)
	acc, dict_tags = evaluation_obj.get_accuracy(tags_test[index], tag_pred, dict_tags)
	acc_geral.append(acc)
	logging.info('ACURÁCIA ALCANÇADA: {0:.2f}'.format(acc))

read_obj.write_file('relatorio.txt', acc, dict_tags)
logging.info('Finalizado...')
