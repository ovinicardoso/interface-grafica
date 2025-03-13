import tkinter as tk
from basic_methods import BasicMethodsWindow
from description import DescriptionWindow


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Problema do Caixeiro Viajante")
        self.geometry("500x400")  # Janela maior

        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, pady=20)

        # Cabeçalho
        tk.Label(main_frame,
                 text="Problema do Caixeiro Viajante",
                 font=("Arial", 16, "bold")).pack(pady=20)

        # Botões para as diferentes opções
        tk.Button(main_frame, text="Métodos Básicos",
                  command=self.open_basic_methods, width=25).pack(pady=8)
        tk.Button(main_frame, text="Algorítmos Genéticos",
                  command=self.open_genetic_algorithms, width=25).pack(pady=8)
        tk.Button(main_frame, text="Descrição do Problema",
                  command=self.open_description, width=25).pack(pady=8)

    def open_basic_methods(self):
        BasicMethodsWindow(self)

    def open_genetic_algorithms(self):
        pass

    def open_description(self):
        DescriptionWindow(self)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
