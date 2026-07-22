import json

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

with open('informacoes.json', 'r', encoding='utf-8') as arquivo:
    funcionarios = json.load(arquivo)

dados = [["Funcionário", "Salário", "Percentual", "Valor Auxílio"]]

for funcionario in funcionarios:
    salario = funcionario['salario']
    percentual = funcionario['percentualAuxilios']
    valor_auxilio = salario * percentual / 100

    dados.append([
        funcionario['nome'],
        f"R$ {salario:,.2f}",
        f"{percentual:.1f}%",
        f"R$ {valor_auxilio:,.2f}"
    ])

pdf = SimpleDocTemplate(f"relatorio_funcionarios_{datetime.now().strftime("%d_%m_%Y")}.pdf", pagesize=A4)

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

print("PDF criado com sucesso!")