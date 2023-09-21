from logging import root
import tkinter as tk
import pyperclip

campos_de_entrada = []
modelo_valor_dict = {
    "PC701": "R$2.000,00",
    "UL151": "R$3.665,69",
    "UL152TI": "R$3.887,17",
    "UL152": "R$3.887,17",
    "UL124": "R$4.121,60",
    "UL121": "R$4.121,60",
    "UB536": "R$2.225,13",
    "UB523": "R$2.225,13",
    "IMAC": "R$16.000,00",
    "MACBOOK": "R$18.000,00",
    "RAUL": "xD",
    "Nokia 5.4": "R$1.315,03",
    "Nokia 2.4": "R$911,34",
    "Nokia G21": "R$1.582,02",
    "G PRO": "R$618,97",
    "G": "R$498,18"
}

# Definição da lista de campos
col1 = ["Nome completo:", "E-mail:", "CPF:", "Chamado"]
col2 = ["Ativos Novos:", "Departamento:", "Usuário:", "Valor:",
        "Modelo Novo:", "Ativos Antigos:", "Modelo Antigo:"]


def copiar_texto(indice):
    texto = campos_de_entrada[indice].get()
    pyperclip.copy(texto)


def limpar_campos():
    for entrada in campos_de_entrada:
        entrada.delete(0, tk.END)

    # Redefinir os campos Usuário e Valor
    campos_de_entrada[6].config(state=tk.NORMAL)
    campos_de_entrada[6].delete(0, tk.END)
    campos_de_entrada[6].config(state=tk.DISABLED)

    campos_de_entrada[7].config(state=tk.NORMAL)
    campos_de_entrada[7].delete(0, tk.END)
    campos_de_entrada[7].config(state=tk.DISABLED)


def preencher_usuario(event):
    email = campos_de_entrada[1].get()
    if "@" in email:
        usuario = email.split("@")[0]
        campos_de_entrada[6].config(state=tk.NORMAL)
        campos_de_entrada[6].delete(0, tk.END)
        campos_de_entrada[6].insert(0, usuario)
        campos_de_entrada[6].config(state=tk.DISABLED)


def validar_cpf(event):
    cpf = campos_de_entrada[2].get()
    if len(cpf) == 11 and cpf.isdigit():
        campos_de_entrada[2].config(fg='green')
    else:
        campos_de_entrada[2].config(fg='red')


def preencher_valor(event):
    modelo = campos_de_entrada[8].get().upper()
    valor = modelo_valor_dict.get(modelo, "")
    campos_de_entrada[7].config(state=tk.NORMAL)
    campos_de_entrada[7].delete(0, tk.END)
    campos_de_entrada[7].insert(0, valor)
    campos_de_entrada[7].config(state=tk.DISABLED)


def proximo_campo(event):
    atual = campos_de_entrada.index(event.widget)
    proximo = (atual + 1) % len(campos_de_entrada)
    campos_de_entrada[proximo].focus_set()


def copiar_todos_campos():
    valores = []
    for i, entrada in enumerate(campos_de_entrada):
        valor_selecionado = entrada.get()
        if i < len(col1):
            campo = col1[i]
        else:
            campo = col2[i - len(col1)]
        valores.append(f"{campo} {valor_selecionado}")

    valores_formatados = "\n\n".join(valores)
    pyperclip.copy(valores_formatados)


def exportar_campos():
    usuario = campos_de_entrada[6].get()
    if usuario:
        campos_formatados = []
        campos_formatados.extend(col1)
        campos_formatados.extend(col2)
        for i, entrada in enumerate(campos_de_entrada):
            valor_selecionado = entrada.get()
            campos_formatados[i] = f"{campos_formatados[i]} {valor_selecionado}\n"

        nome_arquivo = f"{usuario}.txt"

        with open(nome_arquivo, "w") as arquivo:
            arquivo.writelines(campos_formatados)

        popup = tk.Tk()
        popup.title("Exportado com Sucesso")
        label = tk.Label(
            popup, text=f"Os campos foram exportados para {nome_arquivo}", padx=10, pady=10)
        label.pack()
        popup.mainloop()
    else:
        popup = tk.Tk()
        popup.title("Erro")
        label = tk.Label(
            popup, text="Digite o nome de usuário antes de exportar.", padx=10, pady=10)
        label.pack()
        popup.mainloop()


def criar_tela():
    global campos_de_entrada

    root = tk.Tk()
    root.title("Informações para Termo e Slack")
    root.resizable(width=False, height=False)

    largura_janela = 630
    altura_janela = 260

    x_pos = (root.winfo_screenwidth() - largura_janela) // 2
    y_pos = (root.winfo_screenheight() - altura_janela) // 2

    root.geometry(f"{largura_janela}x{altura_janela}+{x_pos}+{y_pos}")

    for i, campo in enumerate(col1):
        tk.Label(root, text=campo, bg="#f2f2f2", fg="black").grid(
            row=i, column=0, padx=10, pady=5, sticky="e")
        entrada = tk.Entry(root)
        entrada.grid(row=i, column=1, padx=10, pady=5)
        campos_de_entrada.append(entrada)

        botao_copiar = tk.Button(root, text="Copiar", bg="#4CAF50", fg="white",
                                 command=lambda indice=i: copiar_texto(indice), takefocus=False)
        botao_copiar.grid(row=i, column=2, padx=0, pady=5, sticky="w")

    for i, campo in enumerate(col2):
        tk.Label(root, text=campo, bg="#f2f2f2", fg="black").grid(
            row=i, column=3, padx=10, pady=5, sticky="e")
        entrada = tk.Entry(root)
        entrada.grid(row=i, column=4, padx=10, pady=5)
        campos_de_entrada.append(entrada)

        botao_copiar = tk.Button(root, text="Copiar", bg="#4CAF50", fg="white",
                                 command=lambda indice=i+len(col1): copiar_texto(indice), takefocus=False)
        botao_copiar.grid(row=i, column=5, padx=0, pady=5, sticky="w")

    campos_de_entrada[1].bind("<KeyRelease>", preencher_usuario)
    campos_de_entrada[2].bind("<KeyRelease>", validar_cpf)
    campos_de_entrada[8].bind("<KeyRelease>", preencher_valor)

    for campo in campos_de_entrada:
        campo.bind("<Tab>", proximo_campo)

    botao_limpar = tk.Button(root, text="Limpar Campos",
                             bg="#f44336", fg="white", command=limpar_campos, width=20)
    botao_limpar.grid(row=4, column=0, columnspan=3,
                      padx=35, pady=5, sticky="e")

    botao_exportar = tk.Button(
        root, text="Exportar", bg="#FFC107", fg="black", command=exportar_campos, width=20)
    botao_exportar.grid(row=5, column=0, columnspan=3,
                        padx=35, pady=5, sticky="e")

    botao_copiar_todos = tk.Button(
        root, text="Copiar", bg="#2196F3", fg="white", command=copiar_todos_campos, width=20)
    botao_copiar_todos.grid(row=6, column=0, columnspan=3,
                            padx=35, pady=5, sticky="e")
    limpar_campos()
    root.mainloop()


if __name__ == "__main__":
    criar_tela()
