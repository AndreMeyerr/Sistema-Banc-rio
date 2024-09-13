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
    def transferir(self, numero_conta_destino, valor):
        # Converte o valor para float e verifica se é válido
        try:
            valor = float(valor)
            if valor <= 0:
                return "Valor de transferência inválido."
        except ValueError:
            return "Valor de transferência inválido."

        # Verifica se há saldo suficiente para a transferência
        if self.saldo < valor:
            return "Saldo insuficiente para realizar a transferência."

        # Verifica se a conta de destino existe
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT Balance FROM Contas WHERE NumberAccount = ?", (numero_conta_destino,))
        resultado = cursor.fetchone()

        if not resultado:
            conn.close()
            return "Conta de destino não encontrada."

        # Obtém o saldo da conta de destino
        saldo_destino = resultado[0]

        try:
            # Atualiza o saldo da conta de origem
            self.saldo -= valor
            atualizar_saldo_db(self.numero, self.saldo)
            self.registrar_transacao('TRANSFERÊNCIA ENVIADA', -valor)

            # Atualiza o saldo da conta de destino
            saldo_destino += valor
            cursor.execute("UPDATE Contas SET Balance = ? WHERE NumberAccount = ?", (saldo_destino, numero_conta_destino))
            conn.commit()

            # Registra a transação na conta de destino
            cursor.execute("""
            INSERT INTO Transacoes (numero_conta, tipo, valor)
            VALUES (?, 'TRANSFERÊNCIA RECEBIDA', ?)
            """, (numero_conta_destino, valor))
            conn.commit()

            return f"Transferência de R${valor:.2f} para a conta {numero_conta_destino} realizada com sucesso!"

        except sqlite3.Error as e:
            return f"Erro ao realizar transferência: {e}"

        finally:
            conn.close()

        
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
    
class pessoa:
    def __init__(self,nome,email,cpf):
        self.nome = nome
        self.email = email
        self.cpf = cpf


