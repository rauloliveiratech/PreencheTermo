import tkinter as tk
import pyperclip

campos_de_entrada = []
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

# Definição da lista de campos
campos = [
    "Nome completo:", "E-mail:", "CPF:",
    "Chamado", "Ativos Novos:", "Departamento:", "Usuário:",
    "Valor:", "Modelo Novo:", "Ativos Antigos:", "Modelo Antigo:"
]

def copiar_texto(indice):
    texto = campos_de_entrada[indice].get()
    pyperclip.copy(texto)

def limpar_campos():
    for entrada in campos_de_entrada:
        entrada.delete(0, tk.END)

def preencher_usuario(event):
    email = campos_de_entrada[1].get()
    if "@" in email:
        usuario = email.split("@")[0]
        campos_de_entrada[6].config(state=tk.NORMAL)  # Habilitar o campo para atualizar o valor
        campos_de_entrada[6].delete(0, tk.END)
        campos_de_entrada[6].insert(0, usuario)
        campos_de_entrada[6].config(state=tk.DISABLED)  # Desabilitar o campo novamente

def validar_cpf(event):
    cpf = campos_de_entrada[2].get()
    if len(cpf) == 11 and cpf.isdigit():
        campos_de_entrada[2].config(fg='green')
    else:
        campos_de_entrada[2].config(fg='red')

def preencher_valor(event):
    modelo = campos_de_entrada[8].get().upper()
    valor = modelo_valor_dict.get(modelo, "")
    campos_de_entrada[7].config(state=tk.NORMAL)  # Habilitar o campo para atualizar o valor
    campos_de_entrada[7].delete(0, tk.END)
    campos_de_entrada[7].insert(0, valor)
    campos_de_entrada[7].config(state=tk.DISABLED)  # Desabilitar o campo novamente

def proximo_campo(event):
    atual = campos_de_entrada.index(event.widget)
    proximo = (atual + 1) % len(campos_de_entrada)
    campos_de_entrada[proximo].focus_set()

def copiar_todos_campos():
    valores = []
    for i, entrada in enumerate(campos_de_entrada):
        valor_selecionado = entrada.get()
        campo = campos[i]
        valores.append(f"{campo} {valor_selecionado}")

    valores_formatados = "\n\n".join(valores)
    pyperclip.copy(valores_formatados)

def exportar_campos():
    usuario = campos_de_entrada[6].get()
    if usuario:
        campos_formatados = [
            "Nome completo:", "E-mail:", "CPF:",
            "Chamado", "Ativos Novos:", "Departamento:", "Usuário:",
            "Valor:", "Modelo Novo:", "Ativos Antigos:", "Modelo Antigo:"
        ]
        for i, entrada in enumerate(campos_de_entrada):
            valor_selecionado = entrada.get()
            campos_formatados[i] = f"{campos_formatados[i]} {valor_selecionado}\n"

        nome_arquivo = f"{usuario}.txt"

        with open(nome_arquivo, "w") as arquivo:
            arquivo.writelines(campos_formatados)

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
    global campos_de_entrada

    root = tk.Tk()
    root.title("Informações para Termo e Slack")
    root.resizable(width=False, height=False)

    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()

    largura_janela = 300
    altura_janela = 600

    x_pos = (largura_tela - largura_janela) // 2
    y_pos = (altura_tela - altura_janela) // 2

    root.geometry(f"{largura_janela}x{altura_janela}+{x_pos}+{y_pos}")

    for i, campo in enumerate(campos):
        tk.Label(root, text=campo, bg="#f2f2f2", fg="black").grid(row=i, column=0, padx=0, pady=10)
        entrada = tk.Entry(root)
        entrada.grid(row=i, column=1, padx=10, pady=5)
        campos_de_entrada.append(entrada)

        botao_copiar = tk.Button(root, text="Copiar", bg="#4CAF50", fg="white", command=lambda indice=i: copiar_texto(indice), takefocus=False)
        botao_copiar.grid(row=i, column=2, padx=0, pady=10)

    campos_de_entrada[1].bind("<KeyRelease>", preencher_usuario)
    campos_de_entrada[2].bind("<KeyRelease>", validar_cpf)
    campos_de_entrada[8].bind("<KeyRelease>", preencher_valor)

    for campo in campos_de_entrada:
        campo.bind("<Tab>", proximo_campo)

    campos_de_entrada[6].config(state=tk.DISABLED)  # Inicialmente, o campo "Usuário" é desabilitado
    campos_de_entrada[7].config(state=tk.DISABLED)  # Inicialmente, o campo "Valor" é desabilitado

    botao_limpar = tk.Button(root, text="Limpar Campos", bg="#f44336", fg="white", command=limpar_campos)
    botao_limpar.grid(row=len(campos), column=0, columnspan=3, padx=10, pady=1)

    botao_exportar = tk.Button(root, text="Exportar", bg="#FFC107", fg="black", command=exportar_campos)
    botao_exportar.grid(row=len(campos)+1, column=0, columnspan=3, padx=10, pady=1)

    botao_copiar_todos = tk.Button(root, text="Copiar", bg="#2196F3", fg="white", command=copiar_todos_campos)
    botao_copiar_todos.grid(row=len(campos)+2, column=0, columnspan=3, padx=10, pady=1)

    root.mainloop()

if __name__ == "__main__":
    criar_tela()
