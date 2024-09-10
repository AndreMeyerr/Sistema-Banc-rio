import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog

class Conta:
    def __init__(self, numero, titular, saldo=0):
        self.numero = numero
        self.titular = titular
        self.saldo = saldo
        self.transacoes = []

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.transacoes.append((valor, 'DEPOSITO'))
            return f'Depósito de R${valor:.2f} realizado com sucesso! Saldo atual: R${self.saldo:.2f}'
        else:
            return 'Deposite um valor positivo!'

    def sacar(self, valor):
        if valor > self.saldo or valor < 0:
            return "Valor para saque inválido!"
        else:
            self.saldo -= valor
            self.transacoes.append((-valor, 'SAQUE'))
            return f'Saque de R${valor:.2f} realizado com sucesso! Saldo atual: R${self.saldo:.2f}'

    def transferir(self, valor, conta_destino):
        if valor > self.saldo or valor < 0:
            return "Transferência não realizada. Verifique o saldo ou o valor informado."
        else:
            self.saldo -= valor
            conta_destino.depositar(valor)
            self.transacoes.append((-valor, 'TRANSFERENCIA'))
            conta_destino.transacoes.append((valor, 'TRANSFERENCIA_RECEBIDA'))
            return f'Transferência de R${valor:.2f} realizada com sucesso para a conta {conta_destino.numero}!'

    def extrato(self):
        extrato_str = f"Extrato de transações da conta {self.numero}:\n"
        for valor, tipo in self.transacoes:
            tipo_transacao = 'Crédito' if valor > 0 else 'Débito'
            extrato_str += f"{tipo} - {tipo_transacao}: R${abs(valor):.2f}\n"
        extrato_str += f"Saldo atual: R${self.saldo:.2f}"
        return extrato_str

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Bancário")

        self.conta = None

        # Criar widgets
        self.create_widgets()

    def create_widgets(self):
        # Entrada do número da conta
        self.label_numero = tk.Label(self.root, text="Número da Conta:")
        self.label_numero.grid(row=0, column=0)
        self.entry_numero = tk.Entry(self.root)
        self.entry_numero.grid(row=0, column=1)

        # Entrada do titular da conta
        self.label_titular = tk.Label(self.root, text="Titular da Conta:")
        self.label_titular.grid(row=1, column=0)
        self.entry_titular = tk.Entry(self.root)
        self.entry_titular.grid(row=1, column=1)

        # Área de texto para mensagens
        self.text_area = scrolledtext.ScrolledText(self.root, width=40, height=10)
        self.text_area.grid(row=3, column=0, columnspan=2)

        # Botões
        self.btn_criar_conta = tk.Button(self.root, text="Criar Conta", command=self.criar_conta)
        self.btn_criar_conta.grid(row=2, column=0)

        self.btn_depositar = tk.Button(self.root, text="Depositar", command=self.depositar)
        self.btn_depositar.grid(row=2, column=1)

        self.btn_sacar = tk.Button(self.root, text="Sacar", command=self.sacar)
        self.btn_sacar.grid(row=2, column=2)

        self.btn_transferir = tk.Button(self.root, text="Transferir", command=self.transferir)
        self.btn_transferir.grid(row=2, column=3)

        self.btn_extrato = tk.Button(self.root, text="Extrato", command=self.mostrar_extrato)
        self.btn_extrato.grid(row=2, column=4)

    def criar_conta(self):
        numero = self.entry_numero.get()
        titular = self.entry_titular.get()
        if numero and titular:
            self.conta = Conta(numero, titular)
            self.text_area.insert(tk.END, f"Conta criada para {titular} com o número {numero}.\n")
        else:
            messagebox.showerror("Erro", "Número e titular da conta são obrigatórios!")

    def depositar(self):
        if self.conta:
            valor = float(simpledialog.askstring("Depósito", "Valor para depositar:"))
            mensagem = self.conta.depositar(valor)
            self.text_area.insert(tk.END, mensagem + "\n")
        else:
            messagebox.showerror("Erro", "Crie uma conta primeiro!")

    def sacar(self):
        if self.conta:
            valor = float(simpledialog.askstring("Saque", "Valor para sacar:"))
            mensagem = self.conta.sacar(valor)
            self.text_area.insert(tk.END, mensagem + "\n")
        else:
            messagebox.showerror("Erro", "Crie uma conta primeiro!")

    def transferir(self):
        if self.conta:
            numero_destino = simpledialog.askstring("Transferência", "Número da conta destino:")
            valor = float(simpledialog.askstring("Transferência", "Valor para transferir:"))
            conta_destino = Conta(numero_destino, "")  # Apenas um exemplo, deve ser tratado de outra forma.
            mensagem = self.conta.transferir(valor, conta_destino)
            self.text_area.insert(tk.END, mensagem + "\n")
        else:
            messagebox.showerror("Erro", "Crie uma conta primeiro!")

    def mostrar_extrato(self):
        if self.conta:
            extrato = self.conta.extrato()
            self.text_area.insert(tk.END, extrato + "\n")
        else:
            messagebox.showerror("Erro", "Crie uma conta primeiro!")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
