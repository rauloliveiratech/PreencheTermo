import tkinter as tk
import pyperclip  # Biblioteca para copiar o texto para a área de transferência
from tkinter import ttk

campos_de_entrada = []  # Lista para armazenar os objetos Entry
modelo_valor_dict = {
    "PC701": "R$2.000,00",
    "UL151": "R$3.665,69",
    "UL152": "R$3.887,17",
    "UL124": "R$4.121,60",
    "UB536": "R$2.225,13",
    "UB523": "R$2.225,13",
    "IMAC": "R$16.000,00",
    "Macbook": "R$18.000,00"
}

def copiar_texto(indice):
    if isinstance(campos_de_entrada[indice], ttk.Combobox):
        valor_selecionado = campos_de_entrada[indice].get()  # Obter o valor selecionado no Combobox
        if valor_selecionado:  # Verificar se um valor foi selecionado
            pyperclip.copy(valor_selecionado)
    else:
        texto = campos_de_entrada[indice].get()
        pyperclip.copy(texto)

def limpar_campos():
    for entrada in campos_de_entrada:
        entrada.delete(0, tk.END)

def preencher_usuario(event):
    email = campos_de_entrada[1].get()  # Índice 1 corresponde ao campo de e-mail
    if "@" in email:
        usuario = email.split("@")[0]
        campos_de_entrada[6].delete(0, tk.END)  # Limpar o campo "Usuário" antes de preencher automaticamente
        campos_de_entrada[6].insert(0, usuario)

def preencher_valor(event):
    modelo = modelo_var.get()  # Obter o modelo selecionado na lista de opções
    if modelo in modelo_valor_dict:
        valor = modelo_valor_dict[modelo]
        campos_de_entrada[8].delete(0, tk.END)  # Limpar o campo "Valor" antes de preencher automaticamente
        campos_de_entrada[8].insert(0, valor)
    else:
        campos_de_entrada[8].delete(0, tk.END)  # Limpa o campo "Valor" se o modelo não for encontrado

def validar_cpf(event):
    cpf = campos_de_entrada[2].get()  # Índice 2 corresponde ao campo "CPF"
    if len(cpf) == 11 and cpf.isdigit():
        campos_de_entrada[2].config(fg='green')  # Alterar a cor do texto para verde se o CPF for válido
    else:
        campos_de_entrada[2].config(fg='red')  # Alterar a cor do texto para vermelho se o CPF for inválido

def proximo_campo(event, root):
    atual = campos_de_entrada.index(root.focus_get())
    proximo = (atual + 1) % len(campos_de_entrada)
    campos_de_entrada[proximo].focus_set()

def copiar_todos_campos():
    campos_nomes = [
        "Nome completo:", "E-mail:", "CPF:",
        "Chamado", "Ativos Novos:", "Departamento:", "Usuário:",
        "Modelo Novo:", "Valor:", "Ativo Antigo:", "Modelo Antigo:"
    ]

    valores = []
    for campo, entrada in zip(campos_nomes, campos_de_entrada):
        if isinstance(entrada, ttk.Combobox):
            valor_selecionado = entrada.get()
            if campo == "Modelo Novo:" or campo == "Modelo Antigo:":
                valor_selecionado = modelo_valor_dict.get(valor_selecionado, "")
            valores.append(f"{campo}\n{valor_selecionado}")
        else:
            valor_selecionado = entrada.get()
            valores.append(f"{campo}\n{valor_selecionado}")

    valores_formatados = "\n\n".join(valores)
    pyperclip.copy(valores_formatados)

def exportar_campos():
    usuario = campos_de_entrada[6].get()  # Índice 6 corresponde ao campo "Usuário"
    if usuario:
        campos_nomes = [
            "Nome completo:", "E-mail:", "CPF:",
            "Chamado", "Ativos Novos:", "Departamento:", "Usuário:",
            "Modelo Novo:", "Valor:", "Ativo Antigo:", "Modelo Antigo:"
        ]

        valores = []
        for campo, entrada in zip(campos_nomes, campos_de_entrada):
            if isinstance(entrada, ttk.Combobox):
                valor_selecionado = entrada.get()
                if campo == "Modelo Novo:" or campo == "Modelo Antigo:":
                    valor_selecionado = modelo_valor_dict.get(valor_selecionado, "")
                valores.append(f"{campo}\n{valor_selecionado}")
            else:
                valor_selecionado = entrada.get()
                valores.append(f"{campo}\n{valor_selecionado}")

        valores_formatados = "\n\n".join(valores)
        nome_arquivo = f"{usuario}.txt"

        with open(nome_arquivo, "w") as arquivo:
            arquivo.write(valores_formatados)

        popup = tk.Tk()
        popup.title("Exportado com Sucesso")
        label = tk.Label(popup, text=f"Os campos foram exportados para {nome_arquivo}", padx=10, pady=10)
        label.pack()
        popup.mainloop()
    else:
        popup = tk.Tk()
        popup.title("Erro")
        label = tk.Label(popup, text="Digite o nome de usuário antes de exportar.", padx=10, pady=10)
        label.pack()
        popup.mainloop()

