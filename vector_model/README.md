# Exercício - Modelo Vetorial

## Estrutura do código

Na pasta *src*:
	- **pastas:**
		- *config*: contém todos os arquivos de configuração. Nos arquivos de configuração estão presentes os caminhos dos arquivos a serem lidos e a serem escritos. Os arquivos a serem lidos estão indicados na tag **INPUT** e os arquivos a serem escritos estão indicados na tag **OUTPUT**.
		- *result*: contém todos os arquivos produzidos pelo código. São eles: 
			- consultas.csv: contém todas as consultas que serão realizadas
			- esperados.csv: contém os documentos esperados a serem recuperados para cada consulta realizada
			- output.csv: contém a frequência das palavras em cada documento
			- modelo.json: contém o modelo vetorial, indicando os pesos de cada palavra em cada documento em que aparecem
			- resultados.csv: contém os documentos recuperados pelo modelo a partir das consultas dadas
		- *data*: arquivos de onde serão extraídas as consultas e os documentos para a recuperação
	- **queries_processor.py:** lê as consultas presentes em um arquivo xml e os documentos esperados a serem recuperados por estas consultas
	- **list_generator.py:** para cada palavra presente nos documentos, calcula a frequência com que aparecem
	- **indexer.py:** calcula tf-idf das palavras que estão nos documentos
	- **queries_search:** recupera os documentos da coleção de acordo com cada consulta processada em *queries_processor.py*
	- **main.py:** executa cada um dos passos da recuperação dos documentos de acordo com as consultas.

## Execução

Para executar o código, dentro da pasta *src*, utilize o comando:

``` python main.py
```