class Sistema(pessoa):
    def __init__(self, nome, saldo, numero_conta, email, cpf, password):
        super().__init__(nome,email,cpf)
        self.saldo = saldo
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
        label_name = ctk.CTkLabel(master=self.janela, text=f"SEJA BEM-VINDO {self.nome.upper()}!",
                                  font=("ARIAL", 20,"bold"), text_color="#00B0F0")
        label_name.place(x=10, y=40)

        label_account = ctk.CTkLabel(master=self.janela, text=f"Conta: {self.conta.numero}",
                                     font=("ARIAL", 20,"bold"), text_color="#00B0F0")
        label_account.place(x=357, y=80)

        label_balance_title = ctk.CTkLabel(master=self.janela, text="SALDO ATUAL: ",
                                           font=("ARIAL", 20,"bold"), text_color="#00B0F0")
        label_balance_title.place(x=10, y=80)

        if self.conta.saldo >= 100:
            label_balance = ctk.CTkLabel(master=self.janela, text=f"R$ {self.conta.saldo:.2f}",
                                         font=("ARIAL", 30,"bold"), text_color="green")
        else:
            label_balance = ctk.CTkLabel(master=self.janela, text=f"R$ {self.conta.saldo:.2f}",
                                         font=("ARIAL", 30,"bold"), text_color="red")

        label_balance.place(x=160, y=72)





    
    def tela_inicio(self):
        self.frame_inicio = ctk.CTkFrame(master=self.janela, width=700, height=350)
        self.frame_inicio.pack(side=ctk.BOTTOM)

        # Botões de navegação
        btn_inicio = ctk.CTkButton(master=self.frame_inicio, text='INÍCIO',
                                fg_color="#7BB4E3", font=("Times New Roman", 20))
        btn_inicio.place(x=50, y=20)

        btn_transferir = ctk.CTkButton(master=self.frame_inicio, text='TRANSFERÊNCIA',
                                    fg_color="#004B57", font=("Times New Roman", 20),
                                    command=self.transferir)
        btn_transferir.place(x=240, y=20) 

        btn_conta = ctk.CTkButton(master=self.frame_inicio, text='MINHA CONTA',
                                fg_color="#004B57", font=("Times New Roman", 20),
                                command=self.tela_conta)
        btn_conta.place(x=450, y=20)     



        def criar_card(container, cor_fundo, cor_borda, titulo, comando_botao, descricao, texto_botao):
            card_frame = ctk.CTkFrame(
                container, fg_color=cor_fundo, corner_radius=15, border_width=2, 
                border_color=cor_borda, width=300, height=200
            )
            
            titulo_label = ctk.CTkLabel(
                card_frame, text=titulo, font=("Arial", 14, "bold"), fg_color='transparent', 
                text_color="white", wraplength=260, anchor='center', justify="center", width=260
            )
            titulo_label.place(relx=0.5, rely=0.2, anchor='center')  

            descricao_label = ctk.CTkLabel(
                card_frame, text=descricao, font=("Arial", 11), text_color="white", 
                wraplength=260, justify="center", width=260
            )
            descricao_label.place(relx=0.5, rely=0.5, anchor='center')  

            botao = ctk.CTkButton(
            card_frame, text=texto_botao, font=("Arial", 14, "bold"), command=comando_botao, 
            fg_color='#00A2E8', hover_color='#007ACC', corner_radius=8, text_color='white',
            width=150, height=40  # Aumentando a largura e altura do botão
            )
            botao.place(relx=0.5, rely=0.8, anchor='center')  # Posicionamento relativo dentro do card

            return card_frame



        # Criando frames específicos para cada card
        frame_card1 = ctk.CTkFrame(self.frame_inicio, width=220, height=240, fg_color="transparent")
        frame_card1.place(x=10, y=50)
        card1 = criar_card(frame_card1, 'transparent', '#00569D', 'Realize um \n Depósito na sua conta.', comando_botao=self.depositar, descricao='Deposite dinheiro na sua conta para\n aumentar o saldo disponível.', texto_botao='DEPOSITAR')
        card1.place(relx=0.5, rely=0.5, anchor='center')  # Posicionando o card dentro do frame
        
        
        frame_card2 = ctk.CTkFrame(self.frame_inicio, width=220, height=240, fg_color="transparent")
        frame_card2.place(x=215, y=50)
        card2 = criar_card(frame_card2, 'transparent', '#00569D', 'Realize um\n saque na sua Conta.', comando_botao=self.sacar, descricao='Saque dinheiro da sua conta,\n reduzindo o saldo atual.', texto_botao='SACAR')
        card2.place(relx=0.5, rely=0.5, anchor='center') 

        frame_card3 = ctk.CTkFrame(self.frame_inicio, width=220, height=240, fg_color="transparent")
        frame_card3.place(x=412, y=50)
        card3 = criar_card(frame_card3, 'transparent', '#00569D', 'Consulte o seu\n Extrato \nde Transações.', comando_botao=self.mostrar_extrato, descricao='Visualize todas as transações\n realizadas na sua conta.', texto_botao='EXTRATO')
        card3.place(relx=0.5, rely=0.5, anchor='center')
    
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
    def transferir(self):
        # Criação de uma nova janela de diálogo
        janela_transferencia = Toplevel(self.janela)
        janela_transferencia.title("Transferência")
        janela_transferencia.geometry("300x400")


        label_conta = ctk.CTkLabel(janela_transferencia, text_color='black', text="Número da Conta de Destino:", font=("Arial", 12))
        label_conta.pack(pady=(20, 5))

        entry_conta = ctk.CTkEntry(janela_transferencia, placeholder_text="Conta: ", font=("Roboto", 14), width=200)
        entry_conta.pack(pady=(0, 10))

        
        label_valor = ctk.CTkLabel(janela_transferencia, text_color='black', text="Valor da Transferência (R$):", font=("Arial", 12))
        label_valor.pack(pady=(10, 5))

        entry_valor = ctk.CTkEntry(janela_transferencia, placeholder_text="Valor R$: ", font=("Roboto", 14), width=200)
        entry_valor.pack(pady=(0, 20))

        # Função interna para capturar os dados de entrada e executar a transferência
        def executar_transferencia():
            numero_conta_destino = entry_conta.get()
            valor_transferencia = entry_valor.get()

            # Chama o método de transferência da classe Conta
            resultado = self.conta.transferir(numero_conta_destino, valor_transferencia)
            
            # Exibe o resultado da operação
            messagebox.showinfo("Resultado da Transferência", resultado)
            
            # Fecha a janela de transferência após o sucesso
            janela_transferencia.destroy()
            self.atualizar_saldo()
            self.tela_inicio()

        # Botão para confirmar a transferência
        btn_confirmar = ctk.CTkButton(janela_transferencia, text="Confirmar", command=executar_transferencia)
        btn_confirmar.pack(pady=10)

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
                                    fg_color="#004B57", font=("Times New Roman", 20),
                                    command=self.back_to_inicio)
        btn_inicio.place(x=50, y=20)

        btn_transferir = ctk.CTkButton(master=self.conta_frame, text='TRANSFERÊNCIA',
                                    fg_color="#004B57", font=("Times New Roman", 20),
                                    command=self.transferir)
        btn_transferir.place(x=240, y=20) 
        
        

        btn_conta = ctk.CTkButton(master=self.conta_frame, text='MINHA CONTA',
                                    fg_color="#7BB4E3", font=("Times New Roman", 20))
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
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                
                # Excluir todas as transações associadas ao usuário
                cursor.execute("DELETE FROM Transacoes WHERE numero_conta IN (SELECT NumberAccount FROM Contas WHERE CPF = ?)", (cpf,))
                
                # Excluir todas as contas associadas ao usuário
                cursor.execute("DELETE FROM Contas WHERE CPF = ?", (cpf,))
                
                # Excluir o próprio usuário
                cursor.execute("DELETE FROM Customers WHERE CPF = ?", (cpf,))
                
                conn.commit()
                print(f"Usuário com CPF {cpf} foi excluído.")
        except sqlite3.Error as e:
            print(f"Erro ao excluir usuário: {e}")
            messagebox.showerror("Erro", f"Não foi possível excluir o usuário: {e}")


    def del_acc(self, cpf):
        if self.saldo > 0:
            resposta = messagebox.askyesno("Aviso", "A conta ainda possui saldo. Você tem certeza que deseja excluí-la?")
            if resposta:
                self.excluir_usuario(cpf)  # Chama a função de exclusão
                messagebox.showinfo("Sucesso", "Conta excluída com sucesso.")
                self.janela.destroy()  # Fecha a janela atual
                self.voltar_para_login()
            else:
                messagebox.showinfo("Cancelado", "A exclusão da conta foi cancelada.")
        else:
            self.excluir_usuario(cpf)  # Exclui se não houver saldo
            messagebox.showinfo("Sucesso", "Conta excluída com sucesso.")
            self.janela.destroy()  # Fecha a janela atual
            self.voltar_para_login()
            
    def voltar_para_login(self):
        from Login import Application
        Application()


    def escolher_dado_atualizar(self):
        # Criar uma nova janela (janela de diálogo)
        janela_atualizacao = Toplevel(self.janela)
        janela_atualizacao.title("Atualizar Dados")
        janela_atualizacao.geometry("400x250")  # Aumenta o tamanho da janela
        
        # Label explicativa
        label = ctk.CTkLabel(master=janela_atualizacao, text="Escolha o dado que deseja atualizar:",
                            font=("Arial", 14), text_color='black')  # Aumenta o tamanho da fonte
        label.pack(pady=20)  # Aumenta o espaçamento vertical para 20

        # Criação da Combobox com tamanho de fonte ajustado
        self.opcao_atualizacao = StringVar()
        combobox = ttk.Combobox(janela_atualizacao, textvariable=self.opcao_atualizacao, 
                                values=["Nome", "E-mail", "Senha"], state="readonly", font=("Arial", 12))  # Define o tamanho da fonte
        combobox.set("Selecione uma opção")  # Placeholder padrão
        combobox.pack(pady=20, padx=10, ipadx=10, ipady=5)  # Aumenta o espaçamento e o preenchimento

        # Botão para confirmar a escolha
        confirmar_button = ctk.CTkButton(master=janela_atualizacao, text="Confirmar", 
                                        command=lambda: self.confirmar_atualizacao(janela_atualizacao))
        confirmar_button.pack(pady=20)  # Aumenta o espaçamento vertical para 20

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
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT ct.Name, C.Balance,C.NumberAccount,ct.Email,ct.CPF,ct.Password
                              FROM Customers ct
                              JOIN Contas C ON ct.CPF = C.CPF
                              WHERE ct.CPF = ? AND ct.Password = ?;""", (cpf, password))
            resultado = cursor.fetchone()
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao verificar login: {e}")
        return

    if resultado:
        nome, saldo, numero_conta, email, cpf, password = resultado
        Sistema(nome=nome, saldo=saldo, numero_conta=numero_conta, email=email, cpf=cpf, password=password)
    else:
        messagebox.showerror("Erro", "CPF ou senha incorretos.")



verificar_login("03868304100","fama1234",)