def criar_tela():
    global campos_de_entrada  # Indicar que estamos utilizando a variável global
    global modelo_var  # Indicar que estamos utilizando a variável global modelo_var

    root = tk.Tk()
    root.title("Informações para Termo e Slack")
    root.resizable(width=False, height=False)

    # Obter a largura e altura da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    # Calcular a posição x e y para centralizar a janela
    largura_janela = 360  # Defina a largura desejada da janela
    altura_janela = 600  # Defina a altura desejada da janela

    x_pos = (largura_tela - largura_janela) // 2
    y_pos = (altura_tela - altura_janela) // 2

    # Definir a posição da janela no centro
    root.geometry(f"{largura_janela}x{altura_janela}+{x_pos}+{y_pos}")

    campos = [
        "Nome completo:", "E-mail:", "CPF:",
        "Chamado", "Ativos Novos:", "Departamento:", "Usuário:",
        "Modelo Novo:", "Valor:", "Ativo Antigo:", "Modelo Antigo:"
    ]

    for i, campo in enumerate(campos):
        tk.Label(root, text=campo, bg="#f2f2f2", fg="black").grid(row=i, column=0, padx=0, pady=10)
        entrada = tk.Entry(root)
        entrada.grid(row=i, column=1, padx=10, pady=5)
        campos_de_entrada.append(entrada)

        if i not in [7, 10]:  # Adiciona o botão "Copiar" somente para os campos que não são Comboboxes
            botao_copiar = tk.Button(root, text="Copiar", bg="#4CAF50", fg="white", command=lambda indice=i: copiar_texto(indice), takefocus=False)
            botao_copiar.grid(row=i, column=2, padx=0, pady=10)

    # Criar a variável de controle para o Combobox "Modelo Novo"
    modelo_var = tk.StringVar(root)
    modelo_var.set("Selecione um modelo")  # Definir o valor inicial como "Selecione um modelo"

    # Criar o Combobox para o campo "Modelo Novo"
    modelo_menu = ttk.Combobox(root, textvariable=modelo_var, values=list(modelo_valor_dict.keys()), state="readonly")
    modelo_menu.grid(row=7, column=1, padx=30, pady=5)
    campos_de_entrada.append(modelo_menu)  # Adicionar o objeto Combobox à lista

    # Adicionar evento para preencher automaticamente o campo "Valor" ao selecionar um modelo novo
    modelo_menu.bind("<<ComboboxSelected>>", preencher_valor)

    # Criar a variável de controle para o Combobox "Modelo Antigo"
    modelo_antigo_var = tk.StringVar(root)
    modelo_antigo_var.set("Selecione um modelo")  # Definir o valor inicial como "Selecione um modelo"

    # Criar o Combobox para o campo "Modelo Antigo"
    modelo_antigo_menu = ttk.Combobox(root, textvariable=modelo_antigo_var, values=list(modelo_valor_dict.keys()), state="readonly")
    modelo_antigo_menu.grid(row=10, column=1, padx=30, pady=5)
    campos_de_entrada.append(modelo_antigo_menu)  # Adicionar o objeto Combobox à lista

    # Adicionar evento para preencher automaticamente o campo "Valor" ao selecionar um modelo antigo
    modelo_antigo_menu.bind("<<ComboboxSelected>>", preencher_valor)

    # Adicionar os eventos para preencher automaticamente o campo "Usuário"
    campos_de_entrada[1].bind("<KeyRelease>", preencher_usuario)

    # Adicionar evento para validar o CPF e mudar a cor do texto
    campos_de_entrada[2].bind("<KeyRelease>", validar_cpf)
    # Adicionar evento para pular para o próximo campo ao pressionar "Tab"
    for i, campo in enumerate(campos_de_entrada):
        campo.bind("<Tab>", lambda event, root=root: proximo_campo(event, root))

    botao_limpar = tk.Button(root, text="Limpar Campos", bg="#f44336", fg="white", command=limpar_campos)
    botao_limpar.grid(row=len(campos), column=0, columnspan=3, padx=10, pady=1)

    botao_exportar = tk.Button(root, text="Exportar", bg="#FFC107", fg="black", command=exportar_campos)
    botao_exportar.grid(row=len(campos)+1, column=0, columnspan=3, padx=10, pady=1)

    botao_copiar_todos = tk.Button(root, text="Copiar", bg="#2196F3", fg="white", command=copiar_todos_campos)
    botao_copiar_todos.grid(row=len(campos)+2, column=0, columnspan=3, padx=10, pady=1)

    root.mainloop()

if __name__ == "__main__":
    criar_tela()


