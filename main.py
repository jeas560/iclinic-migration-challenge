import pandas

# with open('desafio-base1/agenda.csv', encoding='iso-8859-1') as csv_file:
#     csv_reader = csv.DictReader(csv_file, delimiter='|')
#     print(csv_reader.keys())

df = pandas.read_csv('desafio-base1/agenda.csv', encoding='iso-8859-1',quotechar='"', delimiter='|')
df['CodConvenio']
print(df)   