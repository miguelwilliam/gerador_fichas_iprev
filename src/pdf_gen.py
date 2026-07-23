import json

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def gerarRelatorio(dados, caminho_pdf):

    with open(dados, 'r', encoding='utf-8') as arquivo:
        funcionarios = json.load(arquivo)

    dados = [["Matrícula", "Nome", "Salário\nEfetivo", "Comiss. /\nF. Grat.", "Total da\nRemuneração", "Remuneração\nde Contribuição", "Contribuição\n Prev. Própria"]]

    #ADICIONAR OS VALORES PARA CADA FUNCIONÁRIO

    for funcionario in funcionarios:
        matricula = funcionario['MATRICULA']
        nome = funcionario['NOME']
        orgao = funcionario['ORGAO']
        base_calc = funcionario['BASE_CALC']
        percentual_segurados = 14/100
        # percentual_patronal = 15.83/100
        segurados = percentual_segurados*base_calc
        # patronal = percentual_patronal*BASE_CALC

        dados.append([orgao, '', '', '', '', ''])

        dados.append([
            matricula,
            nome,
            f"{base_calc:,.2f}",
            f"{base_calc:,.2f}",
            f"{segurados:,.2f}"
        ])

    # ADICIONAR VALORES DE SOMA NO FINAL DA TABELA

    pdf = SimpleDocTemplate(str(caminho_pdf), pagesize=landscape(A4))

    tabela = Table(dados)

    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 2), (-1, 0), "RIGHT"),
        ("ALIGN", (0, 0), (1, 0), "LEFT"),
        ("LINEABOVE", (0, 0), (-1, 0), 1, colors.grey),
        ("LINEABOVE", (0, 1), (-1, 1), 1, colors.grey),

        ("ALIGN", (1, 1), (-1, -1), "LEFT"),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 20)
    ]

    for i in range(len(funcionarios)):
        estilo.append(
            ("SPAN", (0, i*2+1), (-1, i*2+1)),
            ()
        )

    tabela.setStyle(TableStyle(estilo))

    pdf.build([tabela])

    #print("PDF criado com sucesso!")