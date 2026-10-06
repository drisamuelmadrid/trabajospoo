"""
Ejercicio 8.2
"""
import math
import tkinter as tk
from tkinter import messagebox


class Notas:
    def __init__(self):
        self.lista_notas = [0.0] * 5

    def calcular_promedio(self):
        suma = 0.0

        for i in range(len(self.lista_notas)):
            suma = suma + self.lista_notas[i]
        return suma / len(self.lista_notas)

    def calcular_desviacion(self):
        prom = self.calcular_promedio()
        suma = 0.0

        for i in range(len(self.lista_notas)):
            suma += math.pow(self.lista_notas[i] - prom, 2)
        return math.sqrt(suma / len(self.lista_notas))

    def calcular_menor(self):
        menor = self.lista_notas[0]
        for i in range(len(self.lista_notas)):
            if self.lista_notas[i] < menor:
                menor = self.lista_notas[i]
        return menor

    def calcular_mayor(self):
        mayor = self.lista_notas[0]
        for i in range(len(self.lista_notas)):
            if self.lista_notas[i] > mayor:
                mayor = self.lista_notas[i]
        return mayor


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.campos_nota = []  
        self._inicio()
        self.title("Notas")                      
        self._centrar(280, 380)                  
        self.resizable(False, False)             

    def _centrar(self, ancho, alto):
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _inicio(self):
        # Etiquetas y campos de las 5 notas (y = 20, 50, 80, 110, 140)
        for i in range(5):
            y = 20 + 30 * i
            etiqueta = tk.Label(self, text=f"Nota {i + 1}:", anchor="w")
            etiqueta.place(x=20, y=y, width=80, height=23)
            campo = tk.Entry(self)
            campo.place(x=105, y=y, width=135, height=23)
            self.campos_nota.append(campo)

        # Botones (command= equivale a addActionListener)
        self.calcular = tk.Button(self, text="Calcular", command=self._calcular)
        self.calcular.place(x=20, y=170, width=100, height=23)
        self.limpiar = tk.Button(self, text="Limpiar", command=self._limpiar)
        self.limpiar.place(x=125, y=170, width=80, height=23)

        # Etiquetas de resultados
        self.promedio = tk.Label(self, text="Promedio = ", anchor="w")
        self.promedio.place(x=20, y=210, width=200, height=23)
        self.desviacion = tk.Label(self, text="Desviación estándar = ", anchor="w")
        self.desviacion.place(x=20, y=240, width=200, height=23)
        self.mayor = tk.Label(self, text="Valor mayor = ", anchor="w")
        self.mayor.place(x=20, y=270, width=200, height=23)
        self.menor = tk.Label(self, text="Valor menor = ", anchor="w")
        self.menor.place(x=20, y=300, width=200, height=23)

    def _leer_notas(self):
        textos = [campo.get().strip() for campo in self.campos_nota]

        # Parte propuesta 2: todas las notas son obligatorias
        faltantes = [i for i, t in enumerate(textos) if t == ""]
        if faltantes:
            lista = ", ".join(f"Nota {i + 1}" for i in faltantes)
            messagebox.showwarning(
                "Nota sin ingresar",
                f"Es obligatorio ingresar las cinco notas.\nFalta: {lista}")
            self.campos_nota[faltantes[0]].focus_set()
            return None

        # Parte propuesta 1: solo se aceptan datos numéricos
        valores = []
        for i, texto in enumerate(textos):
            try:
                valor = float(texto.replace(",", "."))  # acepta 4,5 y 4.5
                if not math.isfinite(valor):            # rechaza "nan" e "inf"
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Dato no numérico",
                    f"La Nota {i + 1} no es un número válido: '{texto}'")
                self.campos_nota[i].focus_set()
                return None
            valores.append(valor)
        return valores

    def _calcular(self):
        valores = self._leer_notas()
        if valores is None:
            return
        notas = Notas()
        notas.lista_notas = valores
        self.promedio.config(text=f"Promedio = {notas.calcular_promedio():.2f}")
        self.desviacion.config(text=f"Desviación estándar = {notas.calcular_desviacion():.2f}")
        self.mayor.config(text=f"Valor mayor = {notas.calcular_mayor()}")
        self.menor.config(text=f"Valor menor = {notas.calcular_menor()}")

    def _limpiar(self):
        for campo in self.campos_nota:
            campo.delete(0, tk.END)
        self.promedio.config(text="Promedio = ")
        self.desviacion.config(text="Desviación estándar = ")
        self.mayor.config(text="Valor mayor = ")
        self.menor.config(text="Valor menor = ")
        self.campos_nota[0].focus_set()


if __name__ == "__main__":
    mi_ventana_principal = VentanaPrincipal()   # crea la ventana
    mi_ventana_principal.mainloop()             # la muestra (equivale a setVisible(true))