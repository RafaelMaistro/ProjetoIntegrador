import tkinter as tk
from tkinter import messagebox
import random
import mysql.connector

def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",       
        user="root",            
        password="imtdb",   
        database="jogo_educacional"
    )

# Base de perguntas por matéria
banco_perguntas = {
    "Matemática": [
        ("Quanto é 7 x 8?", "54", "56", "63", "58", "60", "B"),
        ("Qual é a metade de 50?", "20", "10", "25", "30", "15", "C"),
        ("Quanto é 10²?", "100", "20", "110", "10", "120", "A")
    ],
    "Português": [
        ("Qual é o antônimo de 'feliz'?", "contente", "alegre", "triste", "divertido", "animado", "C"),
        ("Qual é a forma correta: 'há anos atrás' ou 'há anos'?", "'há anos atrás'", "'há anos'", "'anos atrás'", "'há ano atrás'", "'há ano'", "B"),
        ("Qual é a classe gramatical da palavra 'rapidamente'?", "substantivo", "verbo", "adjetivo", "advérbio", "conjunção", "D")
    ],
    "História": [
        ("Quem foi o primeiro presidente do Brasil?", "Getúlio Vargas", "Marechal Deodoro", "Dom Pedro II", "Lula", "Juscelino Kubitschek", "B"),
        ("Em que ano ocorreu a Proclamação da República?", "1889", "1822", "1500", "1989", "1922", "A"),
        ("Quem descobriu o Brasil?", "Pedro Álvares Cabral", "Cristóvão Colombo", "Vasco da Gama", "Dom João VI", "Tiradentes", "A")
    ],
    "Geografia": [
        ("Qual é o maior país do mundo em extensão territorial?", "Canadá", "Brasil", "China", "Estados Unidos", "Rússia", "E"),
        ("Qual é o rio mais extenso do mundo?", "Amazonas", "Nilo", "Yangtzé", "Mississippi", "Danúbio", "B"),
        ("O que é uma ilha?", "Montanha", "Porção de terra cercada de água", "Deserto", "Vale", "Glaciar", "B")
    ]
}

ranking = []

class ShowDoMilhaoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Show do Milhão")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#f0f0f0")

        self.usuario = None
        self.materia = None
        self.serie = None

        self.tela_login_aluno()

    def tela_login_aluno(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(frame, text="Nome de Usuário:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        self.entry_usuario = tk.Entry(frame, font=("Arial", 14))
        self.entry_usuario.pack(pady=10)

        tk.Label(frame, text="Senha:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        self.entry_senha = tk.Entry(frame, show="*", font=("Arial", 14))
        self.entry_senha.pack(pady=10)

        tk.Button(frame, text="🎮 Entrar", font=("Arial", 14), bg="#d0f0d0", command=self.validar_login_aluno).pack(pady=20)
        tk.Button(frame, text="🔐 Login Admin", font=("Arial", 14), bg="#f0d0d0", command=self.tela_login_admin).pack(pady=10)

    def validar_login_aluno(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if usuario and senha:
            self.usuario = usuario
            self.tela_selecao_materia_serie()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def tela_selecao_materia_serie(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(frame, text="Escolha a Matéria:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        self.var_materia = tk.StringVar(value="Matemática")
        materias = ["Matemática", "Português", "História", "Geografia"]
        for materia in materias:
            tk.Radiobutton(frame, text=materia, variable=self.var_materia, value=materia, font=("Arial", 12), bg="#f0f0f0").pack()

        tk.Label(frame, text="Escolha a Série:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        self.var_serie = tk.StringVar(value="1º ano")
        series = ["1º ano", "2º ano", "3º ano"]
        for serie in series:
            tk.Radiobutton(frame, text=serie, variable=self.var_serie, value=serie, font=("Arial", 12), bg="#f0f0f0").pack()

        tk.Button(frame, text="✅ Iniciar Jogo", font=("Arial", 14), bg="#d0f0d0", command=self.iniciar_jogo_aluno).pack(pady=20)

    def iniciar_jogo_aluno(self):
        materia = self.var_materia.get()
        serie = self.var_serie.get()
        ShowDoMilhao(self.root, materia, serie, self.usuario, self.tela_selecao_materia_serie)

    # ========== ADMIN ==========
    def tela_login_admin(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(frame, text="Admin - Usuário:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        self.entry_admin_user = tk.Entry(frame, font=("Arial", 14))
        self.entry_admin_user.pack(pady=10)

        tk.Label(frame, text="Senha:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        self.entry_admin_pass = tk.Entry(frame, show="*", font=("Arial", 14))
        self.entry_admin_pass.pack(pady=10)

        tk.Button(frame, text="Entrar como Admin", font=("Arial", 14), bg="#d0d0f0", command=self.validar_login_admin).pack(pady=20)
        tk.Button(frame, text="⬅ Voltar", font=("Arial", 12), command=self.tela_login_aluno).pack(pady=10)

    def validar_login_admin(self):
        usuario = self.entry_admin_user.get()
        senha = self.entry_admin_pass.get()

        if usuario == "admin" and senha == "1234":
            self.tela_admin()
        else:
            messagebox.showerror("Erro", "Credenciais de administrador inválidas.")

    def tela_admin(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(frame, text="Painel do Administrador", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Button(frame, text="✏️ Editar Questões", font=("Arial", 14), bg="#d0f0ff", command=self.tela_editar_questoes).pack(pady=10)
        tk.Button(frame, text="📊 Visualizar Ranking", font=("Arial", 14), bg="#d0ffd0", command=self.tela_ranking).pack(pady=10)
        tk.Button(frame, text="⬅ Voltar", font=("Arial", 12), command=self.tela_login_aluno).pack(pady=20)

    def tela_editar_questoes(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(frame, text="Edição de Questões", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        self.var_materia_editar = tk.StringVar(value="Matemática")
        tk.Label(frame, text="Escolha a Matéria:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)
        materias = ["Matemática", "Português", "História", "Geografia"]
        for materia in materias:
            tk.Radiobutton(frame, text=materia, variable=self.var_materia_editar, value=materia, font=("Arial", 12), bg="#f0f0f0").pack()

        self.entry_pergunta = tk.Entry(frame, font=("Arial", 14), width=50)
        self.entry_pergunta.pack(pady=10)
        self.entry_resposta_a = tk.Entry(frame, font=("Arial", 14), width=50)
        self.entry_resposta_a.pack(pady=10)
        self.entry_resposta_b = tk.Entry(frame, font=("Arial", 14), width=50)
        self.entry_resposta_b.pack(pady=10)
        self.entry_resposta_c = tk.Entry(frame, font=("Arial", 14), width=50)
        self.entry_resposta_c.pack(pady=10)
        self.entry_resposta_d = tk.Entry(frame, font=("Arial", 14), width=50)
        self.entry_resposta_d.pack(pady=10)
        self.entry_resposta_e = tk.Entry(frame, font=("Arial", 14), width=50)
        self.entry_resposta_e.pack(pady=10)
        self.entry_resposta_correta = tk.Entry(frame, font=("Arial", 14), width=50)
        self.entry_resposta_correta.pack(pady=10)

        tk.Button(frame, text="Adicionar Pergunta", font=("Arial", 14), bg="#d0ff90", command=self.adicionar_pergunta).pack(pady=10)
        tk.Button(frame, text="⬅ Voltar", font=("Arial", 12), command=self.tela_admin).pack(pady=10)

    def adicionar_pergunta(self):
        pergunta = self.entry_pergunta.get()
        resposta_a = self.entry_resposta_a.get()
        resposta_b = self.entry_resposta_b.get()
        resposta_c = self.entry_resposta_c.get()
        resposta_d = self.entry_resposta_d.get()
        resposta_e = self.entry_resposta_e.get()
        resposta_correta = self.entry_resposta_correta.get()

        if pergunta and resposta_a and resposta_b and resposta_c and resposta_d and resposta_e and resposta_correta:
            materia = self.var_materia_editar.get()
            banco_perguntas[materia].append((pergunta, resposta_a, resposta_b, resposta_c, resposta_d, resposta_e, resposta_correta))
            messagebox.showinfo("Sucesso", "Pergunta adicionada com sucesso!")
            self.limpar_campos_edicao()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def limpar_campos_edicao(self):
        self.entry_pergunta.delete(0, tk.END)
        self.entry_resposta_a.delete(0, tk.END)
        self.entry_resposta_b.delete(0, tk.END)
        self.entry_resposta_c.delete(0, tk.END)
        self.entry_resposta_d.delete(0, tk.END)
        self.entry_resposta_e.delete(0, tk.END)
        self.entry_resposta_correta.delete(0, tk.END)

    def tela_ranking(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.place(relx=0.5, rely=0.3, anchor="center")

        tk.Label(frame, text="Ranking de Pontuação", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)
        ranking_ordenado = sorted(ranking, key=lambda x: x[1], reverse=True)
        for i, (nome, pontos) in enumerate(ranking_ordenado[:10], start=1):
            tk.Label(frame, text=f"{i}. {nome} - {pontos} pts", font=("Arial", 12), bg="#f0f0f0").pack()

        tk.Button(frame, text="⬅ Voltar", command=self.tela_admin).pack(pady=20)

class ShowDoMilhao:
    def __init__(self, master, materia, serie, usuario, voltar_menu_callback):
        self.master = master
        self.materia = materia
        self.serie = serie
        self.usuario = usuario
        self.voltar_menu_callback = voltar_menu_callback

        self.pergunta_atual = 0
        self.pontuacao = 0
        self.dica_usada = False
        self.checkpoint = 0

        perguntas_da_materia = banco_perguntas.get(materia, [])
        self.perguntas_embaralhadas = random.sample(perguntas_da_materia, len(perguntas_da_materia))

        for widget in self.master.winfo_children():
            widget.destroy()

        self.criar_widgets()

    def criar_widgets(self):
        self.frame_central = tk.Frame(self.master, bg="#f0f0f0")
        self.frame_central.place(relx=0.5, rely=0.1, anchor="n")

        self.label_pergunta = tk.Label(self.frame_central, text="", font=("Arial", 16), wraplength=700, justify="center", bg="#f0f0f0")
        self.label_pergunta.pack(pady=20)

        self.botoes = []
        self.letras = ["A", "B", "C", "D", "E"]
        for i in range(5):
            botao = tk.Button(self.frame_central, text="", width=50, font=("Arial", 12),
                              command=lambda letra=self.letras[i], idx=i: self.verificar_resposta(letra, idx))
            botao.pack(pady=5)
            self.botoes.append(botao)

        self.botao_dica = tk.Button(self.master, text="💡 Usar Dica (eliminar 2)", command=self.usar_dica, font=("Arial", 12), bg="#ffffcc")
        self.botao_dica.pack(pady=10)

        self.botao_sair = tk.Button(self.master, text="🚪 Sair", command=self.voltar_menu_callback, font=("Arial", 12), bg="#f0d0d0")
        self.botao_sair.pack(pady=10)

        self.label_pontuacao = tk.Label(self.master, text=f"Pontuação: {self.pontuacao}", font=("Arial", 12), bg="#f0f0f0")
        self.label_pontuacao.pack(pady=10, side="bottom")

        self.carregar_pergunta()

    def carregar_pergunta(self):
        if self.pergunta_atual < len(self.perguntas_embaralhadas):
            pergunta = self.perguntas_embaralhadas[self.pergunta_atual]
            self.label_pergunta.config(text=pergunta[0])
            for i in range(5):
                self.botoes[i].config(text=f"{self.letras[i]}) {pergunta[i+1]}", state="normal", bg="SystemButtonFace")
            if not self.dica_usada:
                self.botao_dica.config(state="normal")
        else:
            self.exibir_tela_final()

    def verificar_resposta(self, letra_escolhida, idx_escolhido):
        correta = self.perguntas_embaralhadas[self.pergunta_atual][6]
        letra_correta_idx = self.letras.index(correta)

        for botao in self.botoes:
            botao.config(state="disabled")
        self.botao_dica.config(state="disabled")

        if letra_escolhida == correta:
            self.pontuacao += 100
            self.botoes[idx_escolhido].config(bg="#32CD32")
            self.label_pontuacao.config(text=f"Pontuação: {self.pontuacao}")
            self.pergunta_atual += 1

            if self.pergunta_atual % 3 == 0:
                self.checkpoint = self.pergunta_atual
                messagebox.showinfo("Checkpoint", "Checkpoint alcançado!")

            self.master.after(1000, self.carregar_pergunta)
        else:
            self.botoes[idx_escolhido].config(bg="red")
            self.botoes[letra_correta_idx].config(bg="#32CD32")
            self.label_pontuacao.config(text=f"Pontuação: {self.pontuacao}")
            self.master.after(1000, self.exibir_tela_final)

    def usar_dica(self):
        if self.dica_usada:
            return
        self.dica_usada = True
        self.botao_dica.config(state="disabled")

        correta = self.perguntas_embaralhadas[self.pergunta_atual][6]
        letra_correta_idx = self.letras.index(correta)
        erradas = [i for i in range(5) if i != letra_correta_idx and self.botoes[i]['state'] == "normal"]
        eliminar = random.sample(erradas, 2)

        for i in eliminar:
            self.botoes[i].config(state="disabled")

    def exibir_tela_final(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        final_frame = tk.Frame(self.master, bg="#f0f0f0")
        final_frame.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(final_frame, text=f"Fim de Jogo!\nPontuação: {self.pontuacao} Reais", font=("Arial", 20), bg="#f0f0f0").pack(pady=20)

        ranking.append((self.usuario, self.pontuacao))
        salvar_ranking_mysql(self.usuario, self.pontuacao)


        tk.Button(final_frame, text="🔁 Jogar Novamente", font=("Arial", 14), bg="#d0f0d0", command=self.jogar_novamente).pack(pady=10)
        tk.Button(final_frame, text="🚪 Sair", font=("Arial", 14), bg="#f0d0d0", command=self.voltar_menu_callback).pack(pady=10)

    def jogar_novamente(self):
        self.pergunta_atual = 0
        self.pontuacao = 0
        self.dica_usada = False
        self.checkpoint = 0
        perguntas_da_materia = banco_perguntas.get(self.materia, [])
        self.perguntas_embaralhadas = random.sample(perguntas_da_materia, len(perguntas_da_materia))
        for widget in self.master.winfo_children():
            widget.destroy()
        self.criar_widgets()

# Inicializar o app

root = tk.Tk()
app = ShowDoMilhaoApp(root)
root.mainloop()
