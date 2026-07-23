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
    paginas=['ALIQUOTA', 'CLAUDETE']
    )

meuExcel.caminho = os.getenv('CAMINHO')
dataframe = meuExcel.carregar_pagina(1) 

for celula, pos in meuExcel.celulas.items():
    pos_pandas = Spreadsheet.excel_para_pandas(pos)
    print(f'{celula}, {pos_pandas} > {dataframe.iloc[pos_pandas[0], pos_pandas[1]]}')
    