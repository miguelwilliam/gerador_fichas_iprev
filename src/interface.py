import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from pdf_gen import gerarRelatorio

from datetime import datetime

janela = tk.Tk()
janela.title("Gerador de relatório")
janela.geometry("650x220")

arquivo_json = tk.StringVar()
nome_pdf = tk.StringVar(value='relatório')
pasta_saida = tk.StringVar()


def selecionar_json():
    arquivo = filedialog.askopenfilename(
        title='Selecione o arquivo JSON',
        filetypes=[('Arquivos JSON', '*.json')]
    )

    if arquivo:
        arquivo_json.set(arquivo)

def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione a pasta de saída")

    if pasta:
        pasta_saida.set(pasta)

def gerar():
    if not arquivo_json.get():
        messagebox.showerror('Erro', 'Selecione um arquivo JSON.')
        return

    if not nome_pdf.get():
        messagebox.showerror('Erro', 'Informe o nome do PDF.')
        return

    if not pasta_saida.get():
        messagebox.showerror('Erro', 'Informe um caminho de saída.')
        return

    caminho_pdf = Path(pasta_saida.get()) / f"{nome_pdf.get()}{datetime.now().strftime("%d_%m_%Y")}.pdf"

    gerarRelatorio(dados=arquivo_json.get(), caminho_pdf=caminho_pdf)

    messagebox.showinfo(
        "Sucesso",
        f"O PDF será salvo em:\n\n{caminho_pdf}"
    )

# Linha 1
tk.Label(janela, text="Arquivo JSON").grid(row=0, column=0, padx=10, pady=10, sticky="w")

tk.Entry(janela, textvariable=arquivo_json, width=55).grid(row=0, column=1)

tk.Button(janela, text="Selecionar", command=selecionar_json).grid(row=0, column=2, padx=10)

# Linha 2
tk.Label(janela, text="Nome do PDF").grid(row=1, column=0, padx=10, pady=10, sticky="w")

tk.Entry(janela, textvariable=nome_pdf, width=30).grid(row=1, column=1, sticky="w")

# Linha 3
tk.Label(janela, text="Pasta de saída").grid(row=2, column=0, padx=10, pady=10, sticky="w")

tk.Entry(janela, textvariable=pasta_saida, width=55).grid(row=2, column=1)

tk.Button(janela, text="Selecionar", command=selecionar_pasta).grid(row=2, column=2, padx=10)

# Botão
tk.Button(
    janela,
    text="Gerar PDF",
    command=gerar,
    width=20,
    height=2
).grid(row=3, column=0, columnspan=3, pady=20)

janela.mainloop()