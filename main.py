import collections
import tkinter as tk
from tkinter import ttk
import json

def carregar_tarefas_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    tarefas = []
    for item in dados:
        tarefas.append(
            Tarefa(
                item["nome"],
                item["inicio"],
                item["fim"],
                item["lucro"]
            )
        )

    return tarefas


Tarefa = collections.namedtuple('Tarefa', ['id', 'inicio', 'fim', 'prioridade'])

def encontrar_predecessor_compativel(tarefas_ordenadas, i):
    inicio = 0
    fim = i - 1
    p_i = 0
    tempo_inicio_atual = tarefas_ordenadas[i].inicio

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if tarefas_ordenadas[meio].fim <= tempo_inicio_atual:
            p_i = meio + 1
            inicio = meio + 1
        else:
            fim = meio - 1

    return p_i

def agendamento_intervalo_ponderado_pd(tarefas):
    tarefas_ordenadas = sorted(tarefas, key=lambda t: t.fim)
    n = len(tarefas_ordenadas)

    M = [0] * (n + 1)
    solucao = [False] * (n + 1)
    passos = []

    for i in range(1, n + 1):
        t = tarefas_ordenadas[i - 1]
        v_i = t.prioridade
        p_i = encontrar_predecessor_compativel(tarefas_ordenadas, i - 1)

        opcao1 = M[i - 1]
        opcao2 = v_i + M[p_i]

        if opcao2 >= opcao1:
            M[i] = opcao2
            solucao[i] = True
        else:
            M[i] = opcao1
            solucao[i] = False

        passos.append({
            "i": i,
            "id": t.id,
            "inicio": t.inicio,
            "fim": t.fim,
            "prioridade": t.prioridade,
            "p_i": p_i,
            "M_i_1": opcao1,
            "M_p_i_v_i": opcao2,
            "M_i": M[i],
            "incluiu": solucao[i]
        })

    selecionadas = []
    k = n
    while k > 0:
        if solucao[k]:
            selecionadas.append(tarefas_ordenadas[k - 1])
            k = encontrar_predecessor_compativel(tarefas_ordenadas, k - 1)
        else:
            k -= 1

    selecionadas.reverse()
    return M[n], tarefas_ordenadas, selecionadas, passos

# INTERFACE GRAFICA
class AgendamentoApp:
    def __init__(self, master, tarefas):
        self.master = master
        master.title("Programação Dinâmica: Agendamento de Tarefas")
        master.geometry("1400x800")

        style = ttk.Style()
        style.configure("Treeview", rowheight=35, font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        self.tarefas = tarefas
        self.criar_widgets()
        self.executar_algoritmo()

    def criar_widgets(self):
        main = ttk.Frame(self.master, padding=10)
        main.pack(fill='both', expand=True)

        header = ttk.Frame(main)
        header.pack(fill='x')

        ttk.Label(header, text="Algoritmo de Agendamento Ponderado (PD)",
                  font=("Arial", 16, "bold")).pack(side='left')

        self.resultado = ttk.Label(header, text="prioridade Máximo:",
                                   font=("Arial", 14, "bold"), foreground="green")
        self.resultado.pack(side='right')

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill='both', expand=True)

        self.criar_aba_entrada()
        self.criar_aba_processo_pd()
        self.criar_aba_agendamento_final()

    def criar_treeview(self, parent, colunas, larguras):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True)

        tree = ttk.Treeview(frame, columns=colunas, show="headings")

        for col, largura in zip(colunas, larguras):
            tree.heading(col, text=col)
            tree.column(col, width=largura, anchor='center')

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        return tree

    def criar_aba_entrada(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📌 Tarefas de Entrada")

        cols = ["ID", "Início", "Fim", "prioridade"]
        larg = [120, 120, 120, 120]

        self.tree_entrada = self.criar_treeview(tab, cols, larg)

        for t in self.tarefas:
            self.tree_entrada.insert("", tk.END, values=(t.id, t.inicio, t.fim, t.prioridade))

    def criar_aba_processo_pd(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📘 Processo PD (Tabela M)")

        cols = ["i", "Tarefa", "Início", "Fim", "prioridade", "p(i)",
                "M[i-1]", "M[p(i)] + prioridade", "M[i]"]

        larg = [70, 80, 90, 90, 90, 70, 140, 180, 120, 100]

        self.tree_pd = self.criar_treeview(tab, cols, larg)

    def criar_aba_agendamento_final(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🏆 Agendamento Final")

        cols = ["ID", "Início", "Fim", "prioridade"]
        larg = [160, 160, 160, 160]

        self.tree_final = self.criar_treeview(tab, cols, larg)

    def executar_algoritmo(self):
        prioridade, ordenadas, finais, passos = agendamento_intervalo_ponderado_pd(self.tarefas)

        self.resultado.config(text=f"prioridade Máxima: {prioridade}")

        for p in passos:
            self.tree_pd.insert("", tk.END, values=(
                p["i"], p["id"], p["inicio"], p["fim"], p["prioridade"],
                p["p_i"], p["M_i_1"], p["M_p_i_v_i"], p["M_i"]
            ))

        for t in finais:
            self.tree_final.insert("", tk.END, values=(t.id, t.inicio, t.fim, t.prioridade))



if __name__ == "__main__":
    root = tk.Tk()
    tarefas = carregar_tarefas_json("input.json")
    app = AgendamentoApp(root, tarefas)
    root.mainloop()