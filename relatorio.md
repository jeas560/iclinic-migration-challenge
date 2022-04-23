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

<!-- Em seguida será printada na tela o `shape` que é de 783x18, ou seja, têm-se 738 linhas (registros), além da linha correspondente ao cabeçalho do arquivo `.csv`, e 18 colunas (recursos). -->

### Visualização dos dados

Nas próximas duas células é realizada a visualização inicial dos dados.

Usando o método `head()` do `pandas` com um argumento `5` nele é possível visualizar os primeiros `5` registros do Dataframe.
    
O `.T` significa `Transposição`, desta forma as linhas serão visualizadas como colunas e vice-versa.

O método `info()` do `pandas` apresenta um resumo dos dados no Dataframe, uma informação interessante é o tipo de dado de cada recurso.

## Limpeza e tratamento dos dados

A seguir será realizada a limpeza e tratamento dos dados.

### Valores ausentes

Quando utilizamos o método `info()` para ver o resumo dos dados, foi possível ver que muitas colunas tinham muitos dados ausentes, entrentanto, é solicitado na documentação da iClinic que os campos `patient_id` e `name` sejam obrigatórios, como é possível ver, nas colunas `Código` e `Nome`, que são seus correspondentes, estas são as únicas colunas que não tem valores nulos nos seus registros, logo não será preciso maior tratamento para cumprir as condições obrigatórias.

### Recursos equivalentes

Como comentado anteriormente, é possível ver que muitos dos recursos no arquivo lido possuem uma relação de equivalencia quase direta com os recursos da documentação iClinic, são estes:

- "Código":"patient_id"
- "Nome": "name"
- "DataNasc":"birth_date"
- "Sexo": "gender"
- "Estado": "state"
- "Cidade": "city"
- "CEP": "zip_code"
- "Naturalidade": "birth_place"
- "Profissao": "occupation"
- "Pai": "patientrelatedness_father_names"
- "Mae": "patientrelatedness_mother_names"
- "Cor": "ethnicity"
- "EstadoCivil": "marital_status"

O tratamento destes recursos será realizado em seguida, já que é relativamente simples. 

A mudança nos nomes entre os recursos equivalentes será realizada no final, já que não é relevante para este início.

Uns recursos precisarão de uma atenção ou tratamento mais detalhada, são estes: "Telefone", "TipoTelefone" e "Endereco".

Além desses recursos, no arquivo lido tem informação adicional que pode ser colocado na coluna "observation", mas devido ao tempo não foi possível de ser concluído, são estas "Conjuge", "ProfissaoConjuge"

### Tratando o recurso "Sexo"
 
Neste recurso precisaremos apenas trocar os caractéres 'M' por 'm' e 'F' por 'f', entretanto, utizaremos um procedimento com `list comprehension` para chegar neste fim. 

É possível ver uns comentários nessa célula, pois foi realizada uma tentativa utilizando os métodos `.astype(str).str.lower()` entretanto, desta forma o valor `NaN` era substituido por uma `string` equivalente, o que podia trazer informação errada na hora de verificar os dados.

Com o código a seguir é possível realizar esta mudança e não mudar o valor simbólico do `NaN`:

```python
df['Sexo'] = ['m' if x == 'M' else 'f' if x == 'F' else np.nan for x in df['Sexo']]

```

### Tratando o recurso "Estado"

Neste caso, apenas verificaremos se este recurso possui seus registros de forma correta, ou seja só duas letras em maiúscula para cada Estado brasileiro:

```python
teste = df['Estado'].str.contains(r'\b[A-Z]{2}')
print(teste.value_counts())

```

O método `str.contains(r'\b[A-Z]{2}')` retorna `True` se o registro avaliado contem o padrão ou `Regex` indicado e `False` caso contrário, caso o registro for `NaN` o valor permanece inalterado.

Ao aplicar o cógigo acima, obtemos no seguinte resultado `True    632`, e, ao comparar com o resultado dos valores não nulos deste recurso, é possível afirmar que todos os registros estão na forma correta.

