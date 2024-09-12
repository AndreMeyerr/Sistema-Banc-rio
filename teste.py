import customtkinter as ctk

# Inicializa a janela principal com customtkinter
root = ctk.CTk()
root.title('Banco Meyer')

# Definindo o tema do customtkinter
ctk.set_appearance_mode("dark")  # Tema escuro
ctk.set_default_color_theme("blue")  # Tema de cor azul padrão

# Definição de propriedades da janela
root.geometry('600x400')  # Tamanho da janela (largura x altura)


def criar_card(container, cor_fundo, titulo, texto_botao):
    # Frame para o card com fundo personalizado
    card_frame = ctk.CTkFrame(container, fg_color=cor_fundo, corner_radius=10)
    
    # Rótulo para a explicação
    titulo_label = ctk.CTkLabel(card_frame, text=titulo, font=("Arial", 12), text_color="white")
    titulo_label.pack(pady=(10, 10))

    # Botão de ação
    botao = ctk.CTkButton(card_frame, text=texto_botao, fg_color='#007BFF', hover_color='#0056b3', corner_radius=5)
    botao.pack(pady=(0, 10))

    return card_frame

# Criando um frame principal para alinhar os cards
frame_principal = ctk.CTkFrame(root)
frame_principal.pack(pady=40)

# Adicionando os cards ao frame principal
card1 = criar_card(frame_principal, '#333333', 'Realize um depósito na sua conta.', 'DEPOSITAR')
card1.grid(row=0, column=0, padx=10)

card2 = criar_card(frame_principal, '#333333', 'Faça um saque do seu saldo.', 'SACAR')
card2.grid(row=0, column=1, padx=10)

card3 = criar_card(frame_principal, '#333333', 'Consulte o seu extrato de transações.', 'EXTRATO')
card3.grid(row=0, column=2, padx=10)

# Executa o loop da interface gráfica
root.mainloop()
