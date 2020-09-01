# Exercício - Pos Tagging

## Estrutura do código

1. Na pasta *src*:

	1. **read_file.py:** lê o arquivo com as sentenças, separa as palavras das tags, separa o dataset em treino e teste, além de escrever o relatório, contendo a acurácia geral e a porcentagem de cada tag no dataset.

	2. **learner.py:** calcula o algoritmo de Viterbi para uma dada observação.

	3. **decoder.py:** traduz os indíces retornados pelo algoritmo de Viterbi para a tag correspondente.

	4. **evaluation.py:** calcula a acurácia das tags que foram definidas pelo algoritmo de Viterbi, além de calcular a quantidade de vezes que uma tag foi predita corretamente

	5. **pos_tagging.py:** executa cada um dos passos para predição das tags de teste e escreve os resultados no arquivo *relatorio.txt*

2. Na pasta *data*: são encontrados os arquivos usados para o treinamento e predição das tags

3. **relatorio.txt:** arquivo com os resultados da acurácia geral do sistema e com a acurácia de cada classe. Quando uma classe não foi encontrada nas sentenças de teste, afirmamos que a classe *"Nao presente no corpus de teste."*.


## Execução

Para executar o código do sistema, dentro da pasta *src*, utilize o comando:

``` 
python pos_tagging.py 
```
