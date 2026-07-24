import os
from dotenv import load_dotenv

from spreadsheet import Spreadsheet
from pdf_gen import gerarRelatorio

load_dotenv()

estrutura = {
    'CELULAS': 
    {
        'NOME': 'A1',
        'ORGAO': 'B3',
    },

    'LINHAS': 
    {
        'COMPETENCIA': 5,
        'BASE_CALC': 8,
        'IPREV': 9,
        'PATRONAL': 13
    }
}

meuExcel = Spreadsheet(
    celulas=estrutura['CELULAS'], 
    linhas=estrutura['LINHAS'], 
    paginas=['ALIQUOTA', 'CLAUDETE', 'JUNIOR']
    )

meuExcel.caminho = os.getenv('CAMINHO')
df = meuExcel.carregar_pagina(1) 


# Bloco de teste de leitura do excel:
'''
for celula, pos in meuExcel.celulas.items():
    pos_pandas = Spreadsheet.excel_para_pandas(pos)

    # Para extrair o nome da célula
    if celula == 'NOME':
        dados = str(df.iloc[pos_pandas[0], pos_pandas[1]]).split(' - ')
        print(f'NOME, {pos_pandas} > {dados[0]}')
        print(f'DATA DE ADMISSÃO, {pos_pandas} > {dados[1]}')
        continue

    print(f'{celula}, {pos_pandas} > {df.iloc[pos_pandas[0], pos_pandas[1]]}')

for col in range(len(df.columns)):
    if col == 0: continue

    print('==================')
    for dado, linha in meuExcel.linhas.items():
        pos_pandas = [linha-1, col]
        
        # print(f'{dado}, ({linha-1}, {col}) > {df.iloc[pos_pandas[0], pos_pandas[1]]}')
        print(f'{dado} > {df.iloc[pos_pandas[0], pos_pandas[1]]}')
'''

# Teste com formatação de dados no python

dados = {}

for celula, pos in meuExcel.celulas.items():
    pos_pandas = Spreadsheet.excel_para_pandas(pos)

    # Para extrair o nome da célula
    if celula == 'NOME':
        dados_excel = str(df.iloc[pos_pandas[0], pos_pandas[1]]).split(' - ')
        dados['NOME'] = dados_excel[0]
        dados['ADMISSAO'] = dados_excel[1].split(' ')[1]
        continue

    dados[str(celula)] = df.iloc[pos_pandas[0], pos_pandas[1]]

for col in range(len(df.columns)):
    if col == 0: continue

    dados[str(col)] = {}

    for dado, linha in meuExcel.linhas.items():
        pos_pandas = [linha-1, col]
        
        # print(f'{dado}, ({linha-1}, {col}) > {df.iloc[pos_pandas[0], pos_pandas[1]]}')
        # print(f'{dado} > {df.iloc[pos_pandas[0], pos_pandas[1]]}')
        dados[str(col)][dado] = df.iloc[pos_pandas[0], pos_pandas[1]]

for chave, valor in dados.items(): print(f'{chave} > {valor}')

gerarRelatorio(dados, r'./relatorio_teste.pdf')