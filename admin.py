import customtkinter as ctk
from tkinter import messagebox, Toplevel, StringVar, IntVar
from tkinter import ttk
from tkinter.constants import BOTH, END, NO, W, X
from database import conectar
import sqlite3

class AdminInterface:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Administração do Banco de Dados")
        self.janela.geometry("800x600")

        # Cria o Notebook (abas)
        self.notebook = ttk.Notebook(self.janela)
        self.notebook.pack(fill=BOTH, expand=True)

        # Aba de Usuários
        self.frame_usuarios = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.frame_usuarios, text="Usuários")

        # Aba de Contas
        self.frame_contas = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.frame_contas, text="Contas")

        # Aba de Transações
        self.frame_transacoes = ctk.CTkFrame(self.notebook)
        self.notebook.add(self.frame_transacoes, text="Transações")

        # Inicializa as diferentes abas
        self.init_usuarios_tab()
        self.init_contas_tab()
        self.init_transacoes_tab()

        self.janela.mainloop()

    def init_usuarios_tab(self):
        # Treeview para usuários
        self.tree_usuarios = ttk.Treeview(self.frame_usuarios)
        self.tree_usuarios["columns"] = ("ID", "Name", "CPF", "Idade", "Email", "is_admin")
        self.tree_usuarios.column("#0", width=0, stretch=NO)
        self.tree_usuarios.heading("#0", text="", anchor=W)

        for col in self.tree_usuarios["columns"]:
            self.tree_usuarios.column(col, anchor=W, width=100)
            self.tree_usuarios.heading(col, text=col, anchor=W)

        self.tree_usuarios.pack(fill=BOTH, expand=True)

        # Botões para interagir com os dados
        btn_frame = ctk.CTkFrame(self.frame_usuarios)
        btn_frame.pack(fill=X)

        add_btn = ctk.CTkButton(btn_frame, text="Adicionar Usuário", command=self.add_user)
        add_btn.pack(side="left", padx=10, pady=10)

        edit_btn = ctk.CTkButton(btn_frame, text="Editar Usuário", command=self.edit_user)
        edit_btn.pack(side="left", padx=10, pady=10)

        delete_btn = ctk.CTkButton(btn_frame, text="Excluir Usuário", command=self.delete_user)
        delete_btn.pack(side="left", padx=10, pady=10)

        self.load_data_usuarios()

    def load_data_usuarios(self):
        # Limpa a árvore
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Name, CPF, Idade, Email, is_admin FROM Customers")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree_usuarios.insert("", END, values=row)

    def init_contas_tab(self):
        # Treeview para contas
        self.tree_contas = ttk.Treeview(self.frame_contas)
        self.tree_contas["columns"] = ("NumberAccount", "Name", "Balance", "CPF")
        self.tree_contas.column("#0", width=0, stretch=NO)
        self.tree_contas.heading("#0", text="", anchor=W)

        for col in self.tree_contas["columns"]:
            self.tree_contas.column(col, anchor=W, width=100)
            self.tree_contas.heading(col, text=col, anchor=W)

        self.tree_contas.pack(fill=BOTH, expand=True)

        # Botões para interagir com os dados
        btn_frame = ctk.CTkFrame(self.frame_contas)
        btn_frame.pack(fill=X)

        refresh_btn = ctk.CTkButton(btn_frame, text="Atualizar", command=self.load_data_contas)
        refresh_btn.pack(side="left", padx=10, pady=10)

        self.load_data_contas()

    def load_data_contas(self):
        # Limpa a árvore
        for item in self.tree_contas.get_children():
            self.tree_contas.delete(item)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT NumberAccount, Name, Balance, CPF FROM Contas")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree_contas.insert("", END, values=row)

    def init_transacoes_tab(self):
        # Treeview para transações
        self.tree_transacoes = ttk.Treeview(self.frame_transacoes)
        self.tree_transacoes["columns"] = ("ID", "Numero_Conta", "Tipo", "Valor", "Data")
        self.tree_transacoes.column("#0", width=0, stretch=NO)
        self.tree_transacoes.heading("#0", text="", anchor=W)

        for col in self.tree_transacoes["columns"]:
            self.tree_transacoes.column(col, anchor=W, width=100)
            self.tree_transacoes.heading(col, text=col, anchor=W)

        self.tree_transacoes.pack(fill=BOTH, expand=True)

        # Botões para interagir com os dados
        btn_frame = ctk.CTkFrame(self.frame_transacoes)
        btn_frame.pack(fill=X)

        refresh_btn = ctk.CTkButton(btn_frame, text="Atualizar", command=self.load_data_transacoes)
        refresh_btn.pack(side="left", padx=10, pady=10)

        self.load_data_transacoes()

    def load_data_transacoes(self):
        # Limpa a árvore
        for item in self.tree_transacoes.get_children():
            self.tree_transacoes.delete(item)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, numero_conta, tipo, valor, data FROM Transacoes")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree_transacoes.insert("", END, values=row)

    def add_user(self):
        self.user_window = Toplevel(self.janela)
        self.user_window.title("Adicionar Usuário")

        # Labels e entradas para os campos
        labels = ["Nome", "CPF", "Idade", "Email", "Senha", "É Admin (0 ou 1)"]
        self.entries = []

        for idx, label in enumerate(labels):
            lbl = ctk.CTkLabel(self.user_window, text=label)
            lbl.grid(row=idx, column=0, padx=10, pady=5)

            entry = ctk.CTkEntry(self.user_window)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries.append(entry)

        save_btn = ctk.CTkButton(self.user_window, text="Salvar", command=self.save_new_user)
        save_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def save_new_user(self):
        values = [entry.get() for entry in self.entries]
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO Customers (Name, CPF, Idade, Email, Password, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
            """, values)
            conn.commit()
            conn.close()
            self.user_window.destroy()
            self.load_data_usuarios()
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao adicionar usuário: {e}")

    def edit_user(self):
        selected_item = self.tree_usuarios.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Nenhum usuário selecionado.")
            return

        user_values = self.tree_usuarios.item(selected_item)["values"]
        self.user_id = user_values[0]

        self.user_window = Toplevel(self.janela)
        self.user_window.title("Editar Usuário")

        labels = ["Nome", "CPF", "Idade", "Email", "Senha", "É Admin (0 ou 1)"]
        self.entries = []

        for idx, label in enumerate(labels):
            lbl = ctk.CTkLabel(self.user_window, text=label)
            lbl.grid(row=idx, column=0, padx=10, pady=5)

            entry = ctk.CTkEntry(self.user_window)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries.append(entry)

        # Preenche os campos com os valores atuais
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT Name, CPF, Idade, Email, Password, is_admin FROM Customers WHERE ID = ?", (self.user_id,))
        user_data = cursor.fetchone()
        conn.close()

        for idx, value in enumerate(user_data):
            self.entries[idx].insert(0, value)

        save_btn = ctk.CTkButton(self.user_window, text="Atualizar", command=self.update_user)
        save_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_user(self):
        values = [entry.get() for entry in self.entries]
        values.append(self.user_id)  # Adiciona o ID para a cláusula WHERE
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE Customers SET Name = ?, CPF = ?, Idade = ?, Email = ?, Password = ?, is_admin = ?
            WHERE ID = ?
            """, values)
            conn.commit()
            conn.close()
            self.user_window.destroy()
            self.load_data_usuarios()
            messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso.")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar usuário: {e}")

    def delete_user(self):
        selected_item = self.tree_usuarios.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Nenhum usuário selecionado.")
            return

        user_id = self.tree_usuarios.item(selected_item)["values"][0]
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este usuário?")
        if resposta:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Customers WHERE ID = ?", (user_id,))
            conn.commit()
            conn.close()
            self.load_data_usuarios()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")

# Inicialize a interface do administrador apenas se este arquivo for executado diretamente
if __name__ == '__main__':
    AdminInterface()
