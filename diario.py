import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
import os
import shutil

# Banco de Dados
conn = sqlite3.connect('diario.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        titulo TEXT,
        categoria TEXT,
        conteudo TEXT
    )
''')
conn.commit()

# Funções
def adicionar_registro():
    data = datetime.date.today().strftime('%Y-%m-%d')
    titulo = simpledialog.askstring("Título", "Digite o título:")
    categoria = simpledialog.askstring("Categoria", "Digite a categoria:")
    conteudo = simpledialog.askstring("Conteúdo", "Digite o conteúdo do registro:")

    if titulo and conteudo:
        cursor.execute('INSERT INTO registros (data, titulo, categoria, conteudo) VALUES (?, ?, ?, ?)',
                       (data, titulo, categoria, conteudo))
        conn.commit()
        messagebox.showinfo("Sucesso", "Registro salvo com sucesso!")

def visualizar_registros():
    registros = cursor.execute('SELECT * FROM registros').fetchall()
    output = ""
    for reg in registros:
        output += f"ID: {reg[0]}\nData: {reg[1]}\nTítulo: {reg[2]}\nCategoria: {reg[3]}\nConteúdo: {reg[4]}\n{'-'*40}\n"
    messagebox.showinfo("Registros", output if output else "Nenhum registro encontrado.")

def buscar_por_palavra():
    palavra = simpledialog.askstring("Buscar", "Digite a palavra-chave:")
    registros = cursor.execute('SELECT * FROM registros WHERE conteudo LIKE ?', (f'%{palavra}%',)).fetchall()
    output = ""
    for reg in registros:
        output += f"ID: {reg[0]}\nData: {reg[1]}\nTítulo: {reg[2]}\nCategoria: {reg[3]}\nConteúdo: {reg[4]}\n{'-'*40}\n"
    messagebox.showinfo("Busca", output if output else "Nenhum registro encontrado.")

def visualizar_por_data():
    data = simpledialog.askstring("Data", "Digite a data (AAAA-MM-DD):")
    registros = cursor.execute('SELECT * FROM registros WHERE data = ?', (data,)).fetchall()
    output = ""
    for reg in registros:
        output += f"ID: {reg[0]}\nTítulo: {reg[2]}\nCategoria: {reg[3]}\nConteúdo: {reg[4]}\n{'-'*40}\n"
    messagebox.showinfo("Registros na data", output if output else "Nenhum registro encontrado para essa data.")

def excluir_registro():
    id_registro = simpledialog.askinteger("Excluir", "Digite o ID do registro para excluir:")
    cursor.execute('DELETE FROM registros WHERE id = ?', (id_registro,))
    conn.commit()
    messagebox.showinfo("Exclusão", "Registro excluído com sucesso!")

def backup_dados():
    if not os.path.exists('backup'):
        os.makedirs('backup')
    shutil.copy('diario.db', f'backup/diario_backup_{datetime.date.today()}.db')
    messagebox.showinfo("Backup", "Backup realizado com sucesso!")

# Interface Gráfica
root = tk.Tk()
root.title("Diário Digital")

root.configure(bg="#222222")
style = ttk.Style(root)
style.theme_use("clam")
style.configure('TButton', background="#444444", foreground="white", padding=6)
style.configure('TLabel', background="#222222", foreground="white")

tk.Label(root, text="Diário Digital", font=("Arial", 18), bg="#222222", fg="white").pack(pady=10)

ttk.Button(root, text="Adicionar Registro", command=adicionar_registro).pack(pady=5)
ttk.Button(root, text="Visualizar Registros", command=visualizar_registros).pack(pady=5)
ttk.Button(root, text="Buscar por Palavra", command=buscar_por_palavra).pack(pady=5)
ttk.Button(root, text="Visualizar por Data", command=visualizar_por_data).pack(pady=5)
ttk.Button(root, text="Excluir Registro", command=excluir_registro).pack(pady=5)
ttk.Button(root, text="Fazer Backup", command=backup_dados).pack(pady=5)

root.mainloop()
