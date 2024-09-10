import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from database import cadastrar_usuario, verificar_login
import re
from datetime import datetime

class Application():
    def __init__(self):
        self.janela = ctk.CTk()
        self.tema()
        self.tela()
        self.tela_login()
        self.janela.mainloop()

    def tema(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
    
    def tela(self):
        self.janela.geometry("700x400")
        self.janela.title("Sistema de Login")
        self.janela.resizable(FALSE,FALSE)

    def tela_login(self):
        # Trabalhando com a Imagem
        self.img = PhotoImage(file="Imagem Teste.png")
        Label_img = ctk.CTkLabel(master=self.janela, image=self.img, text=None)
        Label_img.place(x=-30, y=65)

        label_tt = ctk.CTkLabel(master=self.janela, text="Faça o Login para ter Acesso a Sua Conta!",
                                font=("Roboto", 18), text_color="#00B0F0")
        label_tt.place(x=10, y=60)

        # Login frame
        self.login_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.login_frame.pack(side=RIGHT)

        # Frame widgets
        label = ctk.CTkLabel(master=self.login_frame, text="Sistema de Login", font=("Roboto", 30))
        label.place(x=25, y=5)

        self.cpf_entry = ctk.CTkEntry(master=self.login_frame, placeholder_text="CPF: ",
                                      width=300, font=("Roboto", 14))
        self.cpf_entry.place(x=25, y=105)
        cpf_label = ctk.CTkLabel(master=self.login_frame,
                                      text="O Campo CPF do Usuário é de caráter Obrigatório.",
                                      text_color="green", font=("Roboto", 8))
        cpf_label.place(x=25, y=135)

        self.password_entry = ctk.CTkEntry(master=self.login_frame, placeholder_text="Senha do Usuário:",
                                      width=300, show="*", font=("Roboto", 14))
        self.password_entry.place(x=25, y=175)
        password_label = ctk.CTkLabel(master=self.login_frame,
                                      text="O Campo Senha do Usuário é de caráter Obrigatório.",
                                      text_color="green", font=("Roboto", 8))
        password_label.place(x=25, y=205)

        remember_password_checkbox = ctk.CTkCheckBox(master=self.login_frame, text="Manter-me Conectado")
        remember_password_checkbox.place(x=25, y=235)

        # Login Button
        login_button = ctk.CTkButton(master=self.login_frame, text="LOGIN", fg_color="#006494",
                                     command=self.login_user, width=300)
        login_button.place(x=25, y=275)

        # Register option
        choice_register_span = ctk.CTkLabel(master=self.login_frame, text="Se Não Possuir Uma Conta -> ")
        choice_register_span.place(x=25, y=310)

        choice_register_button = ctk.CTkButton(master=self.login_frame, text="Cadastre-se", fg_color="green",
                                               hover_color="#2D9334", command=self.tela_register, width=100)
        choice_register_button.place(x=225, y=310)

    def login_user(self):
        cpf = self.cpf_entry.get()
        password = self.password_entry.get()
        if verificar_login(cpf, password):
            messagebox.showinfo(title="Situação de Login", message='Login Feito com Sucesso!')
            self.tela_caixa_eletronico()
        else:
            messagebox.showerror(title="Erro", message="Nome de usuário ou senha incorretos.")

    def tela_caixa_eletronico(self):
        # Remove a interface de login
        self.login_frame.pack_forget()

        # Caixa eletrônico interface
        caixa_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        caixa_frame.pack(side=RIGHT)

        label = ctk.CTkLabel(master=caixa_frame, text="Caixa Eletrônico", font=("Roboto", 30))
        label.place(x=25, y=5)

        # Exemplo de Botões para funcionalidades do Caixa Eletrônico
        depositar_button = ctk.CTkButton(master=caixa_frame, text="Depositar", fg_color="#00B0F0", command=self.depositar, width=300)
        depositar_button.place(x=25, y=75)

        sacar_button = ctk.CTkButton(master=caixa_frame, text="Sacar", fg_color="#00B0F0", command=self.sacar, width=300)
        sacar_button.place(x=25, y=115)

        transferir_button = ctk.CTkButton(master=caixa_frame, text="Transferir", fg_color="#00B0F0", command=self.transferir, width=300)
        transferir_button.place(x=25, y=155)

        saldo_button = ctk.CTkButton(master=caixa_frame, text="Ver Saldo", fg_color="#00B0F0", command=self.ver_saldo, width=300)
        saldo_button.place(x=25, y=195)

        sair_button = ctk.CTkButton(master=caixa_frame, text="Sair", fg_color="red", command=self.janela.quit, width=300)
        sair_button.place(x=25, y=235)

    def depositar(self):
        valor = float(messagebox.askstring("Depósito", "Valor para depositar:"))
        # Lógica de depósito

    def sacar(self):
        valor = float(messagebox.askstring("Saque", "Valor para sacar:"))
        # Lógica de saque

    def transferir(self):
        numero_destino = messagebox.askstring("Transferência", "Número da conta destino:")
        valor = float(messagebox.askstring("Transferência", "Valor para transferir:"))
        # Lógica de transferência

    def ver_saldo(self):
        # Exibe o saldo atual
        messagebox.showinfo("Saldo", "Seu saldo é: R$ X.XXX,XX")

    def tela_register(self):
        # Remover o frame de Login e adicionando frame de Registro
        self.login_frame.pack_forget()
        self.rg_frame = ctk.CTkFrame(master=self.janela, width=350, height=396)
        self.rg_frame.pack(side=RIGHT)

        label = ctk.CTkLabel(master=self.rg_frame, text='Faça o seu Cadastro!', font=('Roboto', 20))
        label.place(x=25, y=5)

        register_span = ctk.CTkLabel(master=self.rg_frame, text="Favor Preencher com Dados Verídicos ",
                                    font=('Roboto', 12))
        register_span.place(x=25, y=45)

        self.name_entry = ctk.CTkEntry(master=self.rg_frame, placeholder_text="Nome Completo: ",
                                    width=300, font=("Roboto", 14))
        self.name_entry.place(x=25, y=75)

        self.data_nascimento_entry = ctk.CTkEntry(master=self.rg_frame, placeholder_text="Data de Nascimento: (dd/mm/yyyy)",
                                        width=300, font=("Roboto", 14))
        self.data_nascimento_entry.place(x=25, y=115)

        self.email_entry = ctk.CTkEntry(master=self.rg_frame, placeholder_text="Email de Usuário: ",
                                    width=300, font=("Roboto", 14))
        self.email_entry.place(x=25, y=155)

        self.cpf_entry = ctk.CTkEntry(master=self.rg_frame, placeholder_text="CPF: ",
                                width=300, font=("Roboto", 14))
        self.cpf_entry.place(x=25, y=195)

        self.password_entry = ctk.CTkEntry(master=self.rg_frame, placeholder_text="Senha: ",
                                    show="*", width=300, font=("Roboto", 14))
        self.password_entry.place(x=25, y=235)

        terms_checkbox = ctk.CTkCheckBox(master=self.rg_frame, text="Concordo com os Termos e Políticas")
        terms_checkbox.place(x=25, y=275)

        # Register Button
        register_button = ctk.CTkButton(master=self.rg_frame, text="REGISTRAR", command=self.register_user,
                                        fg_color="green", hover_color="#014B05", width=300)
        register_button.place(x=25, y=310)

        # Back Button
        back_button = ctk.CTkButton(master=self.rg_frame, text="Voltar", command=self.voltar_tela_login, fg_color="red",
                                    hover_color="#A3262A", width=100)
        back_button.place(x=225, y=350)

    def register_user(self):
        name = self.name_entry.get()
        data_nascimento = self.data_nascimento_entry.get()
        email = self.email_entry.get()
        cpf = self.cpf_entry.get()
        password = self.password_entry.get()

        # Data de Nascimento Validação
        if not re.match(r'\d{2}/\d{2}/\d{4}', data_nascimento):
            messagebox.showerror("Erro de Cadastro", "Data de nascimento inválida. Formato esperado: dd/mm/yyyy.")
            return

        data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y').date()
        idade = (datetime.now().date() - data_nascimento).days // 365

        if idade < 18:
            messagebox.showerror("Erro de Cadastro", "Usuário menor de 18 anos. Cadastro não permitido.")
            return

        if not name or not email or not cpf or not password:
            messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios.")
            return

        try:
            cadastrar_usuario(name, cpf, password, data_nascimento, email)
            messagebox.showinfo(title="Situação de Cadastro", message="Cadastro feito com Sucesso!")
            self.voltar_tela_login()
        except Exception as e:
            messagebox.showerror("Erro de Cadastro", str(e))

    def voltar_tela_login(self):
        self.rg_frame.pack_forget()
        self.tela_login()

if __name__ == '__main__':
    Application()