Ainda, seria interessante fazer a validação se cada um dos registros possui as siglas que representam um estado brasileiro, pois pode ter acontecido alguma escrita errada na hora de entrar com a informação do paciente.

### Tratando o recurso "CEP"

É realizado o mapemento dos registros que possuem o caracter '-' para em seguida formatar aqueles onde o valor não for `True`, da seguinte forma:

```python
rows_with_dashes = df['CEP'].str.contains('-')
df['CEP'] = [df['CEP'][i] if x == True else df['CEP'][i][:5]+'-'+df['CEP'][i][5:] if x == False else np.nan for i, x in enumerate(rows_with_dashes)]

```

Repare que os valores `NaN` permanecem inalterados.

### Tratando o recurso "EstadoCivil" <a id="ancora1"></a>

Neste recurso precisamos antes de tudo saber quais as categorias utilizadas para classificar o estado civil do paciente, assim, utilizaremos a seguinte linha de código:

```python
print(df['EstadoCivil'].value_counts())
```

Obtendo o seguinte output:

```python
CA    187
ES    170
VI    145
SE    132
```

É possível observar que precisaremos subsituir essas categorias pelas equivalentes no padrão iClinic, como a seguir:

- CA : casado : ma
- ES : união estável : st
- VI : Viúvo : wi
- SE : Separado : se

Em seguida é aplicado o seguinte comando para fazer a substituição das categorias:

```python
df['EstadoCivil'].replace({'CA': 'ms', 'ES': 'st', 'VI': 'wi','SE': 'se'}, inplace=True)
```

O parâmetro `inplace=True` garante que será feita a substituição na mesma coluna, e não uma cópia em outra coluna como por padrão.

### Tratando o recurso "Cor"

De modo semelhante ao realizado no recurso "EstadoCivil", precisamos saber quais as categorias utilizadas para classificar a cor do paciente, assim, utilizaremos a seguinte linha de código:

```python
print(df['Cor'].value_counts())
```

Obtendo o seguinte output:

```python
B    132
A    131
P    127
N    127
I    114
```

Como realizado anteriormente, precisaremos subsituir essas categorias pelas equivalentes no padrão iClinic, como a seguir:

- B : Branca : wh
- A : Amarela :	ye
- P : Parda : br
- N : Negra : bl
- I : Indigena : br

Neste caso, decidimos colocar a raça indigena como parda já que não possui uma categoria específica no padrão iClinic, e esta foi a mais proxima no entender do autor.

Em seguida é aplicado o seguinte comando para fazer a substituição das categorias:

```python
df['Cor'].replace({'B': 'wh', 'A': 'ye', 'P': 'br','N': 'bl', 'I': 'br'}, inplace=True)
```

### Tratando o recurso "Endereco"

Neste recurso estão incluidas as informações de outros recursos solicitados no padrão iClinic.
Assim, precisaremos dividir esta informação em novos recursos, pelo que criaremos os seguintes recursos:

```python
df['address'] = np.nan
df['number'] = np.nan
df['complement'] = np.nan
df['neighborhood'] = np.nan
df['country'] = "BR"
```

Dessa forma, o valor padrão delas será `NaN` com excepção do recurso 'country', repare que criamos as novas colunas de acordo ao padrão iClinic.

Em seguida, separaremos a informação contida no recurso 'Endereco' com o método `str.split(',')` e a armazenaremos numa coluna temporária cujo nome será `row_with_adress`.

Finalmente, distribuiremos a informação de acordo ao seu tipo, como a seguir:

```python
row_with_adress = df['Endereco'].str.split(',')
df['number'] = [np.nan if str(x) == 'nan' else x[1].strip() if len(x) == 3 else np.nan for x in row_with_adress]
df['neighborhood'] = [np.nan if str(x) == 'nan' else x[1].strip() if len(x) == 2 else x[2].strip() for x in row_with_adress]
df['address'] = [np.nan if str(x) == 'nan' else x[0] for x in row_with_adress]
```

### Tratando o recurso "TipoTelefone" e "Telefone"

