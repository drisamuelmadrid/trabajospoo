"""
Ejercicio 8.3
"""
import math
import tkinter as tk
from tkinter import messagebox

def centrar_ventana(ventana, ancho, alto):
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def leer_numero_positivo(texto):
    texto = texto.strip()
    if texto == "":
        raise ValueError("campo nulo")
    try:
        valor = float(texto.replace(",", "."))  # acepta 1,5 y 1.5
    except ValueError:
        raise ValueError("error en formato de número") from None
    if not math.isfinite(valor):                # rechaza "nan" e "inf"
        raise ValueError("error en formato de número")
    if valor <= 0:
        raise ValueError("debe ser mayor que cero")
    return valor


class FiguraGeometrica:
    def __init__(self):
        self._volumen = 0.0
        self._superficie = 0.0

    def set_volumen(self, volumen):
        self._volumen = volumen

    def set_superficie(self, superficie):
        self._superficie = superficie

    def get_volumen(self):
        return self._volumen

    def get_superficie(self):
        return self._superficie

    def calcular_volumen(self):
        raise NotImplementedError("Cada figura define su propio volumen")

    def calcular_superficie(self):
        raise NotImplementedError("Cada figura define su propia superficie")


class Cilindro(FiguraGeometrica):
    def __init__(self, radio, altura):
        super().__init__()
        self._radio = radio
        self._altura = altura
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        # V = pi * r^2 * h
        return math.pi * self._altura * math.pow(self._radio, 2.0)

    def calcular_superficie(self):
        # S = 2*pi*r*h (lado) + 2*pi*r^2 (dos tapas)
        area_lado_a = 2.0 * math.pi * self._radio * self._altura
        area_lado_b = 2.0 * math.pi * math.pow(self._radio, 2.0)
        return area_lado_a + area_lado_b


class Esfera(FiguraGeometrica):
    def __init__(self, radio):
        super().__init__()
        self._radio = radio
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        # V = (4/3) * pi * r^3   (el libro usa 1.333, aquí se usa 4/3 exacto)
        return (4.0 / 3.0) * math.pi * math.pow(self._radio, 3.0)

    def calcular_superficie(self):
        # S = 4 * pi * r^2
        return 4.0 * math.pi * math.pow(self._radio, 2.0)


class Piramide(FiguraGeometrica):
    """Pirámide de base cuadrada."""

    def __init__(self, base, altura, apotema):
        super().__init__()
        self._base = base
        self._altura = altura
        self._apotema = apotema
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        # V = base^2 * h / 3
        return (math.pow(self._base, 2.0) * self._altura) / 3.0

    def calcular_superficie(self):
        # S = base^2 (área de la base) + 2 * base * apotema (4 triángulos laterales)
        area_base = math.pow(self._base, 2.0)
        area_lado = 2.0 * self._base * self._apotema
        return area_base + area_lado


class Cubo(FiguraGeometrica):

    def __init__(self, arista):
        super().__init__()
        self._arista = arista
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        # V = a^3
        return math.pow(self._arista, 3.0)

    def calcular_superficie(self):
        # S = 6 * a^2
        return 6.0 * math.pow(self._arista, 2.0)


class Prisma(FiguraGeometrica):

    def __init__(self, largo, ancho, altura):
        super().__init__()
        self._largo = largo
        self._ancho = ancho
        self._altura = altura
        self.set_volumen(self.calcular_volumen())
        self.set_superficie(self.calcular_superficie())

    def calcular_volumen(self):
        # V = largo * ancho * altura
        return self._largo * self._ancho * self._altura

    def calcular_superficie(self):
        # S = 2 * (largo*ancho + largo*altura + ancho*altura)
        return 2.0 * (self._largo * self._ancho
                      + self._largo * self._altura
                      + self._ancho * self._altura)


