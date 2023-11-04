import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import os

# Função para adicionar valores para a data selecionada e ao arquivo de relatório
def adicionar_valor():
    data = data_combobox.get()
    valor = valor_entry.get()
    
    if data and valor:
        if not validar_formato_data(data):
            messagebox.showwarning("Formato de Data Inválido", "O formato da data deve ser dd/mm/yyyy.")
            return
        
        # Substitua vírgulas por pontos e converta para um número de ponto flutuante
        valor = float(valor.replace(',', '.'))
        
        adicionar_valor_arquivo(data, valor)
        valor_entry.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Valor adicionado com sucesso!")

# Função para adicionar valores ao arquivo de relatório
def adicionar_valor_arquivo(data, valor):
    arquivo_nome = f"contas_{data.replace('/', '-')}.txt"
    
    if not os.path.exists(arquivo_nome):
        # Se o arquivo não existir, crie-o com um cabeçalho
        with open(arquivo_nome, "w") as file:
            file.write("-------------Relatório-------------\n")
    
    with open(arquivo_nome, "a") as file:
        file.write(f"Valor: R${valor:.2f}\n")

# Função para gerar o relatório do dia, incluindo a soma dos valores
def gerar_contas():
    data_selecionada = data_combobox.get()
    
    if not validar_formato_data(data_selecionada):
        messagebox.showwarning("Formato de Data Inválido", "O formato da data deve ser dd/mm/yyyy.")
        return
    
    valores = ler_valores_do_dia(data_selecionada)
    
    if not valores:
        messagebox.showwarning("Nenhum Valor", "Nenhum valor para a data selecionada.")
        return
    
    arquivo_nome = f"contas_{data_selecionada.replace('/', '-')}.txt"
    
    with open(arquivo_nome, "a") as file:
        # Calcule e adicione a soma dos valores ao final do arquivo
        soma = sum(valores)
        file.write(f"-------------------------------------\nSoma dos Valores do Dia: R${soma:.2f}\n-------------------------------------\n")
        
    messagebox.showinfo("Relatório Gerado", f"O relatório para {data_selecionada} foi gerado com sucesso!")

# Função para ler os valores de um dia a partir do arquivo
def ler_valores_do_dia(data):
    arquivo_nome = f"contas_{data.replace('/', '-')}.txt"
    valores = []
    
    if os.path.exists(arquivo_nome):
        with open(arquivo_nome, "r") as file:
            for linha in file:
                if linha.startswith("Valor: R$"):
                    valor = float(linha.split("R$")[1].strip())
                    valores.append(valor)
    
    return valores

# Função para validar o formato da data
def validar_formato_data(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False

# Cria a janela principal
root = tk.Tk()
root.title("Sistema de Caixa")

# Maximiza a janela
root.state('zoomed')

# Configura uma fonte maior para rótulos e entradas
fonte = ('Helvetica', 28)  # Família da fonte e tamanho

# Cria e posiciona um quadro (frame) para centralizar verticalmente e horizontalmente
frame = tk.Frame(root)
frame.pack(expand=True, fill='both', padx=20, pady=20)

# Cria e posiciona os widgets dentro do quadro
data_label = tk.Label(frame, text="Escolha uma data:", font=fonte)
data_label.pack(pady=10)

data_combobox = ttk.Combobox(frame, values=[""], font=fonte)
data_combobox.pack(pady=10)

valor_label = tk.Label(frame, text="Valor da Compra:", font=fonte)
valor_label.pack(pady=10)

valor_entry = tk.Entry(frame, font=fonte)
valor_entry.pack(pady=10)

adicionar_button = tk.Button(frame, text="Adicionar Valor", font=fonte, command=adicionar_valor)
adicionar_button.pack(pady=10)

gerar_contas_button = tk.Button(frame, text="Gerar Relatório do Dia", font=fonte, command=gerar_contas)
gerar_contas_button.pack(pady=10)

# Inicializa o valor padrão do Combobox com a data atual
data_combobox.set(datetime.now().strftime('%d/%m/%Y'))

# Inicia o loop principal da interface gráfica
root.mainloop()
