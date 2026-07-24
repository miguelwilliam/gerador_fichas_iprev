from src.testes import testes

def main():
    meuExcel, df = testes.carregarPlanilha()
    testes.teste_gerar_documento(meuExcel, df)

if __name__ == "__main__":
    main()