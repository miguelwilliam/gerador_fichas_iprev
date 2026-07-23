import os
from dotenv import load_dotenv

from spreadsheet import Spreadsheet

load_dotenv()

estrutura = {
    'CELULAS': 
    {
        'NOME': 'A1',
        'ORGAO': 'B3',
    },

    'LINHAS': 
    {
        'MESES': 5,
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

for celula, pos in meuExcel.celulas.items():
    pos_pandas = Spreadsheet.excel_para_pandas(pos)

    # Para extrair o nome da célula
    if celula == 'NOME':
        nome = str(df.iloc[pos_pandas[0], pos_pandas[1]]).split(' - ')[0]
        print(f'{celula}, {pos_pandas} > {nome}') 
        continue

    print(f'{celula}, {pos_pandas} > {df.iloc[pos_pandas[0], pos_pandas[1]]}')

for col in range(len(df.columns)):
    if col == 0: continue

    print('==================')
    for dado, linha in meuExcel.linhas.items():
        pos_pandas = [linha-1, col]
        
        # print(f'{dado}, ({linha-1}, {col}) > {df.iloc[pos_pandas[0], pos_pandas[1]]}')
        print(f'{dado} > {df.iloc[pos_pandas[0], pos_pandas[1]]}')