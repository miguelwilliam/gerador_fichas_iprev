from src.interface import interface
from src.testes import testes

def main():
    app = interface.ExcelToPDFGUI()
    app.run()
    
    #myExcel, df = testes.carregarPlanilha()
    #testes.teste_gerar_documento(myExcel, df)

if __name__ == "__main__":
    main()