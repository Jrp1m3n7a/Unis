import tkinter as tk
from tkinter import ttk
import sqlite3

def calcular_imc():
    try:
        nome = nome_var.get()
        endereco = endereco_var.get()
        altura_cm = float(altura_entry.get())
        altura_m = altura_cm / 100  # Convertendo centímetros para metros
        peso = float(peso_entry.get())
        imc = peso / (altura_m ** 2)
        resultado_var.set(f"{nome}\n{endereco}\nSeu IMC é: {imc:.2f}")

        # Salvar o resultado no banco de dados
        salvar_resultado_banco(nome, endereco, altura_cm, peso, imc)

    except ValueError:
        resultado_var.set("Por favor, insira valores válidos.")

def salvar_resultado_banco(nome, endereco, altura, peso, imc):
    # Conectar ao banco de dados SQLite
    conexao = sqlite3.connect('imc_db.db')
    cursor = conexao.cursor()

    # Inserir dados na tabela 'calculos_imc'
    cursor.execute('''
        INSERT INTO calculos_imc (nome, endereco, altura, peso, imc)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, endereco, altura, peso, imc))

    # Commit e fechar a conexão
    conexao.commit()
    conexao.close()

def reiniciar():
    nome_entry.delete(0, tk.END)
    endereco_entry.delete(0, tk.END)
    altura_entry.delete(0, tk.END)
    peso_entry.delete(0, tk.END)
    resultado_var.set("Resultado do IMC aparecerá aqui")

def exibir_todos_dados():
    # Conectar ao banco de dados SQLite
    conexao = sqlite3.connect('imc_db.db')
    cursor = conexao.cursor()

    # Selecionar todos os dados da tabela 'calculos_imc'
    cursor.execute('SELECT * FROM calculos_imc')
    dados = cursor.fetchall()

    # Criar uma nova janela para exibir os dados em uma tabela
    tabela_window = tk.Toplevel(root)
    tabela_window.title("Dados do IMC")

    # Criar a tabela
    tabela = ttk.Treeview(tabela_window)
    tabela["columns"] = ("ID", "Nome", "Endereço", "Altura", "Peso", "IMC", "Data do Cálculo")

    # Definir cabeçalhos
    for coluna in tabela["columns"]:
        tabela.heading(coluna, text=coluna)

    # Preencher a tabela com os dados
    for dado in dados:
        tabela.insert("", "end", values=dado)

    tabela.pack()

    # Fechar a conexão
    conexao.close()

def sair():
    root.destroy()

# Criar tabela se não existir
def criar_tabela():
    conexao = sqlite3.connect('imc_db.db')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calculos_imc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT,
            altura REAL NOT NULL,
            peso REAL NOT NULL,
            imc REAL NOT NULL,
            data_calculo DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conexao.commit()
    conexao.close()

# Iniciar a aplicação
root = tk.Tk()
root.title("Cálculo do IMC - Índice de Massa Corporal")

# Criar tabela antes de iniciar a aplicação
criar_tabela()

# Restante do código permanece o mesmo
nome_var = tk.StringVar()
endereco_var = tk.StringVar()
altura_var = tk.StringVar()
peso_var = tk.StringVar()
resultado_var = tk.StringVar()
resultado_var.set("Resultado do IMC aparecerá aqui")

nome_label = tk.Label(root, text="Nome do paciente:")
nome_entry = tk.Entry(root, textvariable=nome_var)
nome_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
nome_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=5, sticky="we")

endereco_label = tk.Label(root, text="Endereço Completo:")
endereco_entry = tk.Entry(root, textvariable=endereco_var)
endereco_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
endereco_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="we")

altura_label = tk.Label(root, text="Altura (cm):")
altura_entry = tk.Entry(root, textvariable=altura_var)
altura_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
altura_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

peso_label = tk.Label(root, text="Peso (kg):")
peso_entry = tk.Entry(root, textvariable=peso_var)
peso_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
peso_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

resultado_label = tk.Label(root, textvariable=resultado_var, font=('Arial', 12), justify="left")
resultado_label.grid(row=2, column=2, rowspan=2, columnspan=2, padx=10, pady=5, sticky="nsew")

calcular_button = tk.Button(root, text="Calcular", command=calcular_imc)
calcular_button.grid(row=4, column=0, columnspan=2, pady=10, padx=(10, 0), sticky="we")

reiniciar_button = tk.Button(root, text="Reiniciar", command=reiniciar)
reiniciar_button.grid(row=5, column=0, columnspan=2, pady=5, padx=(10, 0), sticky="we")

exibir_button = tk.Button(root, text="Exibir Dados", command=exibir_todos_dados)
exibir_button.grid(row=5, column=2, columnspan=2, pady=5, padx=(10, 0), sticky="we")

sair_button = tk.Button(root, text="Sair", command=sair)
sair_button.grid(row=6, column=3, pady=5, padx=(0, 10), sticky="e")

root.grid_columnconfigure(0, weight=1)

root.mainloop()
