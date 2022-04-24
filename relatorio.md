# Relatorio iClinic

Neste relatório serão apresentadas as tomadas de decisão, etapas e ferramentas, assim como dificuldades encontradas na resolução do desafio.

Será apresentada a análise e tratamento de cada base de dados, começando com 'desafio-base1' e finalizando com 'desafio-base2'.

***
## Entendendimento do problema
***

Têm-se uma base de dados médica do Dr. José e outra da Dra. Ana, Dr. Carlos e Dr. Gustavo, ambas precisam ser transformadas para o padrão iClinic disponível em https://docs.iclinic.com.br.

Será feita uma exploração das bases de dados e comparação com o padrão solicitado através de bibliotecas Python&reg;.

***
## Tratamento da base de dados 'desafio-base1' 
***

O tratamento dos dados da base de dados 'desafio-base1' iniciou com arquivo `desafio-base1/pacientes.csv` por ser o que possuí maior volume de informações.
Em seguida serão analisados os próximos arquivos.

> É necessário manter a sequencia de análise proposta para o correto funcionamento das próximas scripts.

## Tratamento do arquivo 'pacientes.csv'
***

A script correspondente ao tratamento dos dados pode ser encontrada no arquivo `desafio-base1_pacientes.ipynb`.

## Exploração inicial e primeiras impressões

