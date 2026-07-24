import json

from datetime import datetime

from spreadsheet import Spreadsheet

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

styles = getSampleStyleSheet()

def gerarRelatorio(dados, caminho_pdf):
    try:
        tabelas = []

        # GERANDO IDENTIFICADOR (FC/FR)
        admissao = datetime.strptime(dados['ADMISSAO'], '%d/%m/%Y')
        if admissao < datetime.strptime('31/12/2012', '%d/%m/%Y') or admissao > datetime.strptime('01/01/2025', '%d/%m/%Y'):
            identificador = 'FR - IPREV'
        else:
            identificador = 'FC - IPREV'

        estiloParagrafo1 = ParagraphStyle(
            "Compacto",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,          # espaçamento entre linhas
            wordWrap="LTR",     # quebra de linha normal
        )
        estiloParagrafo2 = ParagraphStyle(
            "Compacto",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9,          # espaçamento entre linhas
            wordWrap="LTR",     # quebra de linha normal
            alignment=TA_CENTER
        )
        estiloParagrafo3 = ParagraphStyle(
            "Compacto",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=9,          # espaçamento entre linhas
            wordWrap="LTR",     # quebra de linha normal
            alignment=TA_CENTER
        )
        estiloTabela = [
            ('FONTSIZE', (0, 0), (-1, -1), 7.5),
            ('FONTNAME', (0, 0), (0, 2), 'Helvetica-Bold'),
            #('GRID', (0, 0), (-1, -1), 1, colors.black),

            # RETIRANDO CERTAS BORDAS:
            # ('BOX', (0, 0), (-1, -1), 1, colors.black), # não necessário
            ('BOX', (0, 0), (1, 2), 1, colors.black),
            ('GRID', (2, 0), (-1, -1), 1, colors.black),
            ('BOX', (0, 3), (1, 6), 1, colors.black),
            ('GRID', (0, 7), (1, 10), 1, colors.black),
            ('BOX', (0, 11), (1, -1), 1, colors.black),

            # ALINHAMENTO :
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (2, 10), (2, 10), 'TOP'), # exceção, por algum motivo

            ('SPAN', (0, 0), (1,0)),
            ('SPAN', (0, 1), (1,1)),
            ('SPAN', (0, 2), (1,2)),
            ('SPAN', (0, 3), (1,3)),
            ('SPAN', (0, 4), (1,4)),
            ('SPAN', (0, 5), (1,5)),
            ('SPAN', (0, 6), (1,6)),
            ('SPAN', (0, 8), (1,9)),
            ('SPAN', (0, 10), (1,10)),
            ('SPAN', (0, 11), (1,11)),
            ('SPAN', (0, 12), (1,12)),
            ('SPAN', (0, 13), (1,13)),
            ('SPAN', (2, 10), (-1, -1))
        ]
        
        for i in range(len(dados)-3):
            i = str(i+1)

            multa = 0
            
            dados_tabela = [
                [Paragraph('INST. PREVIDÊNCIA DE SÃO GONÇALO DO AMARANTE', estiloParagrafo2), '', '3. BASE DE CÁLCULO', f'R$ {dados[i]['BASE_CALC']:,.2f}'],
                [Paragraph('INSTITUTO DE PREVIDENCIA DOS SERVIDORES DO MUNICIPIO DE SÃO GONÇALO DO AMARANTE - RN', estiloParagrafo2), '', '4. COMPETÊNCIA', f'{dados[i]['COMPETENCIA']}'],
                [Paragraph('GUIA DA PREVIDÊNCIA PRÓPRIA - GPP', estiloParagrafo3), '', '5. IDENTIFICADOR', identificador],
                ['1. NOME OU RAZÃO SOCIAL/ FONE/ ENDEREÇO:', '', '6. SEGURADO (14%)', f'R$ {dados[i]['IPREV']:,.2f}'],
                [Paragraph('INST. PREVIDÊNCIA DE SÃO GONÇALO DO AMARANTE CNPJ: 11.447.510/0001-28', estiloParagrafo1), '', '7. PATRONAL (15,83%)', f'R$ {dados[i]['PATRONAL']:,.2f}'],
                [Paragraph('R Maria de Fátima Varela Inácio, 61 - Santa Terezinha', estiloParagrafo1), '', '8. CONTRIBUIÇÃO PAT.\nSUPLEMENTAR (7,98%)', 'R$ -'],
                [f'{dados['ORGAO']}', '', '9. (-) DEDUÇÕES', 'R$ -'],
                ['2. VENCIMENTO\n(Uso do IPREV)', 'DIA 10 DO MÊS SEGUINTE À COMPETÊNCIA', '10. VALOR IPREV', f'R$ {(dados[i]['IPREV'] + dados[i]['PATRONAL']):,.2f}'],
                [Paragraph('ATENÇÃO: É vedada a utilização de GPP para recolhimento de receita de valor inferior ao estipulado em Resolução publicada pelo IPREV. A receita que resultar valor inferior deverá ser adicionada à contribuição ou importância correspondente nos meses subsequentes, até que o total seja igual ou superior ao valor mínimo fixado.', estiloParagrafo1), '', '11. ATM, MULTA E JUROS', 'À DEFINIR!!'],
                ['', '', '12. TOTAL', f'R$ {(dados[i]['IPREV'] + dados[i]['PATRONAL'] + multa):,.2f}'],
                [Paragraph(f'GUIA REFERENTE A CESSÃO DO SERVIDOR {dados['NOME']}', estiloParagrafo1), '', '13. AUTENTICAÇÃO BANCÁRIA', ''],
                ['Banco do Brasil: 001', '', '', ''],
                ['Agência: 4486-5', '', '', ''],
                ['Conta Corrente: 31.651-2', '', '', '']
            ]

            tabela = Table(dados_tabela, colWidths=[100,300,100,100])
            
            
    
            tabela.setStyle(TableStyle(estiloTabela))

            tabelas.append(tabela)


        # ADICIONAR OS VALORES PARA CADA FUNCIONÁRIO


        # ADICIONAR VALORES DE SOMA NO FINAL DA TABELA

        pdf = SimpleDocTemplate(str(caminho_pdf), pagesize=landscape(A4))

        pdf.build(tabelas)

        print("PDF criado com sucesso!")
        return True
    
    except Exception as e:
        print(f'ERRO EM GERAR O RELATÓRIO:\n{e}')
        return False