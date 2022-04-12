# Relatorio iClinic

## EDA (Exploratory Data Analysis)

Comecemos com a análise da base de dados na pasta 'desafio-base1':

Iremos dividir nosso relatório em duas grandes partes:
- Entendendimento o problema
- Exploração e tratamento dos dados de cada arquivo na pasta 'desafio-base1'

Até o momento não foi possível realizar a análise do 'desafio-base2' por falta de tempo, pelo que não foi colocado neste repositório.

## O problema

Temos uma base de dados médica do Dr. José, que precisa ser transformada para o padrão iClinic.

Então iremos explorar a base de dados comparando com o padrão solicitado, utilizaremos algumas ferramentas para transformar os dados do arquivo de entrada no formato solicitado.

Começaremos a análies do arquivo `desafio-base1/pacientes.csv` e em seguida iremos analisando os próximos arquivos.

## Tratamento dos dados do arquivo 'pacientes.csv'

### Exploração inicial e primeiras impressões

Nesta seção iremos realizar uma exploração inicial do dataset.

Esta exploração foi realizada num [Notebook Jupyter](https://jupyter.org/).

#### Importando Bibliotecas

Começaremos importando as bibliotecas que serão utlizadas por padrão:

- A biblioteca [NumPy](https://numpy.org/) é fundamental para qualquer tipo de computação científica em Python
- A biblioteca [pandas](https://pandas.pydata.org/) é a nossa ferramenta pricipal para análise e manipulação de dados

```python
import numpy as np
import pandas as pd
```

#### Lendo e análise inicial dos dados de entrada

Como temos dados num arquivo '.csv', utilizaremos `pandas` para ler os dados e darmos uma primeira olhada em como eles estão dispostos.
Assim, utilizaremos a função `read_csv()` do `pandas`, com os seguintes parâmetros: `parse_dates=['DataNasc'], encoding='iso-8859-1', quotechar='"', delimiter='|'`, onde cada um significa:

- `parse_dates=['DataNasc']`: Fazer a importação da coluna `'DataNasc'` como `data hora`
- `encoding='iso-8859-1'`: Tipo de `encoding` do arquivo sendo lido
- `quotechar='"'`: O caracter usado para denotar o inicio e fim de um item entre aspas
- `delimiter='|'`: delimitador utilizado na escrita do arquivo

Em seguida será printada na tela o `shape` que é de 783x18, ou seja, têm-se 738 linhas (registros), além da linha correspondente ao cabeçalho do arquivo `.csv`, e 18 colunas (recursos).

```python
df = pd.read_csv('desafio-base1/pacientes.csv', parse_dates=['DataNasc'], encoding='iso-8859-1',quotechar='"', delimiter='|')
df.shape
```

#### Vendo os dados

Usando a função `head()` do `pandas` com um argumento `3` nele, podemos dar uma olhada nos primeiros `3` registros da tabela interia.
    
O `.T` significa `Transposição`, desta forma visualizaremos as linhas como colunas e vice-versa.

O método `info()` do `pandas` nos dará um resumo dos dados, uma informação interessante é o tipo de dado de cada recurso.

### Limpando e tratando os dados

Nesta seção iremos realizar a limpeza dos dados.

#### Valores ausentes

Quando utilizamos o método `info()` para ver o resumo dos dados, foi possível ver que muitas colunas tinham muitos dados ausentes, entrentanto, é solicitado na documentação da iClinic que os campos `patient_id` e `name` são obrigatórios, como é possível ver, nas colunas `Código` e `Nome`, que são seus correspondentes, estas são as únicas colunas que não tem valores nulos nos seus registros.

#### Recursos equivalentes

Como comentado anteriormente, é possível ver que muitos dos recursos no arquivo lido possuem uma relação de equivalencia quase direta com os recursos da documentação iClinic, são estes:

- "Código":"patient_id",
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


#### Tratando o recurso "Sexo"
 
Neste recurso precisaremos apenas trocar os caractéres 'M' por 'm' e 'F' por 'f', entretanto, utizaremos um procedimento com `list comprehension` para chegar neste fim. 

É possível ver uns comentários nessa célula, pois foi realizada uma tentativa utilizando os métodos `.astype(str).str.lower()` entretanto, desta forma o valor `NaN` era substituido por uma `string` equivalente, o que podia trazer informação errada na hora de verificar os dados.

Com o código a seguir é possível realizar esta mudança e não mudar o valor simbólico do `NaN`:

```python
df['Sexo'] = ['m' if x == 'M' else 'f' if x == 'F' else np.nan for x in df['Sexo']]

```

#### Tratando o recurso "Estado"

Neste caso, apenas verificaremos se este recurso possui seus registros de forma correta, ou seja só duas letras em maiúscula para cada Estado brasileiro:

```python
teste = df['Estado'].str.contains(r'\b[A-Z]{2}')
print(teste.value_counts())

```

O método `str.contains(r'\b[A-Z]{2}')` retorna `True` se o registro avaliado contem o padrão ou `Regex` indicado e `False` caso contrário, caso o registro for `NaN` o valor permanece inalterado.

Ao aplicar o cógigo acima, obtemos no seguinte resultado `True    632`, e, ao comparar com o resultado dos valores não nulos deste recurso, é possível afirmar que todos os registros estão na forma correta.

Ainda, seria interessante fazer a validação se cada um dos registros possui as siglas que representam um estado brasileiro, pois pode ter acontecido alguma escrita errada na hora de entrar com a informação do paciente.

#### Tratando o recurso "CEP"

É realizado o mapemento dos registros que possuem o caracter '-' para em seguida formatar aqueles onde o valor não for `True`, da seguinte forma:

```python
rows_with_dashes = df['CEP'].str.contains('-')
df['CEP'] = [df['CEP'][i] if x == True else df['CEP'][i][:5]+'-'+df['CEP'][i][5:] if x == False else np.nan for i, x in enumerate(rows_with_dashes)]

```

Repare que os valores `NaN` permanecem inalterados.

#### Tratando o recurso "EstadoCivil"

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

#### Tratando o recurso "Cor"

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

#### Tratando o recurso "Endereco"

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

#### Tratando o recurso "TipoTelefone" e "Telefone"

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
#### Tratando os recursos equivalentes

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

#### Adicionando recursos faltantes

Ainda, pelo modelo `importacao-iclinic/patient.csv` é necessário adicionar algumas colunas faltantes, ou seja, que não foram passadas no documento de entrada, por padrão iremos colocar o valor `NaN` nelas:

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

#### Removendo Recursos repetidos ou não necessários

Aqui, iremos remover os recursos repetidos ou que não são mais necessários, como a seguir:

```python
df =  df.loc[:, ["patient_id","name","birth_date","gender","cpf","rg","rg_issuer","mobile_phone","home_phone","office_phone","email","email_secondary","birth_place","birth_state","zip_code","address","number","complement","neighborhood","city","state","country","picture_filename","ethnicity","marital_status","religion","occupation","education","responsible","cns","died","death_info","nationality","indication","indication_observation","active","receive_email","observation","healthinsurance_pack","patientrelatedness_mother_names","patientrelatedness_father_names","tag_names","tag_physician_id"]]
```

### Escrevendo o arquivo de saída

Como solicitado no desafio, o arquivo de saída será gerado com o conjunto de caracteres UTF-8:

```python
df.to_csv('patient.csv',index=False, encoding='utf-8')
```

___
Jonathan Silva