Nesta seção será apresentada a exploração inicial dos dados num caderno Jupyter ou [Jupyter Notebook](https://jupyter.org/).

Ao abrir o caderno `desafio-base1_pacientes.ipynb` será possível ver os códigos utilizados para o tratamento dos dados.

### Importação das bibliotecas

Na primeira célula é realizada a importação das bibliotecas utilizadas:

```python
import numpy as np
import pandas as pd
```

A seguir uma breve apresentação de cada biblioteca:

- A biblioteca [NumPy](https://numpy.org/) é fundamental para qualquer tipo de computação científica em Python
- A biblioteca [pandas](https://pandas.pydata.org/) é a ferramenta pricipal para análise e manipulação de dados

### Leitura e tratamento inicial dos dados de entrada

Na próxima célula é realizada a leitura do arquivo '.csv' através da biblioteca `pandas` utilizando a função `read_csv()`, como a seguir:

```python
df = pd.read_csv('desafio-base1/pacientes.csv', parse_dates=['DataNasc'], encoding='iso-8859-1',quotechar='"', delimiter='|')
```
Cada parâmetro tem o seguinte significado:

- `parse_dates=['DataNasc']`: Fazer a importação da coluna `'DataNasc'` como tipo `data hora`
- `encoding='iso-8859-1'`: Tipo de `encoding` do arquivo sendo lido
- `quotechar='"'`: O caracter usado para denotar o inicio e fim de um item entre aspas
- `delimiter='|'`: delimitador utilizado na escrita do arquivo

### Visualização dos dados

Nas próximas duas células é realizada a visualização inicial dos dados.

Usando o método `head()` do `pandas` com um argumento `5` nele é possível visualizar os primeiros `5` registros do Dataframe.
    
O `.T` significa `Transposição`, desta forma as linhas serão visualizadas como colunas e vice-versa.

O método `info()` do `pandas` apresenta um resumo dos dados no Dataframe, uma informação interessante é o tipo de dado de cada recurso.

## Limpeza e tratamento dos dados

A seguir será realizada a limpeza e tratamento dos dados.

### Valores ausentes, valores equivalentes e tratamento inicial

Quando utilizado o método `info()` para ver o resumo dos dados, foi possível ver que muitas colunas tinham muitos dados ausentes, entrentanto, na documentação da iClinic é possível ver que os campos `patient_id` e `name` são obrigatórios e no Dataset anterior as colunas `Código` e `Nome` são seus equivalentes, ainda, estas são as únicas colunas que não tem valores nulos nos seus registros, logo, a priori, não será necessário um maior tratamento para cumprir as condições obrigatórias.

O tratamento de algumas colunas será realizado em seguida, mas quando o tratamento necessário for apenas na mudança nos nomes entre os recursos equivalentes, este será realizada no final, já que não é relevante para o tratamento inicial.

Alguns dos recursos precisarão de uma atenção ou tratamento mais detalhada, são estes: "Telefone", "TipoTelefone" e "Endereco".

Além desses recursos, no arquivo lido tem informação adicional que pode ser colocado na coluna "observation", mas devido ao tempo não foi possível de ser concluído, são estas "Conjuge", "ProfissaoConjuge"

### Tratamento do recurso 'Sexo'
 
Inicialmente foram testadas algumas ideias mais simples, mas não resultaram sendo corretas.

A primeira consistiu em transformar as strings dentro da coluna 'Sexo' em minúscula:
```python
df['Sexo'] = df['Sexo'].astype(str).str.lower()
```
Porém, os valores 'NaN' eram modificados para 'nan', perdendo o seu significado original.

Outra alternativa foi utilizar list comprehension do próprio python, conseguindo contornar o problema de modificar o valor 'NaN':
```python
df['Sexo'] = ['m' if x == 'M' else 'f' if x == 'F' else np.nan for x in df['Sexo']]
#%timeit 594 µs ± 23.4 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
```

Finalmente, a seguinte alternativa foi a utilizada pois apresentava uma maior velocidade de processamento quando comparada a anterior.
```python
df['Sexo'] = df['Sexo'].replace(sexo)
#%timeit 694 µs ± 14.4 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
```
sendo:
```python
sexo = {
    'M': 'm', 
    'F': 'f'
}
```

### Tratamento do recurso 'Estado'

A fim de verificar se a coluna continha apenas os valores das siglas de cada estado, assim, foi criado uma lista contendo os valores possíveis:

```python
uf = [np.nan,'RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO', 'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA', 'MG', 'ES', 'RJ', 'SP', 'PR', 'SC', 'RS', 'MS', 'MT', 'GO', 'DF']
```

Em seguida, foi necessário realizar um pré processamento da coluna `df['Estado']`, retirando os espaços a mais nas strings armazenadas:

```python
df['Estado'] = [x.strip() if type(x) == str else np.nan for x in df['Estado']]
```

Finalmente, é realizada a validação através do comando `isin()` e `value_counts()`, como a seguir:

```python
df['Estado'].isin(uf).value_counts()
```

Caso existisse algum valor que não se encontrasse na lista `uf` apareceria como `False`, como não é o caso, não será necessário realizar algum pós-processamento.

### Tratamento do recurso 'CEP'

Foi percebido que nem todos os valores armazenado se encontram na formatação desejada, a principal diferença notada foi a falta do hífen dividindo os números, sendo assim será realizado o mapemento dos valores que contém ele a fim de modificar os valores que não o possuem: 

```python
rows_with_dashes = df['CEP'].str.contains('-')
df['CEP'] = [df['CEP'][i] if x == True else df['CEP'][i][:5]+'-'+df['CEP'][i][5:] if x == False else np.nan for i, x in enumerate(rows_with_dashes)]
```

### Tratamento do recurso 'EstadoCivil' <a id="ancora1"></a>

Para tratar esta coluna é necessário saber quais as categorias utilizadas para classificar o estado civil do paciente no Dataset anterior, assim, utilizaremos a seguinte linha de código:

```python
df['EstadoCivil'].value_counts()
```

Obtendo o seguinte output:

```python
CA    187
ES    170
VI    145
SE    132
```

É possível observar os valores equivalentes no padrão iClinic:

- CA : casado : ma
- ES : união estável : st
- VI : Viúvo : wi
- SE : Separado : se

Em seguida é aplicado o seguinte comando para fazer a substituição das categorias:

```python
df['EstadoCivil'] = df['EstadoCivil'].replace({'CA': 'ms', 'ES': 'st', 'VI': 'wi','SE': 'se'})
```

### Tratamento do recurso 'Cor'

Para tratar esta coluna também será necessário saber quais as categorias utilizadas para classificar a cor do paciente no Dataset anterior, assim, analogamente ao realizado no caso anteior:

```python
df['Cor'].value_counts()
```

Obtendo o seguinte output:

```python
B    132
A    131
P    127
N    127
I    114
```

Como realizado anteriormente, serão subsituidas essas categorias pelas equivalentes no padrão iClinic, como a seguir:

- B : Branca : wh
- A : Amarela :	ye
- P : Parda : br
- N : Negra : bl
- I : Indigena : br

Neste caso, foi decidido colocar a raça indigena como parda já que ela não possui uma categoria específica no padrão iClinic, e, no entender do autor, esta foi a mais proxima.

Em seguida é aplicado o seguinte comando para fazer a substituição das categorias:

```python
df['Cor'] = df['Cor'].replace({'B': 'wh', 'A': 'ye', 'P': 'br','N': 'bl', 'I': 'br'})
```

### Tratamento do recurso 'Endereco'

Nesta coluna estão incluidas as informações de outras colunas solicitadas no padrão iClinic.
Assim, será preciso dividir esta informação em novas colunas que serão criadas a seguir:

```python
df['address'] = np.nan
df['number'] = np.nan
df['complement'] = np.nan
df['neighborhood'] = np.nan
df['country'] = "BR"
```

Dessa forma, o valor padrão delas será `NaN` com excepção da coluna 'country'.

Em seguida, a informação contida no recurso 'Endereco' é dividida com o método `str.split(',')` e será armazenada numa coluna temporária de nome `row_with_adress`.

Finalmente, será feita a distribuição da informação de acordo ao seu tipo, como a seguir:

```python
row_with_adress = df['Endereco'].str.split(',')
df['number'] = [np.nan if str(x) == 'nan' else x[1].strip() if len(x) == 3 else np.nan for x in row_with_adress]
df['neighborhood'] = [np.nan if str(x) == 'nan' else x[1].strip() if len(x) == 2 else x[2].strip() for x in row_with_adress]
df['address'] = [np.nan if str(x) == 'nan' else x[0] for x in row_with_adress]
```

### Tratamento dos recursos 'TipoTelefone' e 'Telefone'

De modo semelhante ao realizado nos recursos 'EstadoCivil' e 'Cor', é necessário saber quais as categorias utilizadas para classificar o Tipo de telefone do paciente, assim, será aplicada a segiunte linha de código:

```python
print(df['TipoTelefone'].value_counts())
```
Obtendo o seguinte output:

```python
C    225
T    195
R    195
```

Como realizado anteriormente, serão subsituidas essas categorias pelas equivalentes no padrão iClinic, como a seguir:

- C : Celular : "mobile_phone"
- T : Trabalho : "office_phone"
- R : Residencial: "home_phone"

Porém, diferentemente do realizado anteriormente, será necessário distribuir as categorias de uma coluna em outras de acordo a sua categoria, assim serão criadas novas colunas vazias:

```python
df['mobile_phone'] = np.nan
df['office_phone'] = np.nan
df['home_phone'] = np.nan
```

Em seguida, serão extraídos somente os valores numéricos do recurso "Telefone" e serão armazenados de volta como `string`:

```python
df['Telefone'] = df['Telefone'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int).astype('str')
```

Finalmente, serão armazenados os numeros de telefone no formato desejado e na sua respectiva coluna:

```python
rows_t = df['TipoTelefone'].str.contains('T', na=False)
df['office_phone'] = '(' + df['Telefone'][rows_t].str[-10:-8] + ')' + df['Telefone'][rows_t].str[-8:-4] + '-' + df['Telefone'][rows_t].str[-4:]

rows_t = df['TipoTelefone'].str.contains('C', na=False)
df['mobile_phone'] = '(' + df['Telefone'][rows_t].str[:2] + ')9' + df['Telefone'][rows_t].str[-8:-4] + '-' + df['Telefone'][rows_t].str[-4:]

rows_t = df['TipoTelefone'].str.contains('R', na=False)
df['home_phone'] = '(' + df['Telefone'][rows_t].str[-10:-8] + ')' + df['Telefone'][rows_t].str[-8:-4] + '-' + df['Telefone'][rows_t].str[-4:]
```
### Mudança de nome das colunas para o padrão iClinic

Em seguida será realizada a mudança no nome dos recursos no Dataset anterior para os nomes equivalente ao padrão iClinic:

```python
df = df.rename(
    columns = {
        "Código":"patient_id",
        "Nome": "name",
        "DataNasc":"birth_date",
        "Sexo": "gender",
        "Estado": "state",
        "Cidade": "city",
        "CEP": "zip_code",
        "Naturalidade": "birth_place",
        "Profissao": "occupation",
        "Pai": "patientrelatedness_father_names",
        "Mae": "patientrelatedness_mother_names",
        "Cor": "ethnicity",
        "EstadoCivil": "marital_status",
    }
)
```

### Adição de recursos ausentes

Ainda, pelo modelo `importacao-iclinic/patient.csv` é necessário adicionar algumas colunas ausentes, ou seja, que não foram passadas no documento de entrada, por padrão iremos colocar o valor `NaN` nelas:

```python
df['gender'] = np.nan
df['cpf'] = np.nan
df['rg'] = np.nan
df['rg_issuer'] = np.nan #segundo o modelo encontrado na documentação da iClinic, aqui está repetido 'rg' ao invés de 'rg_issuer', então colocaremos como achamos certo
df['email'] = np.nan
df['email_secondary'] = np.nan
df['birth_state'] = np.nan
df['picture_filename'] = np.nan
df['religion'] = np.nan
df['education'] = np.nan
df['responsible'] = np.nan
df['cns'] = np.nan #na documentação da iClini não existe 'sms' mas aparece segundo o modelo, pelo que não foi adicionado aqui
df['died'] = np.nan
df['death_info'] = np.nan
df['nationality'] = np.nan 
df['indication'] = np.nan
df['indication_observation'] = np.nan
df['active'] = np.nan 
df['receive_email'] = np.nan
df['observation'] = np.nan
df['healthinsurance_pack'] = np.nan 
df['tag_names'] = np.nan
df['tag_physician_id'] = np.nan
```

### Remoção de recursos repetidos ou não necessários

A seguir, serão removidos os recursos repetidos ou que não são mais necessários:

```python
df =  df.loc[:, ["patient_id","name","birth_date","gender","cpf","rg","rg_issuer","mobile_phone","home_phone","office_phone","email","email_secondary","birth_place","birth_state","zip_code","address","number","complement","neighborhood","city","state","country","picture_filename","ethnicity","marital_status","religion","occupation","education","responsible","cns","died","death_info","nationality","indication","indication_observation","active","receive_email","observation","healthinsurance_pack","patientrelatedness_mother_names","patientrelatedness_father_names","tag_names","tag_physician_id"]]
```

## Exportação do arquivo de saída

Como solicitado no desafio, o arquivo de saída será gerado com o conjunto de caracteres `UTF-8`:

```python
df.to_csv('patient.csv',index=False, encoding='utf-8')
```

## Tratamento dos dados do arquivo 'agenda.csv'
***

Como o tratamento para este arquivo é semelhante ao realizado com o arquivo 'pacientes.csv' na seção passada, foi escolhido deixar o tratamento no caderno [Jupyter](https://jupyter.org/) para não deixar este arquivo muito extenso.

Assim, o relatório deste tratamento se encontra no arquivo `desafio-base1_agenda.ipynb`.

## Tratamento dos dados do arquivo 'evolucao.csv'
***

Como o tratamento para este arquivo é semelhante ao realizado com o arquivo 'pacientes.csv' na seção passada, foi escolhido deixar o tratamento no caderno [Jupyter](https://jupyter.org/) para não deixar este arquivo muito extenso.

Assim, o relatório deste tratamento se encontra no arquivo `desafio-base1_evolucao.ipynb`.

***
## Tratamento da base de dados 'desafio-base2' 
***

O tratamento dos dados da base de dados 'desafio-base2' iniciou com a importação do arquivo SQL `desafio-base2/backup.sql`, para o servidor local MySQL, em seguida foi realizada uma análise do conteúdo e relação das tabelas do banco de dados, gerando o arquivo `EER_Diagram_dbase03.pdf` o qual contém uma representação simples, em diagrama, das tabelas do banco de dados importada `dbase03` (repare que não foi possível encontrar as `foreing keys` ou chaves estrangeiras para a criação das setas relacionando as tabelas umas com as outras).

A seguir será apresentada a sequência de análise e tratamento dos dados, é importante ressaltar que é preciso manter esta sequência para o correto funcionamento das próximas scripts.

## Tratamento das tabelas 'plan02' e 'sysuser01'
***

A script correspondente ao tratamento dos dados pode ser encontrada no arquivo `desafio_base2_planos_e_medicos.ipynb`.

### Importação das bibliotecas
 
A seguir uma breve apresentação de cada biblioteca que será utilizada:

- A biblioteca [NumPy](https://numpy.org/) é fundamental para qualquer tipo de computação científica em Python
- A biblioteca [pandas](https://pandas.pydata.org/) é a nossa ferramenta pricipal para análise e manipulação de dados
- A biblioteca [python-decouple](https://github.com/henriquebastos/python-decouple) auxiliar para trabalhar com variaveis de ambiente
- A biblioteca [SQLAlchemy](https://www.sqlalchemy.org/) é uma biblioteca de mapeamento objeto-relacional SQL

```python
import numpy as np
import pandas as pd

import decouple
import sqlalchemy
```

### Leitura e tratamento inicial dos dados de entrada

Para poder realizar a conexão com o banco de dados `SQL`, precisaremos de algumas informações que estão armazenadas no arquivo `.env` e quer serão importadas através da biblioteca `decouple`, como a seguir:

```python
user = decouple.config("db_user_mysql")
host = decouple.config('db_host_mysql')
password = decouple.config('db_password_mysql')
database = decouple.config("db_database_mysql")
```
Através da biblioteca `sqlalchemy` será criado o objeto [Engine](https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Engine) que é baseado na URL do banco de dados.

```python
connection = sqlalchemy.create_engine("mysql+mysqldb://"+user+":"+password+"@"+host+"/"+database)
```

Será necessário instalar o pacote cujo nome para instalação no Ubuntu 20.04 é `libmysqlclient-dev` para utilizar o driver `mysqldb`, caso não esteja instalado.

Em seguida, através da biblioteca `pandas` é realizada a importação da tabela 'plan02' utilizando a função `read_sql_table()`, onde o parâmetro `con = connection` é o objeto `engine` criado na célula anterior.

```python
df = pd.read_sql_table('plan02', con = connection)
```

### Visualização dos dados

Nas próximas duas células é realizada a visualização inicial dos dados.

Usando o método `head()` do `pandas` com um argumento `4` nele é possível visualizar os primeiros `4` registros do Dataframe.
    
O `.T` significa `Transposição`, desta forma as linhas serão visualizadas como colunas e vice-versa.

```python
df.head(4).T
```
O método `info()` do `pandas` apresenta um resumo dos dados no Dataframe, uma informação interessante é o tipo de dado de cada recurso.

```python
df.info()
```

### Remoção de recursos repetidos ou não necessários

A seguir, serão removidos os recursos que o autor não achou necessários:

```python
df =  df.loc[:, ["plan","code","name","account","billsenddayinternal","returndaysexternal"]]
```

### Exportação do arquivo de saída

O arquivo de saída a seguir será gerado com o conjunto de caracteres `UTF-8`, e será útil para o tratamento das próximas tabelas:

```python
df.to_csv('desafio-base2-output/planos.csv',index=False, encoding='utf-8')
```

### Leitura e tratamento inicial dos dados de entrada

Em seguida, será realizada a importação da tabela 'sysuser01'.

```python
df = pd.read_sql_table('sysuser01', con = connection)
```

### Visualização dos dados

Nas próximas duas células é realizada a visualização inicial dos dados.

```python
df.head(3).T
```

e

```python
df.info()
```

### Remoção de recursos repetidos ou não necessários

A seguir, serão removidos os recursos que o autor não achou necessários:

```python
df =  df.loc[:, ["sysuser","name"]]
```

### Exportação do arquivo de saída

O arquivo de saída a seguir será gerado com o conjunto de caracteres `UTF-8`, e será útil para o tratamento das próximas tabelas:

```python
df.to_csv('desafio-base2-output/physician_names.csv',index=False, encoding='utf-8')
```

## Tratamento da tabela 'patient01' 
***

Como o tratamento para este arquivo é semelhante ao realizado com as tabelas 'plan02' e 'sysuser01' na seção passada, foi escolhido deixar o tratamento no caderno [Jupyter](https://jupyter.org/) para não deixar este arquivo muito extenso.

Assim, o relatório deste tratamento se encontra no arquivo `desafio_base2_pacientes.ipynb`.

## Tratamento da tabela 'text04' 
***

Como o tratamento para este arquivo é semelhante ao realizado com as tabelas 'plan02' e 'sysuser01' na seção passada, foi escolhido deixar o tratamento no caderno [Jupyter](https://jupyter.org/) para não deixar este arquivo muito extenso.

Assim, o relatório deste tratamento se encontra no arquivo `desafio_base2_agenda.ipynb`.

## Tratamento da tabela 'text01' 
***

Como o tratamento para este arquivo é semelhante ao realizado com as tabelas 'plan02' e 'sysuser01' na seção passada, foi escolhido deixar o tratamento no caderno [Jupyter](https://jupyter.org/) para não deixar este arquivo muito extenso.

Assim, o relatório deste tratamento se encontra no arquivo `desafio_base2_evolucao.ipynb`.

## Conclusão

Após a execução do tratamento dos dados dos arquivo da pasta `desafio-base1` serão obtidos os arquivos 'patient.csv', 'event_scheduling.csv' e 'event_record.csv' na pasta `desafio-base1-output/`.

Após a execução do tratamento da base de dados SQL da pasta `desafio-base2` serão obtidos os arquivos 'patient.csv', 'event_scheduling.csv' e 'event_record.csv' na pasta `desafio-base2-output/`, além dos arquivos terceriso utilizados para armazenar informação relevante.

Esperamos que o relatório tenha sido claro o suficiente, qualquer dúvida estou a disposição para explicar.

___
Jonathan Silva