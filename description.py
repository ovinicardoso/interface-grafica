import tkinter as tk


class DescriptionWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Descrição do Problema")
        self.geometry("400x300")

        description_text = (
            "O Problema do Caixeiro Viajante (TSP) é um dos problemas mais famosos na área de otimização.\n\n"
            "O objetivo é encontrar o caminho mais curto possível que visita cada cidade exatamente uma vez e retorna à cidade de origem.\n\n"
            "Este problema é NP-difícil, o que significa que não existe uma solução eficiente para todos os casos."
        )

        tk.Label(self, text=description_text, wraplength=380,
                 justify="left").pack(expand=True, padx=10, pady=10)
