from tkinter import *
from tkinter import messagebox, simpledialog
import customtkinter as ctk
from tkinter import ttk
from tkinter import Toplevel, StringVar
from tkinter import ttk
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
import random
from database import obter_saldo_db, atualizar_saldo_db,conectar, verificar_login_nome_saldo_conta



# Classe Conta utilizando o banco de dados
class Conta:
    def __init__(self, numero, saldo, titular):
        self.numero = numero
        self.saldo = saldo
        self.titular = titular


    def registrar_transacao(self, tipo, valor):
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO Transacoes (numero_conta, tipo, valor)
        VALUES (?, ?, ?)
        """, (self.numero, tipo, valor))
        
        conn.commit()
        conn.close()


    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            atualizar_saldo_db(self.numero, self.saldo)
            self.registrar_transacao('DEPOSITO', valor)
            return f'Depósito de R${valor:.2f} realizado com sucesso! Saldo atual: R${self.saldo:.2f}'
        else:
            return 'Deposite um valor positivo!'

    def sacar(self, valor):
        if valor > self.saldo or valor < 0:
            return "Valor para saque inválido!"
        else:
            self.saldo -= valor
            atualizar_saldo_db(self.numero, self.saldo)
            self.registrar_transacao('SAQUE', -valor)
            return f'Saque de R${valor:.2f} realizado com sucesso! Saldo atual: R${self.saldo:.2f}'
        
    def obter_extrato_transacoes(self):
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT tipo, valor, data
        FROM Transacoes
        WHERE numero_conta = ?
        ORDER BY data DESC
        """, (self.numero,))
        
        transacoes = cursor.fetchall()
        conn.close()
        
        extrato_str = f"Extrato de transações da conta {self.numero}:\n"
        for tipo, valor, data in transacoes:
            tipo_transacao = 'Crédito' if valor > 0 else 'Débito'
            extrato_str += f"{data} - {tipo} - {tipo_transacao}: R${abs(valor):.2f}\n"
        extrato_str += f"Saldo atual: R${self.saldo:.2f}"
        
        return extrato_str


    
    
