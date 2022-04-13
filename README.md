# Desafio iClinic

O desafio consistiu em analisar e desenvolver scripts de conversão de dados médicos fictícios para o padrão iClinic, tratando dados sensíveis e não padronizados.

### Solução

Analisar, relacionar, transformar e desenvolver script em Python&reg; de conversão de dados médicos fictícios de duas fontes distintas para o padrão iClinic.

Os arquivos de dados médicos fictícios disponibilizados são:
- [Dados 1](https://github.com/iclinic/iclinic-migration-challenge/blob/master/desafio-base1.zip), do Dr. José;
- [Dados 2](https://github.com/iclinic/iclinic-migration-challenge/blob/master/desafio-base2.zip), da Dra. Ana, Dr. Carlos e Dr. Gustavo.

#### Detalhes:

- Os dados devem ser considerados dados sensíveis e é necessário manter seu conteúdo o mais próximo possível do original.
- Os dados que não fizerem parte do cadastro, do prontuário e do agendamento podem ser desconsiderados na conversão.
- Todo o processo de análise e de relacionamento dos dados deve ser documentado em um relatório, no qual deve descrever as etapas e ferramentas utilizadas de forma detalhada, bem como, toda informação que julgar relevante.
- O relatório está em formato markdown no link a seguir [relatorio.md](relatorio.md).
- A conversão dos dados deve gerar arquivos CSV, de acordo com a documentação que descreve o padrão iClinic, disponível em https://docs.iclinic.com.br. Além disso, os arquivos devem ser gerados com o conjunto de caracteres UTF-8.
- Caso sejam criados arquivos intermediários, para realização da conversão dos dados, estes também devem ser anexados juntos com seus respectivos scripts.
- Também deverá ser gerado um documento, nomeado README.md (o presente documento), contendo as instruções de como executar o(s) script(s) Python&reg;, a descrição dos arquivos intermediários, caso existam, e link para o relatório.

### Recursos solicitados e disponibilizados

- Disponibilizar a solução do desafio em um repositório GitHub;
- Que o código do desafio seja feito em Python 3+;
- Dados convertidos no formato CSV;
- Relatório com a descrição das etapas e ferramentas utilizadas;
- Passo a passo de como executar o script de conversão;
- Clareza no código;
- Gerenciamento de dependências;
- Commits semânticos.
- Utilizar as bibliotecas Pandas e de banco de dados;
- Princípios SOLID;

Neste repositório você encontrará os seguintes documentos:

- requirements.txt: arquivo contendo o nome dos pacotes que precisam ser instalados utilizando pip
- desafio-base1: Pasta contendo os arquivos csv de entrada
- importacao-iclinic: Pasta contendo os arquivos csv de referencia para o padrão iClinic
- desafio_base1_evolucao.ipynb: O Notebook Jupyter contendo a análise de dados do arquivo evolucao.csv na pasta desafio-base1
- desafio_base1_agenda.ipynb: O Notebook Jupyter contendo a análise de dados do arquivo agenda.csv na pasta desafio-base1
- desafio_base1_pacientes.ipynb: O Notebook Jupyter contendo a análise de dados do arquivo pacientes.csv na pasta desafio-base1
- relatorio.md: relatório descrevendo as etapas e ferramentas utilizadas na resolução do desafio de forma detalhada

# Instruções de uso

Para utilizar os dados e códigos neste repositório, siga os seguintes passos.

## Instalando o ambiente virtual e os pacotes Python

Criando um ambiente virtual na pasta do projeto a fim de isolar o nosso projeto em Python:

```sh
virtualenv -p python3 venv
``` 
Ativando o ambiente virtual:
```sh
source venv/bin/activate
```
Instalando os pacotes necessários:
```sh
pip install -r requirements.txt
```

## EDA (Exploratory Data Analysis)
Para ver o EDA no seridor local do Jupyter:
```sh
jupyter-notebook desafio_base1_pacientes.ipynb
jupyter-notebook desafio_base1_agenda.ipynb
jupyter-notebook desafio_base1_evolucao.ipynb

```
também pode ser aberto no VScode, caso tiver as extensões adequadas instaladas.
Em seguida vá em `Cell > Run All` para rodar todos os comandos.

## Limpeza de dados
A limpeza dos dados foi realizada nos Notebook jupyter acima, pelo que, após rodar todos os comandos terão sido criados os arquivos 'patient.csv', 'event_scheduling.csv' e 'event_record.csv'.

# Comentário final

Esperamos poder concluir o tratamento dos dadds do `desafio-base2` em breve.
Esperamos também que o arquivo README.md e o arquivo relatorio.md estejam o suficientemente claros para seu entendimento.

___
Jonathan Silva