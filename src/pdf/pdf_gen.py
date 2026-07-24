from datetime import datetime

from src.my_classes.spreadsheet import Spreadsheet
from src.styles import my_styles
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak, HRFlowable



def gerarRelatorio(dados, caminho_pdf):
    try:
        story = []

        # GERANDO IDENTIFICADOR (FC/FR)
        admissao = datetime.strptime(dados['ADMISSAO'], '%d/%m/%Y')
        if admissao < datetime.strptime('31/12/2012', '%d/%m/%Y') or admissao > datetime.strptime('01/01/2025', '%d/%m/%Y'):
            identificador = 'FR - IPREV'
        else:
            identificador = 'FC - IPREV'

        for i in range(len(dados)-3):
            i = str(i+1)

            multa = 0
            
            dados_tabela = [
                [Paragraph('INST. PREVIDÊNCIA DE SÃO GONÇALO DO AMARANTE', my_styles.estiloParagrafo2), '', '3. BASE DE CÁLCULO', f'R$ {dados[i]['BASE_CALC']:,.2f}'],
                [Paragraph('INSTITUTO DE PREVIDENCIA DOS SERVIDORES DO MUNICIPIO DE SÃO GONÇALO DO AMARANTE - RN', my_styles.estiloParagrafo2), '', '4. COMPETÊNCIA', f'{dados[i]['COMPETENCIA']}'],
                [Paragraph('GUIA DA PREVIDÊNCIA PRÓPRIA - GPP', my_styles.estiloParagrafo3), '', '5. IDENTIFICADOR', identificador],
                ['1. NOME OU RAZÃO SOCIAL/ FONE/ ENDEREÇO:', '', '6. SEGURADO (14%)', f'R$ {dados[i]['IPREV']:,.2f}'],
                [Paragraph('INST. PREVIDÊNCIA DE SÃO GONÇALO DO AMARANTE CNPJ: 11.447.510/0001-28', my_styles.estiloParagrafo1), '', '7. PATRONAL (15,83%)', f'R$ {dados[i]['PATRONAL']:,.2f}'],
                [Paragraph('R Maria de Fátima Varela Inácio, 61 - Santa Terezinha', my_styles.estiloParagrafo1), '', '8. CONTRIBUIÇÃO PAT.\nSUPLEMENTAR (7,98%)', 'R$ -'],
                [f'{dados['ORGAO']}', '', '9. (-) DEDUÇÕES', 'R$ -'],
                ['2. VENCIMENTO\n(Uso do IPREV)', Paragraph('<i>DIA 10 DO MÊS SEGUINTE À COMPETÊNCIA</i>', my_styles.estiloParagrafo1), '10. VALOR IPREV', f'R$ {(dados[i]['IPREV'] + dados[i]['PATRONAL']):,.2f}'],
                [Paragraph('<b>ATENÇÃO:</b> É vedada a utilização de GPP para recolhimento de receita de valor inferior ao estipulado em Resolução publicada pelo IPREV. A receita que resultar valor inferior deverá ser adicionada à contribuição ou importância correspondente nos meses subsequentes, até que o total seja igual ou superior ao valor mínimo fixado.', my_styles.estiloParagrafo1), '', '11. ATM, MULTA\nE JUROS', 'À DEFINIR!!'],
                ['', '', '12. TOTAL', f'R$ {(dados[i]['IPREV'] + dados[i]['PATRONAL'] + multa):,.2f}'],
                [Paragraph(f'GUIA REFERENTE A CESSÃO DO SERVIDOR {dados['NOME']}', my_styles.estiloParagrafo1), '', '13. AUTENTICAÇÃO BANCÁRIA', ''],
                ['Banco do Brasil: 001', '', '', ''],
                ['Agência: 4486-5', '', '', ''],
                ['Conta Corrente: 31.651-2', '', '', '']
            ]

            tabela = Table(dados_tabela, colWidths=[95,285,95,95])
    
            tabela.setStyle(TableStyle(my_styles.estiloTabela))

            story.append(tabela)
            story.append(HRFlowable(width="100%", thickness=1, color="black", spaceBefore=30, spaceAfter=30))
            story.append(tabela)
            story.append(PageBreak())


        # ADICIONAR OS VALORES PARA CADA FUNCIONÁRIO


        # ADICIONAR VALORES DE SOMA NO FINAL DA TABELA

        pdf = SimpleDocTemplate(str(caminho_pdf), pagesize=A4)

        pdf.build(story)

        print("PDF criado com sucesso!")
        return True
    
    except Exception as e:
        print(f'ERRO EM GERAR O RELATÓRIO:\n{e}')
        return False