De modo semelhante ao realizado nos recursos "EstadoCivil" e "Cor", precisamos saber quais as categorias utilizadas para classificar o Tipo de telefone do paciente, assim, utilizaremos a seguinte linha de código:

```python
print(df['TipoTelefone'].value_counts())
```
Obtendo o seguinte output:

```python
C    225
T    195
R    195
```

Diferentemente do realizado anteriormente, precisaremos distribuir as categorias nos rescursos equivalentes no padrão iClinic, como a seguir:

- C : Celular : "mobile_phone"
- T : Trabalho : "office_phone"
- R : Residencial: "home_phone"

Pelo que criaremos os seguintes recursos:

```python
df['mobile_phone'] = np.nan
df['office_phone'] = np.nan
df['home_phone'] = np.nan
```

Em seguida, extrairemos somente os valores numéricos do recurso "Telefone" e os armazenaremos de volta como `string`:

```python
df['Telefone'] = df['Telefone'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int).astype('str')
```

Finalmente, armazenaremos os numeros de telefone no formato desejado e no seu devido recurso dependendo do seu tipo:

```python
rows_t = df['TipoTelefone'].str.contains('T', na=False)
df['office_phone'] = '(' + df['Telefone'][rows_t].str[-10:-8] + ')' + df['Telefone'][rows_t].str[-8:-4] + '-' + df['Telefone'][rows_t].str[-4:]

rows_t = df['TipoTelefone'].str.contains('C', na=False)
df['mobile_phone'] = '(' + df['Telefone'][rows_t].str[:2] + ')9' + df['Telefone'][rows_t].str[-8:-4] + '-' + df['Telefone'][rows_t].str[-4:]

rows_t = df['TipoTelefone'].str.contains('R', na=False)
df['home_phone'] = '(' + df['Telefone'][rows_t].str[-10:-8] + ')' + df['Telefone'][rows_t].str[-8:-4] + '-' + df['Telefone'][rows_t].str[-4:]
```
### Tratando os recursos equivalentes

Como comentado no inicio desta seção, será realizada agora a mudança no nome dos recursos cuja relação é diretamente equivalente ao padrão iClinic:

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

### Adicionando recursos ausentes

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

### Removendo Recursos repetidos ou não necessários

Aqui, iremos remover os recursos repetidos ou que não são mais necessários, como a seguir:

```python
df =  df.loc[:, ["patient_id","name","birth_date","gender","cpf","rg","rg_issuer","mobile_phone","home_phone","office_phone","email","email_secondary","birth_place","birth_state","zip_code","address","number","complement","neighborhood","city","state","country","picture_filename","ethnicity","marital_status","religion","occupation","education","responsible","cns","died","death_info","nationality","indication","indication_observation","active","receive_email","observation","healthinsurance_pack","patientrelatedness_mother_names","patientrelatedness_father_names","tag_names","tag_physician_id"]]
```

## Escrevendo o arquivo de saída

Como solicitado no desafio, o arquivo de saída será gerado com o conjunto de caracteres `UTF-8`:

```python
df.to_csv('patient.csv',index=False, encoding='utf-8')
```

## Tratamento dos dados do arquivo 'agenda.csv'

Nesta seção trabalharemos no arquivo `desafio-base1_agenda.ipynb`.

## Exploração inicial e primeiras impressões

