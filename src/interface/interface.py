import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
from pathlib import Path

from src.pdf.pdf_gen import gerarGuia
from src.my_classes.spreadsheet import Spreadsheet, ESTRUTURA

class ExcelToPDFGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Excel para PDF")
        self.root.geometry("600x250")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        # Arquivo Excel
        tk.Label(self.root, text="Arquivo Excel:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        self.excel_path = tk.StringVar()

        tk.Entry(
            self.root,
            textvariable=self.excel_path,
            width=55
        ).grid(row=0, column=1)

        tk.Button(
            self.root,
            text="Selecionar",
            command=self.select_excel
        ).grid(row=0, column=2, padx=5)

        # Nome da planilha
        tk.Label(self.root, text="Planilha:").grid(row=1, column=0, padx=10, pady=10)

        self.combo_sheet = ttk.Combobox(
            self.root,
            state="readonly",
            width=40
        )

        self.combo_sheet.grid(row=1, column=1, sticky="w")

        '''tk.Label(self.root, text="Nome da planilha:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )

        self.sheet_name = tk.StringVar()

        tk.Entry(
            self.root,
            textvariable=self.sheet_name,
            width=30
        ).grid(row=1, column=1, sticky="w")'''

        # Nome do PDF
        tk.Label(self.root, text="Nome do PDF:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )

        self.pdf_name = tk.StringVar()

        tk.Entry(
            self.root,
            textvariable=self.pdf_name,
            width=30
        ).grid(row=2, column=1, sticky="w")

        # Pasta de saída
        tk.Label(self.root, text="Pasta de saída:").grid(
            row=3, column=0, padx=10, pady=10, sticky="w"
        )

        self.output_path = tk.StringVar()

        tk.Entry(
            self.root,
            textvariable=self.output_path,
            width=55
        ).grid(row=3, column=1)

        tk.Button(
            self.root,
            text="Selecionar",
            command=self.select_output
        ).grid(row=3, column=2, padx=5)

        # Botão principal
        tk.Button(
            self.root,
            text="Converter",
            width=20,
            command=self.convert
        ).grid(row=4, column=1, pady=25)

    def select_excel(self):
        filename = filedialog.askopenfilename(
            title="Selecione um arquivo Excel",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls")]
        )

        if not filename:
            return

        self.excel_path.set(filename)

        xls = pd.ExcelFile(filename)

        self.combo_sheet["values"] = xls.sheet_names

        if xls.sheet_names:
            self.combo_sheet.current(0)

    def select_output(self):
        folder = filedialog.askdirectory(
            title="Selecione a pasta de saída"
        )

        if folder:
            self.output_path.set(folder)

    def convert(self):

        excel = self.excel_path.get().strip()
        sheet = self.combo_sheet.get()
        pdf = self.pdf_name.get().strip()
        output = self.output_path.get().strip()

        if not excel:
            messagebox.showerror("Erro", "Selecione um arquivo Excel.")
            return

        if not sheet:
            messagebox.showerror("Erro", "Informe o nome da planilha.")
            return

        if not pdf:
            messagebox.showerror("Erro", "Informe o nome do PDF.")
            return

        if not output:
            messagebox.showerror("Erro", "Selecione a pasta de saída.")
            return

        pdf_path = Path(output) / f"{pdf}.pdf"

        # ==================================================
        # Coloque aqui sua lógica de conversão Excel -> PDF
        # ==================================================
        
        meuExcel = Spreadsheet(ESTRUTURA['CELULAS'], ESTRUTURA['LINHAS'], paginas=pd.ExcelFile(excel).sheet_names)
        meuExcel.caminho = excel
        df = meuExcel.carregar_pagina(sheet)
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

        sucesso = gerarGuia(dados, pdf_path)
        print('SUCESSO:',sucesso)


        messagebox.showinfo(
            "Dados informados",
            f"""Excel:
{excel}

Planilha:
{sheet}

PDF:
{pdf_path}
"""
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ExcelToPDFGUI()
    app.run()