class VentanaFigura(tk.Toplevel):
    titulo = ""
    campos = []
    clase_figura = None

    def __init__(self, padre):
        super().__init__(padre)
        self.entradas = []
        self._inicio()
        self.title(self.titulo)
        centrar_ventana(self, self.ancho, self.alto)
        self.resizable(False, False)

    def _inicio(self):
        n = len(self.campos)
        for i, nombre in enumerate(self.campos):
            y = 20 + 30 * i
            etiqueta = tk.Label(self, text=f"{nombre} (cms):", anchor="w")
            etiqueta.place(x=20, y=y, width=95, height=23)
            entrada = tk.Entry(self)
            entrada.place(x=120, y=y, width=110, height=23)
            self.entradas.append(entrada)

        y_boton = 20 + 30 * n
        self.calcular = tk.Button(self, text="Calcular", command=self._calcular)
        self.calcular.place(x=120, y=y_boton, width=110, height=23)

        y_res = y_boton + 40
        self.volumen = tk.Label(self, text="Volumen (cm3):", anchor="w")
        self.volumen.place(x=20, y=y_res, width=230, height=23)
        self.superficie = tk.Label(self, text="Superficie (cm2):", anchor="w")
        self.superficie.place(x=20, y=y_res + 30, width=230, height=23)

        # Imagen de la figura (parte propuesta)
        self.lienzo = tk.Canvas(self, width=130, height=130, bg="white",
                                highlightthickness=1, highlightbackground="gray")
        self.lienzo.place(x=255, y=20)
        self.dibujar(self.lienzo)

        self.ancho = 400
        self.alto = max(y_res + 30 + 23 + 20, 170)

    def dibujar(self, lienzo):
        pass

    def _calcular(self):
        valores = []
        for nombre, entrada in zip(self.campos, self.entradas):
            try:
                valores.append(leer_numero_positivo(entrada.get()))
            except ValueError as error:
                messagebox.showerror("Error", f"{nombre}: {error}", parent=self)
                entrada.focus_set()
                return
        figura = self.clase_figura(*valores)  # polimorfismo: cualquier figura
        self.volumen.config(text=f"Volumen (cm3): {figura.calcular_volumen():.2f}")
        self.superficie.config(text=f"Superficie (cm2): {figura.calcular_superficie():.2f}")


class VentanaCilindro(VentanaFigura):
    titulo = "Cilindro"
    campos = ["Radio", "Altura"]
    clase_figura = Cilindro

    def dibujar(self, c):
        c.create_oval(30, 20, 100, 40)
        c.create_line(30, 30, 30, 100)
        c.create_line(100, 30, 100, 100)
        c.create_arc(30, 90, 100, 110, start=180, extent=180, style=tk.ARC)


class VentanaEsfera(VentanaFigura):
    titulo = "Esfera"
    campos = ["Radio"]
    clase_figura = Esfera

    def dibujar(self, c):
        c.create_oval(20, 20, 110, 110)
        c.create_oval(20, 55, 110, 75, dash=(3, 2))


class VentanaPiramide(VentanaFigura):
    titulo = "Pirámide"
    campos = ["Base", "Altura", "Apotema"]
    clase_figura = Piramide

    def dibujar(self, c):
        c.create_polygon(65, 15, 20, 100, 90, 100, fill="", outline="black")
        c.create_polygon(65, 15, 90, 100, 115, 80, fill="", outline="black")
        c.create_line(20, 100, 115, 80, dash=(3, 2))


class VentanaCubo(VentanaFigura):
    titulo = "Cubo"
    campos = ["Arista"]
    clase_figura = Cubo

    def dibujar(self, c):
        c.create_rectangle(20, 40, 80, 100)
        c.create_rectangle(50, 15, 110, 75, dash=(3, 2))
        c.create_line(20, 40, 50, 15)
        c.create_line(80, 40, 110, 15)
        c.create_line(80, 100, 110, 75)
        c.create_line(20, 100, 50, 75, dash=(3, 2))


class VentanaPrisma(VentanaFigura):
    titulo = "Prisma"
    campos = ["Largo", "Ancho", "Altura"]
    clase_figura = Prisma

    def dibujar(self, c):
        c.create_rectangle(10, 55, 80, 105)
        c.create_rectangle(40, 30, 110, 80, dash=(3, 2))
        c.create_line(10, 55, 40, 30)
        c.create_line(80, 55, 110, 30)
        c.create_line(80, 105, 110, 80)
        c.create_line(10, 105, 40, 80, dash=(3, 2))


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self._inicio()
        self.title("Figuras")
        centrar_ventana(self, 530, 130)
        self.resizable(False, False)

    def _inicio(self):
        figuras = [("Cilindro", VentanaCilindro),
                   ("Esfera", VentanaEsfera),
                   ("Pirámide", VentanaPiramide),
                   ("Cubo", VentanaCubo),
                   ("Prisma", VentanaPrisma)]
        for i, (texto, clase_ventana) in enumerate(figuras):
            boton = tk.Button(self, text=texto,
                              command=lambda c=clase_ventana: self._abrir(c))
            boton.place(x=20 + 100 * i, y=50, width=90, height=23)

    def _abrir(self, clase_ventana):
        clase_ventana(self)


if __name__ == "__main__":
    mi_ventana_principal = VentanaPrincipal()
    mi_ventana_principal.mainloop()