# Classe Sistema utilizando tkinter e interagindo com o banco de dados
class Sistema:
    def __init__(self, nome, saldo, numero_conta,email,cpf,password):
        self.nome = nome
        self.saldo = saldo
        self.email = email
        self.cpf = cpf
        self.password = password  
        self.conta = Conta(numero=numero_conta, saldo=saldo, titular=nome)
        self.janela = ctk.CTk()
        self.tema()
        self.tela()
        self.tela_app()
        self.tela_inicio()
        self.janela.mainloop()

    def tema(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def tela(self):
        self.janela.geometry("700x500")
        self.janela.title("Banco Meyer")
        self.janela.resizable(False, False)

    def tela_app(self):
        label_name = ctk.CTkLabel(master=self.janela, text=f"SEJA BEM-VINDO {self.nome}!",
                                  font=("Times New Roman", 20), text_color="#00B0F0")
        label_name.place(x=10, y=40)

        label_account = ctk.CTkLabel(master=self.janela, text=f"Conta: {self.conta.numero}",
                                     font=("Times New Roman", 20), text_color="#00B0F0")
        label_account.place(x=500, y=40)

        label_balance_title = ctk.CTkLabel(master=self.janela, text="SALDO ATUAL",
                                           font=("Times New Roman", 20), text_color="#00B0F0")
        label_balance_title.place(x=10, y=80)

        if self.conta.saldo >= 100:
            label_balance = ctk.CTkLabel(master=self.janela, text=f"R$ {self.conta.saldo:.2f}",
                                         font=("Times New Roman", 30), text_color="#00B0F0")
        else:
            label_balance = ctk.CTkLabel(master=self.janela, text=f"R$ {self.conta.saldo:.2f}",
                                         font=("Times New Roman", 30), text_color="red")

        label_balance.place(x=160, y=72)


    def tela_inicio(self):
        self.frame_inicio = ctk.CTkFrame(master=self.janela, width=700, height=350)
        self.frame_inicio.pack(side=BOTTOM)
            
        btn_inicio = ctk.CTkButton(master=self.frame_inicio, text='INÍCIO',
                                        fg_color="transparent",font=("Times New Roman", 20))
        btn_inicio.place(x=50, y=20)

        btn_invest = ctk.CTkButton(master=self.frame_inicio, text='INVESTIMENTOS',
                                        fg_color="transparent",font=("Times New Roman", 20))
        btn_invest.place(x=240, y=20)

        btn_conta = ctk.CTkButton(master=self.frame_inicio, text='MINHA CONTA',
                                        fg_color="transparent",font=("Times New Roman", 20),
                                        command=self.tela_conta)
        btn_conta.place(x=450, y=20)


        btn_deposit = ctk.CTkButton(master=self.frame_inicio, text='DEPOSITAR',font=("Times New Roman", 20),
                                        command=self.depositar)
        btn_deposit.place(x=100, y=120)

        btn_sacar = ctk.CTkButton(master=self.frame_inicio,font=("Times New Roman", 20), text='SACAR', command=self.sacar)
        btn_sacar.place(x=100, y=180)

        btn_extrato = ctk.CTkButton(master=self.frame_inicio, text='EXTRATO',font=("Times New Roman", 20),
                                        command=self.mostrar_extrato)
        btn_extrato.place(x=100, y=240)


    def depositar(self):
        valor = simpledialog.askfloat("Depósito", "Informe o valor a depositar:")
        if valor is not None:
            msg = self.conta.depositar(valor)
            messagebox.showinfo("Depósito", msg)
            self.atualizar_saldo()
            self.tela_inicio()

    def sacar(self):
        valor = simpledialog.askfloat("Saque", "Informe o valor a sacar:")
        if valor is not None:
            msg = self.conta.sacar(valor)
            messagebox.showinfo("Saque", msg)
            self.atualizar_saldo()
            self.tela_inicio()

    def mostrar_extrato(self):
        extrato = self.conta.obter_extrato_transacoes()
        messagebox.showinfo("Extrato", extrato)


    def atualizar_saldo(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        self.tela_app()


    def tela_conta(self):
        # Esconder ou destruir o frame anterior
        self.frame_inicio.pack_forget()  # Esconde o frame anterior

        self.conta_frame = ctk.CTkFrame(master=self.janela, width=700, height=350)
        self.conta_frame.pack(side=BOTTOM)

        # Botão para voltar ao início
        btn_inicio = ctk.CTkButton(master=self.conta_frame, text='INÍCIO',
                                    fg_color="transparent", font=("Times New Roman", 20),
                                    command=self.back_to_inicio)
        btn_inicio.place(x=50, y=20)

        # Botões da nova tela
        btn_invest = ctk.CTkButton(master=self.conta_frame, text='INVESTIMENTOS',
                                    fg_color="transparent", font=("Times New Roman", 20))
        btn_invest.place(x=240, y=20)

        btn_conta = ctk.CTkButton(master=self.conta_frame, text='MINHA CONTA',
                                    fg_color="transparent", font=("Times New Roman", 20))
        btn_conta.place(x=450, y=20)

        # Exibir dados da conta como exemplo
        label_name = ctk.CTkLabel(master=self.conta_frame, text=f"Nome: {self.nome}",
                                    font=("Times New Roman", 20), text_color="#00B0F0")
        label_name.place(x=50, y=80)
        
        label_email = ctk.CTkLabel(master=self.conta_frame, text=f"E-mail: {self.email}",
                                    font=("Times New Roman", 20), text_color="#00B0F0")
        label_email.place(x=50, y=120)

        label_cpf = ctk.CTkLabel(master=self.conta_frame, text=f"CPF: {self.cpf}",
                                    font=("Times New Roman", 20), text_color="#00B0F0")
        label_cpf.place(x=50, y=160)


        label_account = ctk.CTkLabel(master=self.conta_frame, text=f"Conta: {self.conta.numero}",
                                    font=("Times New Roman", 20), text_color="#00B0F0")
        label_account.place(x=50, y=200)

        label_balance = ctk.CTkLabel(master=self.conta_frame, text=f"Saldo: R$ {self.conta.saldo:.2f}",
                                    font=("Times New Roman", 20), text_color="#00B0F0")
        label_balance.place(x=50, y=240)

        dim_password = len(self.password)
        
        label_password = ctk.CTkLabel(master=self.conta_frame, text=f"Senha: {"*" * dim_password}",
                                    font=("Times New Roman", 20), text_color="#00B0F0")
        label_password.place(x=50, y=240)

        btn_update_data = ctk.CTkButton(master= self.conta_frame,text = "Alterar Dados Cadastrados",
                                        fg_color='green',hover_color="#65B307",font=("Times New Roman", 20),
                                        command=self.escolher_dado_atualizar)
        btn_update_data.place(x=400, y=80)

        btn_logout = ctk.CTkButton(master= self.conta_frame,text = "LOGOUT",
                                        fg_color='red',font=("Times New Roman", 20),
                                        command=self.logout)
        btn_logout.place(x=400, y=130)

        btn_del_acc = ctk.CTkButton(master=self.conta_frame, text="EXCLUIR CONTA",
                            fg_color='red', font=("Times New Roman", 20),
                            command=lambda: self.del_acc(self.cpf))
        btn_del_acc.place(x=400, y=180)



    def logout(self):
        self.janela.destroy()
        from Login import Application
        Application()
        
    
    def excluir_usuario(self, cpf):
        conn = conectar()
        cursor = conn.cursor()
        
        try:
            # Comando SQL para excluir o registro onde o CPF corresponde
            cursor.execute("DELETE FROM Customers WHERE CPF = ?", (cpf))  # Corrigido para passar como tupla
            conn.commit()
            print(f"Usuário com CPF {cpf} foi excluído.")
        except sqlite3.Error as e:
            print(f"Erro ao excluir usuário: {e}")
        finally:
            conn.close()

    def del_acc(self, cpf):
        cpf = self.cpf
        if self.saldo > 0:
            resposta = messagebox.askyesno("Aviso", "A conta ainda possui saldo. Você tem certeza que deseja excluí-la?")
            if resposta:
                self.excluir_usuario(cpf)  # Chama a função de exclusão
                messagebox.showinfo("Sucesso", "Conta excluída com sucesso.")
            else:
                messagebox.showinfo("Cancelado", "A exclusão da conta foi cancelada.")
        else:
            self.excluir_usuario(cpf)  # Exclui se não houver saldo
            messagebox.showinfo("Sucesso", "Conta excluída com sucesso.")


    def escolher_dado_atualizar(self):
        # Criar uma nova janela (janela de diálogo)
        janela_atualizacao = Toplevel(self.janela)
        janela_atualizacao.title("Atualizar Dados")
        janela_atualizacao.geometry("300x150")
        
        # Label explicativa
        label = ctk.CTkLabel(master=janela_atualizacao, text="Escolha o dado que deseja atualizar:")
        label.pack(pady=10)

        # Criação da Combobox
        self.opcao_atualizacao = StringVar()
        combobox = ttk.Combobox(janela_atualizacao, textvariable=self.opcao_atualizacao, 
                                values=["Nome", "E-mail", "Senha"], state="readonly")
        combobox.set("Selecione uma opção")  # Placeholder padrão
        combobox.pack(pady=10)

        # Botão para confirmar a escolha
        confirmar_button = ctk.CTkButton(master=janela_atualizacao, text="Confirmar", 
                                        command=lambda: self.confirmar_atualizacao(janela_atualizacao))
        confirmar_button.pack(pady=10)

    def confirmar_atualizacao(self, janela_atualizacao):
        opcao = self.opcao_atualizacao.get().lower()

        if opcao in ["nome", "e-mail", "senha"]:
            # Fechar a janela de escolha
            janela_atualizacao.destroy()

            # Abrir um novo diálogo para pedir o novo valor
            novo_valor = simpledialog.askstring("Novo Valor", f"Informe o novo valor para {opcao.capitalize()}:")
            if novo_valor:
                self.atualizar_dado(opcao, novo_valor)
            else:
                messagebox.showerror("Erro", "Nenhum valor foi informado.")
        else:
            messagebox.showerror("Erro", "Dado inválido. Escolha entre Nome, E-mail, CPF ou Senha.")


    def atualizar_dado(self, campo, valor):
        conn = conectar()  # Função que conecta ao banco de dados
        cursor = conn.cursor()

        # Define o campo a ser atualizado
        if campo == "nome":
            cursor.execute("UPDATE Customers SET Name = ? WHERE CPF = ?", (valor, self.cpf))
            self.nome = valor  # Atualiza o atributo no sistema também
        elif campo == "e-mail":
            cursor.execute("UPDATE Customers SET Email = ? WHERE CPF = ?", (valor, self.cpf))
            self.email = valor
        elif campo == "senha":
            cursor.execute("UPDATE Customers SET Password = ? WHERE CPF = ?", (valor, self.cpf))
            self.password = valor

        conn.commit()
        conn.close()
        self.atualizar_saldo()  # Atualiza a interface com os novos dados        
        messagebox.showinfo("Sucesso", f"{campo.capitalize()} atualizado com sucesso!")
        self.tela_inicio()




    def back_to_inicio(self):
        self.conta_frame.pack_forget()
        self.frame_inicio.pack(side=BOTTOM)


# Função para verificar o login e iniciar o sistema
def verificar_login(cpf, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""SELECT ct.Name, C.Balance,C.NumberAccount,ct.Email,ct.CPF,ct.Password
                      FROM Customers ct
                      JOIN Contas C ON ct.CPF = C.CPF
                      WHERE ct.CPF = ? AND ct.Password = ?;""", (cpf, password))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nome, saldo, numero_conta, email, cpf, password = resultado
        Sistema(nome=nome, saldo=saldo, numero_conta=numero_conta,email=email,cpf=cpf,password=password)

    else:
        messagebox.showerror("Erro", "CPF ou senha incorretos.")


verificar_login("66495768168","familia281074",)