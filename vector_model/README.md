# Exercício - Modelo Vetorial

## Estrutura do código

Na pasta *src*:

1. **pastas:**

	- *config*: contém todos os arquivos de configuração. Nos arquivos de configuração estão presentes os caminhos dos arquivos a serem lidos e a serem escritos, além de indicar se será/foi utilizado stemmer ou não. Na primeira linha dos arquivos de configuração, haverá a tag **STEMMER** indicando o uso do stemmer de Porter ou **NOSTEMMER**, indicando o não uso. Os arquivos a serem lidos estão indicados na tag **INPUT** e os arquivos a serem escritos estão indicados na tag **OUTPUT**.

	- *result*: contém todos os arquivos produzidos pelo código. Além disso, tem a palavra chave **stemmer/nostemmer** no nome, indicando o uso ou não de stemmer. São eles: 

		- consultas_stemmer/nostemmer.csv: contém todas as consultas que serão realizadas

		- resultados_esperados.csv: contém os documentos esperados a serem recuperados para cada consulta realizada

		- output_stemmer/nostemmer.csv: contém a frequência das palavras em cada documento

		- modelo_stemmer/nostemmer.json: contém o modelo vetorial, indicando os pesos de cada palavra em cada documento em que aparecem

		- resultados_stemmer/nostemmer.csv: contém os documentos recuperados pelo modelo a partir das consultas dadas, que obtiveram similaridade maior ou igual a 0.55

	- *data*: arquivos de onde serão extraídas as consultas e os documentos para a recuperação

	- *avalia*: contém todos os gráficos gerados pela avaliação do sistema criado e arquivos .csv com as informações que geraram os gráficos. Os gráficos e arquivos .csv estão compostos da seguinte forma: **nome_da_avaliação-stemmer/nostemmer-sequencial**. O **stemmer/nostemmer** indica se foi utilizado o stemmer de Porter ou não.

2. **queries_processor.py:** lê as consultas presentes em um arquivo xml e os documentos esperados a serem recuperados por estas consultas

3. **list_generator.py:** para cada palavra presente nos documentos, calcula a frequência com que aparecem

4. **indexer.py:** calcula tf-idf das palavras que estão nos documentos

5. **queries_search:** recupera os documentos da coleção de acordo com cada consulta processada em *queries_processor.py*

6. **diagram.py:** cria gráficos para as métricas de avaliação do sistema

7. **results_file.py:** cria os arquivos **.csv** com os resultados das métricas de  avaliação do sistema e o arquivo com todos os resultados chamado **relatorio.md**

8. **metrics.py:** calcula todas as métricas importantes para avaliação do sistema

9. **stemmer.py:** aplica o stemmer de Porter em uma dada string.

10. **main.py:** executa cada um dos passos da recuperação dos documentos de acordo com as consultas.

11. **main_metrics.py:** executa as métricas para avaliação do sistema, gera seus gráficos e arquivos com os resultados.

Tanto nas consultas, presentes em *consultas_stemmer/nostemmer.csv*, quanto nas palavras, presentes em *output_stemmer/nostemmer.csv*, foram retirados os stopwords e caracteres indesejados, como \n, (, ).

## Execução

Para executar o código do sistema, dentro da pasta *src*, utilize o comando:

``` 
python main.py
```

Para executar o código de avaliação do sistema, dentro da pasta *src*, utilize o comando:

``` 
python main_metrics.py
```