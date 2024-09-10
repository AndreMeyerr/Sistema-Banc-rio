import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from database import cadastrar_usuario, verificar_login_nome_saldo_conta
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
        self.janela.resizable(False, False)

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

        nome_saldo_conta_logado = verificar_login_nome_saldo_conta(cpf, password)
        
        if nome_saldo_conta_logado:
            messagebox.showinfo(title="Situação de Login", message='Login Feito com Sucesso!')
            self.janela.destroy()
            from curso import Sistema
            Sistema(nome_saldo_conta_logado[0],nome_saldo_conta_logado[1],nome_saldo_conta_logado[2],nome_saldo_conta_logado[3],nome_saldo_conta_logado[4],nome_saldo_conta_logado[5])  # Inicia o sistema passando o nome e saldo do usuário
  
              
        else:
            messagebox.showerror(title="Erro", message="Nome de usuário ou senha incorretos.")


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
        back_button = ctk.CTkButton(master=self.rg_frame, text="Voltar", fg_color="gray", hover_color="#404143",
                                    width=100, command=self.back_to_login)
        back_button.place(x=25, y=350)

    def is_valid_email(self, email):
        # Verifica se o email tem um formato válido
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None

    def is_valid_cpf(self, cpf):
        # Implementa a lógica de validação de CPF (apenas um exemplo simples)
        # A validação de CPF completa é mais complexa, considerando dígitos verificadores
        if len(cpf) != 11 or not cpf.isdigit():
            return False
        return True

    def is_valid_name(self, name):
    # Verifica se o nome de usuário não é vazio, tem pelo menos 3 caracteres
    # e não contém números nem caracteres especiais.
        if len(name) < 3:
            return False
        regex = r'^[a-zA-Z\s]+$'
        return re.match(regex, name) is not None

    def is_valid_password(self, password):
        # Verifica se a senha tem pelo menos 8 caracteres e contém letras e números
        return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password)

    def is_valid_age(self,date_of_birth):
        try:
            birth_date = datetime.strptime(date_of_birth, "%d/%m/%Y")
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                messagebox.showerror(title="Erro", message="Você deve ter pelo menos 18 anos para se cadastrar.")
                return False
            return True
        except ValueError:
            messagebox.showerror(title="Erro", message="Data de nascimento inválida. Use o formato dd/mm/yyyy.")
            return False

    def register_user(self):
        name = self.name_entry.get()
        date_of_birth = self.data_nascimento_entry.get()
        email = self.email_entry.get()
        cpf = self.cpf_entry.get()
        password = self.password_entry.get()

        # Validações
        if not self.is_valid_name(name):
            messagebox.showerror(title="Erro", message="O nome deve ter pelo menos 3 caracteres e não deve conter números ou caracteres especiais.")
            return
        age = self.is_valid_age(date_of_birth)
        if age is False:  # Se a idade não for válida
            return
        if not self.is_valid_email(email):
            messagebox.showerror(title="Erro", message="Email inválido.")
            return
        if not self.is_valid_cpf(cpf):
            messagebox.showerror(title="Erro", message="CPF deve ter 11 dígitos numéricos.")
            return
        if not self.is_valid_password(password):
            messagebox.showerror(title="Erro", message="A senha deve ter pelo menos 8 caracteres, incluindo letras, números e caracteres especiais.")
            return
        
        
        
        # Cadastra o usuário se todas as validações passarem
        if cadastrar_usuario(name, cpf, age, email, password):
            messagebox.showinfo(title="Situação Cadastro", message='Parabéns! Usuário Cadastrado Com Sucesso!')
        else:
            messagebox.showerror(title="Erro", message="Erro ao cadastrar. Verifique as informações.")



    def back_to_login(self):
        self.rg_frame.pack_forget()
        self.login_frame.pack(side=RIGHT)



# Executa a aplicação
Application()
