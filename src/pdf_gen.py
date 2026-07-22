import json

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def gerarRelatorio(dados_json, caminho_pdf):

    with open(dados_json, 'r', encoding='utf-8') as arquivo:
        funcionarios = json.load(arquivo)

    dados = [["Matrícula", "Nome", "Salário\nEfetivo", "Comiss. /\nF. Grat.", "Total da\nRemuneração", "Remuneração\nde Contribuição", "Contribuição\n Prev. Própria"]]

    #ADICIONAR OS VALORES PARA CADA FUNCIONÁRIO

    for funcionario in funcionarios:
        matricula = funcionario['MATRICULA']
        nome = funcionario['NOME']
        instituicao = funcionario['INSTITUICAO']
        salario_efetivo = funcionario['SALARIO_EFETIVO']
        gratificacao = funcionario['GRATIFICACAO']
        total_remuneracao = salario_efetivo + gratificacao
        percentual_segurados = 14/100
        percentual_patronal = 15.83/100
        segurados = percentual_segurados*salario_efetivo
        patronal = percentual_patronal*salario_efetivo

        dados.append(['', instituicao, '', '', '', '', ''])

        dados.append([
            matricula,
            nome,
            f"{salario_efetivo:,.2f}",
            f"{gratificacao:,.2f}",
            f"{total_remuneracao:,.2f}",
            f"{salario_efetivo:,.2f}",
            f"{segurados:,.2f}"
        ])

    # ADICIONAR VALORES DE SOMA NO FINAL DA TABELA

    pdf = SimpleDocTemplate(str(caminho_pdf), pagesize=landscape(A4))

    tabela = Table(dados)

    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.antiquewhite),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),

        ("ALIGN", (1, 1), (-1, -1), "LEFT"),

        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.lightgrey]),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 12)
    ]))

    pdf.build([tabela])

    #print("PDF criado com sucesso!")