Análogamente ao realizado no primeiro dataset, nesta seção iremos realizar uma exploração inicial também realizada num [Notebook Jupyter](https://jupyter.org/).

### Importando Bibliotecas

As bibliotecas importadas serão as mesmas que foram utilizadas pro arquivo anterior:

```python
import numpy as np
import pandas as pd
```

### Lendo e análise inicial dos dados de entrada

Novamente, utilizaremos a função `read_csv()` do `pandas`, com os seguintes parâmetros: `parse_dates=['Data'], encoding='iso-8859-1', quotechar='"', delimiter='|'`, como utilizado na seção anterior.

Em seguida será printada na tela o `shape` que é de 1230x9, ou seja, têm-se 1230 linhas (registros), além da linha correspondente ao cabeçalho do arquivo `.csv`, e 9 colunas (recursos).

```python
df = pd.read_csv('desafio-base1/agenda.csv', parse_dates=['Data'], encoding='iso-8859-1',quotechar='"', delimiter='|')
df.shape
```

### Vendo os dados

Usando o métoto `head()` do `pandas` com um argumento `3` nele, veremos os primeiros `3` registros da tabela interia.

De modo semelhante, o método `info()` do `pandas` nos dará um resumo dos dados, para que possamos saber como tratar os dados.

## Limpando e tratando os dados

Nesta seção iremos realizar a limpeza dos dados.

### Valores ausentes

Quando utilizamos o método `info()` para ver o resumo dos dados, foi possível ver que muitas colunas tinham muitos dados ausentes, entrentanto, é solicitado na documentação da iClinic que os campos `patient_name`, `physician_id` e `date` sejam obrigatórios, como é possível ver, nas colunas `Usuário`, `Código` e `Data` são suas colunas correspondentes, estas são as únicas colunas que não tem valores nulos nos seus registros, logo não será preciso maior tratamento para cumprir as condições obrigatórias.

### Recursos equivalentes

Como comentado anteriormente, é possível ver que muitos dos recursos no arquivo lido possuem uma relação de equivalencia quase direta com os recursos da documentação iClinic, são estes:

- "Código":"physician_id"
- "Usuário": "patient_name"
- "Data":"date"
- "HoraConsulta": "arrival_time"
- "HoraAtendimento": "start_time"
- "HoraFim": "end_time"
- "CodConvenio": "healthinsurance_name"
- "Tipo": "name"
- "Valor": "value"

O tratamento destes recursos será realizado em seguida, já que é relativamente simples. 

A mudança nos nomes entre os recursos equivalentes será realizada no final, já que não é relevante para este início.

Uns recursos precisarão de uma atenção ou tratamento mais detalhada, são estes: "Tipo" e "Valor".

### Tratando os recursos "HoraConsulta", "HoraAtendimento" e "HoraFim"
 
Nestes recursos será realizada apenas a formatação das horas como solicitado no padrão iClinic, ainda, como não foi informado a data de entrada, deixaremos só o tempo na coluna do recurso "HoraConsulta", como mostrado a seguir:

```python
df['HoraConsulta'] = pd.to_datetime(df['HoraConsulta'], format='%H:%M:%S').dt.time
df['HoraAtendimento'] = pd.to_datetime(df['HoraAtendimento'], format='%H:%M:%S').dt.time
df['HoraFim'] = pd.to_datetime(df['HoraFim'], format='%H:%M:%S').dt.time
```

### Tratando o recurso "CodConvenio"
 
Neste recurso não tivemos acesso aos nomes dos convênios, mas se tivessemos eles, realizariamos um procedimento semelhante ao realizado na seção [Tratando o recurso "EstadoCivil"](#ancora1).

### Tratando o recurso "physician_id"

Será criado um novo recurso com o nome "physician_id", como a seguir:

```python
df['physician_id'] = pd.factorize(df['Usuário'])[0].astype(int)
```

O método `factorize(df['Usuário'])` realiza o mapeamento dos valores do recurso, dando um número para cada usuário em `df['Usuário']` de forma sequencial.

### Exportando os nomes dos médicos

Aqui seria interessante criar uma lista relacionando o nome do médico e seu "physician_id" do médico para futuro tratamento, a seguir será exportado um arquivo `.csv` com os nomes dos médicos de forma ordenada.

```python
uniques = pd.factorize(df['Usuário'])[1]
pd_uniques = pd.DataFrame(data={"physician_names": uniques})
pd_uniques.to_csv('physician_names.csv',index=False, encoding='utf-8')
```

### Tratamento recurso 'patient_name'

Este recurso precisa de informação externa para ser tratado, resumidamente, utilizaremos o índice em "patient_id" para localizar o nome do usuário no arquivo "patient.csv"

```python
df_patient = pd.read_csv('patient.csv', usecols = ["name"])
```
Repare que estamos utilizando o arquivo com os dados tratados anteriormente.
Neste caso, como o 'patient_id' inicia com 0 e está ordenada é fácil de encontrar seu nome correspondente.

```python
index = df['Código'].values
df['patient_name'] = df_patient['name'][index].values
```

### Tratando do recurso 'eventprocedure_pack'

Será criado um novo recurso com o nome 'eventprocedure_pack', nele teremos que colocar os valores em formato `json`, pelo que utilizaremos o método `to_json` nos colunas 'Tipo' e 'Valor', neste caso foi utilizado parâmetro `force_ascii = False` para visualizar a escrita de forma correta em `utf-8`.
Além disso, como não temos a informação de recurso 'quantity', não colocaremos nada no lugar.

```python
df['eventprocedure_pack'] = ('json::['+df[['Tipo','Valor']].apply(lambda x: x.to_json(force_ascii =  False), axis=1)+']')
```

### Tratando os recursos equivalentes

Como comentado no inicio desta seção, será realizada agora a mudança no nome dos recursos cuja relação é diretamente equivalente ao padrão iClinic:

```python
df = df.rename(
    columns = {
        "Código": "patient_id",
        "Data": "date",
        "HoraConsulta": "arrival_time",
        "HoraAtendimento": "start_time",
        "HoraFim": "end_time",
        "CodConvenio": "healthinsurance_name",
        "Tipo": "name",
        "Valor": "value",
    }
)
```

### Adicionando recursos ausentes

Ainda, pelo modelo `importacao-iclinic/patient.csv` é necessário adicionar algumas colunas ausentes, ou seja, que não foram passadas no documento de entrada, por padrão iremos colocar o valor `NaN` nelas:

```python
df['status'] = 'cp'
df['patient_home_phone'] = np.nan
df['patient_mobile_phone'] = np.nan
df['description'] = np.nan
df['all_day'] = np.nan
df['cancel_reason'] = np.nan  
df['patient_email'] = np.nan  
df['event_blocked_scheduling'] = np.nan
df['quantity'] = np.nan  
```

### Removendo Recursos repetidos ou não necessários

Aqui, iremos remover os recursos repetidos ou que não são mais necessários, como a seguir:

```python
df = df.loc[:, ["patient_id","patient_name","physician_id","date","status","patient_home_phone","patient_mobile_phone","arrival_time","start_time","end_time","description","all_day","cancel_reason","patient_email","event_blocked_scheduling","healthinsurance_name","eventprocedure_pack"]]
```

## Escrevendo o arquivo de saída

Como solicitado no desafio, o arquivo de saída será gerado com o conjunto de caracteres `UTF-8`:

```python
df.to_csv('event_scheduling.csv',index=False, encoding='utf-8')
```

## Tratamento dos dados do arquivo 'evolucao.csv'

Nesta seção trabalharemos no arquivo `desafio-base1_evolucao.ipynb`.

## Exploração inicial e primeiras impressões

Análogamente ao realizado nos primeiros datasets, nesta seção iremos realizar uma exploração inicial também realizada num [Notebook Jupyter](https://jupyter.org/).

### Importando Bibliotecas

As bibliotecas importadas serão as mesmas que foram utilizadas pro arquivo anterior:

```python
import numpy as np
import pandas as pd
```

### Lendo e análise inicial dos dados de entrada

Novamente, utilizaremos a função `read_csv()` do `pandas`, com os seguintes parâmetros: `parse_dates=['Data'], encoding='iso-8859-1', quotechar='"', delimiter='|'`, como utilizado na seção anterior.

Em seguida será printada na tela o `shape` que é de 1230x6, ou seja, têm-se 1230 linhas (registros), além da linha correspondente ao cabeçalho do arquivo `.csv`, e 6 colunas (recursos).

```python
df = pd.read_csv('desafio-base1/evolucao.csv', parse_dates=['Data'], encoding='iso-8859-1',quotechar='"', delimiter='|')
df.shape
```

### Vendo os dados

Usando o métoto `head()` do `pandas` com um argumento `3` nele, veremos os primeiros `3` registros da tabela interia.

De modo semelhante, o método `info()` do `pandas` nos dará um resumo dos dados, para que possamos saber como tratar os dados.

## Limpando e tratando os dados

Nesta seção iremos realizar a limpeza dos dados.

### Valores ausentes

Quando utilizamos o método `info()` para ver o resumo dos dados, foi possível ver que muitas colunas tinham muitos dados ausentes, entrentanto, é solicitado na documentação da iClinic que os campos `patient_id`, `patient_name`, `physician_id`, `date` e `eventblock_text` sejam obrigatórios, como é possível ver, as colunas `Código`, `Data` e `Medico` são seus correspondentes, e a única coluna com valores nulos nos seus registros é a de procedimento.

### Recursos equivalentes

Como comentado anteriormente, é possível ver que muitos dos recursos no arquivo lido possuem uma relação de equivalencia quase direta com os recursos da documentação iClinic, são estes:

- "Código":"patient_id"
- "Data":"date"
- "Medico": "physician_id"
- "Procedimento": "tab_name"
- "Tipo": "eventblock_name"
- "Evolução": "eventblock_text"

O tratamento destes recursos será realizado em seguida. 

Uns recursos precisarão de uma atenção ou tratamento mais detalhada, são estes: "patient_name" e "physician_id".

Será realizada agora a mudança no nome dos recursos cuja relação é diretamente equivalente ao padrão iClinic:

```python
df = df.rename(
    columns = {
        "Código": "patient_id",
        "Data": "date",
        "Procedimento": "tab_name",
        "Tipo": "eventblock_name",
        "Evolução": "eventblock_text",
        "Medico": "physician_id",
    }
)
```

### Tratando do recurso "patient_name"

Este recurso precisa de informação externa para ser tratado, resumidamente, utilizaremos o índice em "patient_id" para localizar o nome do usuário na coluna "patient_name" no arquivo "patient.csv", como a seguir:

```python
df_patient = pd.read_csv('patient.csv', usecols = ["name"])
```
Repare que estamos utilizando o arquivo com os dados tratados anteriormente.
Neste caso, como o 'patient_id' inicia com 0 e está ordenada é fácil de encontrar seu nome correspondente:

```python
index = df['patient_id'].values
df['patient_name'] = df_patient['name'][index].values
```

### Tratando do recurso "physician_id"

Este recurso também precisa de informação externa para ser tratado, resumidamente, importaremos o dataframe do arquivo 'physician_names.csv', como a seguir:

```python
df_physician_names = pd.read_csv('physician_names.csv')
```

Em seguida, como o 'physician_names' está ordenado, podemos relacionar os indices de forma crescente e depois fazer a sua substituição devida.

```python
index_of_df_physician_names = pd.factorize(df_physician_names['physician_names'])[0].astype(int)
df['physician_id'].replace(df_physician_names.values,index_of_df_physician_names, inplace=True)
```

### Adicionando recursos ausentes

Ainda, pelo modelo `importacao-iclinic/event_record.csv` é necessário adicionar algumas colunas ausentes, ou seja, que não foram passadas no documento de entrada, por padrão iremos colocar o valor `NaN` nelas:

```python
df['start_time'] = np.nan
df['end_time'] = np.nan
```

### Removendo Recursos repetidos ou não necessários

Aqui, iremos remover os recursos repetidos ou que não são mais necessários, deixando apenas as colunas de interesse, como a seguir:

```python
df = df.loc[:, ["patient_id","patient_name","physician_id","date","start_time","end_time","tab_name","eventblock_name","eventblock_text"]]
```

## Escrevendo o arquivo de saída

Como solicitado no desafio, o arquivo de saída será gerado com o conjunto de caracteres `UTF-8`:

```python
df.to_csv('event_record.csv',index=False, encoding='utf-8')
```

## Conclusão

Após o tratamento dos dados dos arquivo da pasta `desafio-base1` foram obtidos os arquivos 'patient.csv', 'event_scheduling.csv' e 'event_record.csv'.

Esperamos que o relatório tenha sido claro o suficiente, qualquer dúvida estou a disposição para explicar.

___
Jonathan Silva