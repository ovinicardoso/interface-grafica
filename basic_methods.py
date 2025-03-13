import tkinter as tk
from tkinter import messagebox
import random
import itertools
import math


class BasicMethodsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Métodos Básicos")
        self.geometry("700x600")  # Janela maior

        # Variáveis de controle
        self.points = []
        self.problem_mode = tk.StringVar(value="fixed")
        self.custom_size = tk.StringVar()

        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Seção de configuração do problema
        problem_frame = tk.LabelFrame(
            main_frame, text="Definição do Problema", padx=10, pady=10)
        problem_frame.pack(fill="x", pady=5)

        # Radio buttons para configuração
        tk.Radiobutton(problem_frame,
                       text="Configuração Fixa (5 cidades)",
                       variable=self.problem_mode,
                       value="fixed").pack(anchor="w")

        var_frame = tk.Frame(problem_frame)
        var_frame.pack(anchor="w")
        tk.Radiobutton(var_frame,
                       text="Configuração Variável",
                       variable=self.problem_mode,
                       value="variable").pack(side="left")
        self.custom_size_entry = tk.Entry(var_frame,
                                          textvariable=self.custom_size,
                                          width=5,
                                          state="disabled")
        self.custom_size_entry.pack(side="left", padx=5)
        tk.Label(var_frame, text="cidades").pack(side="left")

        # Botão gerar problema
        tk.Button(problem_frame,
                  text="Gerar Problema",
                  command=self.generate_problem).pack(pady=10)

        # Canvas para visualização
        self.canvas = tk.Canvas(main_frame, bg="white", width=650, height=300)
        self.canvas.pack(fill="both", expand=True, pady=10)

        # Seção de métodos
        methods_frame = tk.LabelFrame(
            main_frame, text="Seleção de Métodos", padx=10, pady=10)
        methods_frame.pack(fill="x", pady=5)

        self.methods = ["Força Bruta", "Vizinho Mais Próximo"]
        self.selected_method = tk.StringVar(value=self.methods[0])

        tk.OptionMenu(methods_frame, self.selected_method, *
                      self.methods).pack(side="left", padx=10)
        tk.Button(methods_frame,
                  text="Executar",
                  command=self.execute_method).pack(side="left", padx=10)

        # Configurar estado da entrada
        self.problem_mode.trace_add("write", self.update_entry_state)

    def update_entry_state(self, *args):
        if self.problem_mode.get() == "variable":
            self.custom_size_entry.config(state="normal")
        else:
            self.custom_size_entry.config(state="disabled")

    def generate_problem(self):
        try:
            if self.problem_mode.get() == "fixed":
                size = 5
            else:
                size = int(self.custom_size.get())
                if size < 2:
                    raise ValueError
        except ValueError:
            messagebox.showerror(
                "Erro", "Tamanho inválido! Digite um número inteiro ≥2")
            return

        self.canvas.delete("all")
        self.points = [(random.randint(50, 600), random.randint(30, 270))
                       for _ in range(size)]

        # Ajustar o tamanho das bolinhas e da fonte com base no número de cidades
        if size <= 10:
            radius = 15  # Raio das bolinhas
            font_size = 10  # Tamanho da fonte
        elif size <= 20:
            radius = 12
            font_size = 9
        else:
            radius = 10
            font_size = 8

        # Desenhar pontos com numeração dentro das bolinhas
        for i, (x, y) in enumerate(self.points):
            self.canvas.create_oval(
                x-radius, y-radius, x+radius, y+radius, fill="blue", outline="black")
            self.canvas.create_text(x, y, text=str(
                i+1), fill="white", font=("Arial", font_size))

    def execute_method(self):
        if not self.points:
            messagebox.showerror("Erro", "Gere o problema primeiro!")
            return

        method = self.selected_method.get()
        if method == "Vizinho Mais Próximo":
            route = self.nearest_neighbor()
        elif method == "Força Bruta":
            route = self.brute_force()

        # Exibir a rota no gráfico
        self.draw_route(route)

        # Exibir a rota encontrada
        # Índices das cidades na rota
        route_indices = [self.points.index(point) for point in route]
        route_description = " -> ".join(
            [f"Cidade {i+1}" for i in route_indices])
        # Volta ao início
        route_description += f" -> Cidade {route_indices[0]+1}"

        messagebox.showinfo(
            "Rota Calculada",
            f"Método utilizado: {method}\n\n"
            f"Rota encontrada:\n{route_description}\n\n"
            f"Distância total: {self.calculate_distance(route):.2f} unidades"
        )

    def nearest_neighbor(self):
        unvisited = self.points.copy()
        current = unvisited.pop(0)
        route = [current]

        while unvisited:
            nearest = min(unvisited, key=lambda x: self.distance(current, x))
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest

        return route

    def brute_force(self):
        if len(self.points) > 8:
            messagebox.showwarning(
                "Aviso", "Força Bruta é lento para mais de 8 cidades!")
            return self.points

        shortest_route = None
        shortest_distance = float("inf")

        for perm in itertools.permutations(self.points):
            distance = self.calculate_distance(perm)
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_route = perm

        return list(shortest_route)

    def draw_route(self, route):
        self.canvas.delete("line")  # Remove rotas anteriores
        for i in range(len(route) - 1):
            x1, y1 = route[i]
            x2, y2 = route[i + 1]
            self.canvas.create_line(
                x1, y1, x2, y2, fill="red", width=2, tags="line")

        # Conectar a última cidade à primeira
        x1, y1 = route[-1]
        x2, y2 = route[0]
        self.canvas.create_line(
            x1, y1, x2, y2, fill="red", width=2, tags="line")

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def calculate_distance(self, route):
        return sum(self.distance(route[i], route[i + 1]) for i in range(len(route) - 1))
