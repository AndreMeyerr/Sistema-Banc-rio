import sqlite3
import random


def conectar():
    return sqlite3.connect("BancoMeyer.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    # Comando para criar a tabela 'Customers' com todas as colunas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customers(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        CPF TEXT UNIQUE NOT NULL,
        Idade INTEGER NOT NULL,
        Email TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Contas (
        NumberAccount INTEGER PRIMARY KEY,
        Name TEXT NOT NULL,
        Balance REAL DEFAULT 0,
        CPF TEXT,
        FOREIGN KEY(CPF) REFERENCES Customers(CPF)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_conta INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        valor REAL NOT NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(numero_conta) REFERENCES Contas(NumberAccount)
    )
    """)

    conn.commit()
    conn.close()

def gerar_numero_conta():
    return random.randint(1000, 9999)

# Cria a nova tabela
criar_tabelas()

def cadastrar_usuario(name, cpf, idade, email, password):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO Customers (Name, CPF, Idade, Email, Password) VALUES (?, ?, ?, ?, ?)",
                       (name, cpf, idade, email, password))

        numero_conta = gerar_numero_conta()
        cursor.execute("SELECT NumberAccount FROM Contas WHERE NumberAccount = ?", (numero_conta,))
        while cursor.fetchone() is not None:
            numero_conta = gerar_numero_conta()
        
        # Inserir nova conta na tabela Contas
        cursor.execute("INSERT INTO Contas (NumberAccount, Name, Balance, CPF) VALUES (?, ?, ?, ?)", (numero_conta, name, 0.0, cpf))
        
        # Confirmar transação
        conn.commit()
        print(f"Usuário {name} cadastrado com sucesso! Número da conta: {numero_conta}")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Erro ao cadastrar usuário: {e}")
    finally:
        conn.close()


def verificar_login_nome_saldo_conta(cpf, password):
    conn = conectar()
    cursor = conn.cursor()
    
    # Selecione o nome do cliente junto com a verificação do CPF e da senha
    cursor.execute("""SELECT ct.Name, C.Balance,C.NumberAccount,ct.Email,ct.CPF,ct.Password
                        FROM Customers ct
                        JOIN Contas C
                        ON ct.CPF = C.CPF
                        WHERE ct.CPF = ? AND ct.Password = ?;""", (cpf, password))
    
    resultado = cursor.fetchone()
    
    conn.close()
    
    if resultado:
        return resultado
    return None
 


#def verificar_login_saldo(cpf, password):
    conn = conectar()
    cursor = conn.cursor()
    
    # Selecione o nome do cliente junto com a verificação do CPF e da senha
    cursor.execute("""SELECT ct.CPF,  C.Balance
                        FROM Customers ct
                        JOIN Contas C
                        ON ct.CPF = C.CPF;
                        """, (cpf, password))
    resultado = cursor.fetchone()
    
    conn.close()
    
    if resultado:
        return resultado  
    return None  


def ver_estrutura_tabela():
    conn = conectar()
    cursor = conn.cursor()
    
    # Comando para ver a estrutura da tabela Customers
    cursor.execute("PRAGMA table_info(Contas)")
    
    # Recupera todas as linhas da consulta
    colunas = cursor.fetchall()
    
    # Exibe as colunas com seus detalhes
    for coluna in colunas:
        print(coluna)
    
    conn.close()

def excluir_usuario(cpf):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        # Comando SQL para excluir o registro onde o CPF corresponde
        cursor.execute("DELETE FROM Customers WHERE CPF = ?", (cpf,))
        conn.commit()
        print(f"Usuário com CPF {cpf} foi excluído.")
    except sqlite3.Error as e:
        print(f"Erro ao excluir usuário: {e}")
    finally:
        conn.close()


def checar_database():
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        # Executa a consulta para selecionar todos os registros
        cursor.execute('SELECT * FROM Customers')
        consulta = cursor.fetchall()
        
        # Imprime os registros
        for registro in consulta:
            print(registro)
    except sqlite3.Error as e:
        print(f"Erro ao consultar a base de dados: {e}")
    finally:
        conn.close()


def usuario_existe(cpf):
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Customers WHERE CPF = ?", (cpf,))
    resultado = cursor.fetchone()
    
    conn.close()
    return resultado is not None

def atualizar_saldo_db(numero_conta, saldo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE Contas SET Balance = ? WHERE NumberAccount = ?", (saldo, numero_conta))
    conn.commit()
    conn.close()

def obter_saldo_db(numero_conta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT Balance FROM Contas WHERE NumberAccount = ?", (numero_conta,))
    saldo = cursor.fetchone()[0]
    conn.close()
    return saldo

checar_database()