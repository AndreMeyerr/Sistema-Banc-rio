import sqlite3
import random


def conectar():
    return sqlite3.connect("BancoMeyer.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

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
    cursor.execute("PRAGMA table_info(Customers)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]
    if 'is_admin' not in colunas:
        cursor.execute("ALTER TABLE Customers ADD COLUMN is_admin INTEGER DEFAULT 0")
        print("Coluna 'is_admin' adicionada à tabela 'Customers'.")
    
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
        return True  
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Erro ao cadastrar usuário: {e}")
        return False  
    finally:
        conn.close()



def verificar_login_nome_saldo_conta(cpf, password):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT ct.Name, C.Balance, C.NumberAccount, ct.Email, ct.CPF, ct.Password, ct.is_admin
                      FROM Customers ct
                      LEFT JOIN Contas C ON ct.CPF = C.CPF
                      WHERE ct.CPF = ? AND ct.Password = ?;""", (cpf, password))

    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return resultado
    return None

 

def ver_estrutura_tabela():
    conn = conectar()
    cursor = conn.cursor()
    
  
    cursor.execute("PRAGMA table_info(Contas)")
    colunas = cursor.fetchall()
    for coluna in colunas:
        print(coluna)
    
    conn.close()

def excluir_usuario(cpf):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
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
        cursor.execute('SELECT * FROM Customers')
        consulta = cursor.fetchall()
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

def limpar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        # Deleta os dados das tabelas Customers, Contas e Transacoes
        cursor.execute("DELETE FROM Transacoes")
        cursor.execute("DELETE FROM Contas")
        cursor.execute("DELETE FROM Customers")
        conn.commit()
        print("Dados das tabelas limpos com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao limpar tabelas: {e}")
    finally:
        conn.close()



def ver_estrutura_tabela(nome_tabela):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        # Ver a estrutura da tabela
        cursor.execute(f"PRAGMA table_info({nome_tabela})")
        colunas = cursor.fetchall()
        
        print(f"Estrutura da tabela {nome_tabela}:")
        for coluna in colunas:
            print(coluna)
    except sqlite3.Error as e:
        print(f"Erro ao consultar a estrutura da tabela {nome_tabela}: {e}")
    finally:
        conn.close()

def criar_usuario_admin():
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO Customers (Name, CPF, Idade, Email, Password, is_admin)
        VALUES (?, ?, ?, ?, ?, 1)
        """, ("Administrador", "00000000000", 30, "admin@example.com", "admin123"))
        conn.commit()
        print("Usuário administrador criado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar administrador: {e}")
    finally:
        conn.close()

checar_database()



