# Agendamento de processos a partir de prioridade (Weighted Interval Scheduling) 

Nesse projeto implementamos o problema de agendamento de processos em um SO de forma ponderada, utilizando o algoritmo **Weighted Interval Scheduling**, ou seja, resolvendo um problema por  **Programação Dinâmica (PD)** para selecionar o conjunto ótimo de processos/tarefas que **maximiza a prioridade** sem conflitos de tempo.

Além da implementação do algoritmo, incluímos uma interface
gráfica em Tkinter, que permite visualizar:

-   Tarefas de entrada;
-   O processo passo a passo da tabela de PD;
-   O agendamento final ótimo;
-   O lucro máximo alcançado.


## Tecnologias utilizadas

-   **Python 3**
-   **Tkinter**: criação da interface gráfica
-   **Collections (namedtuple)**: estrutura leve para definir tarefas


## Principais componentes do projeto

-   `Tarefa`: estrutura contendo `{id, inicio, fim, lucro}`
-   `encontrar_predecessor_compativel(...)`: cálculo via busca binária
-   `agendamento_intervalo_ponderado_pd(...)`: algoritmo de PD
-   `AgendamentoApp`: interface gráfica que exibe todo o processo


## Como Executar

### 1. Certifique-se de ter o Python e tkinter instalados

Recomendado: **Python 3.8+**

### 2. Execute o script principal

``` bash
python3 main.py
```

### 3. A interface será aberta mostrando:

-   As tarefas de entrada
-   A tabela completa de decisões da Programação Dinâmica
-   O conjunto ótimo final selecionado

Cabe lembrar que as tarefas, prioridades e outros dados podem ser alterados no código (JSON) para demais testes.

## Compreendendo a interface

A interface contém três abas:

1.  **Tarefas de entrada**:
    Lista todas as tarefas fornecidas ao algoritmo e seus dados.

2.  **Processo PD (Tabela M)**:
    Mostra, passo a passo:

    -   índice `i`;
    -   tarefa analisada;
    -   predecessor `p(i)`;
    -   valores comparados;
    -   decisão (incluiu ou não).

3.  **Agendamento final**:
    Mostra exatamente quais tarefas compõem o conjunto ótimo.


## Autores

Dupla responsável: **21**

- [Júlia Fortunato](https://github.com/julia-fortunato)
- [Maurício Ferreira](https://github.com/mauricio-araujoo)


## Vídeo de Apresentação

- [Vídeo de apresentação]()