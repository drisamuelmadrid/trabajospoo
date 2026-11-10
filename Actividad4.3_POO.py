import math
import tkinter as tk
from tkinter import ttk, scrolledtext

class CalculosNumericos:
    """Clase con métodos estáticos para realizar cálculos matemáticos con validación de excepciones."""

    @staticmethod
    def calcular_logaritmo_neperiano(valor: float) -> float:
        """
        Calcula el logaritmo neperiano de un número.
        Lanza ValueError (equivalente a ArithmeticException) si el valor no es positivo.
        """
        if valor <= 0:
            raise ValueError("El valor debe ser un número positivo para calcular el logaritmo.")
        return math.log(valor)

    @staticmethod
    def calcular_raiz_cuadrada(valor: float) -> float:
        """
        Calcula la raíz cuadrada de un número.
        Lanza ValueError (equivalente a ArithmeticException) si el valor no es positivo.
        """
        if valor <= 0:
            raise ValueError("El valor debe ser un número positivo para calcular la raíz cuadrada.")
        return math.sqrt(valor)


class CalculosNumericosApp:
    """Interfaz Gráfica de Usuario para la realización de cálculos numéricos."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cálculos Numéricos - Página 412")
        self.root.geometry("540x480")
        self.root.resizable(False, False)

        # Estilo visual
        style = ttk.Style()
        style.theme_use('clam')

        # Contenedor principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        lbl_titulo = ttk.Label(
            main_frame,
            text="Cálculos Numéricos y Manejo de Excepciones",
            font=("Helvetica", 13, "bold")
        )
        lbl_titulo.pack(pady=(0, 15))

        # Entrada de datos
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="Valor numérico:", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.txt_valor = ttk.Entry(input_frame, width=25)
        self.txt_valor.pack(side=tk.LEFT)

        # Botones de operaciones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.btn_logaritmo = ttk.Button(
            btn_frame,
            text="Calcular Logaritmo",
            command=self.procesar_logaritmo
        )
        self.btn_logaritmo.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_raiz = ttk.Button(
            btn_frame,
            text="Calcular Raíz Cuadrada",
            command=self.procesar_raiz
        )
        self.btn_raiz.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_ambos = ttk.Button(
            btn_frame,
            text="Calcular Ambos",
            command=self.procesar_ambos
        )
        self.btn_ambos.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_limpiar = ttk.Button(
            btn_frame,
            text="Limpiar",
            command=self.limpiar_campos
        )
        self.btn_limpiar.pack(side=tk.LEFT)

        # Consola de salida de resultados / errores
        ttk.Label(main_frame, text="Salida de consola / Excepciones:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(10, 2))

        self.txt_salida = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=60,
            height=12,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4"
        )
        self.txt_salida.pack(fill=tk.BOTH, expand=True)

    def log(self, mensaje: str):
        """Escribe una línea en el panel de texto."""
        self.txt_salida.insert(tk.END, mensaje + "\n")
        self.txt_salida.see(tk.END)

    def limpiar_campos(self):
        """Limpia el campo de entrada y la pantalla de log."""
        self.txt_valor.delete(0, tk.END)
        self.txt_salida.delete("1.0", tk.END)

    def obtener_valor(self) -> float:
        """
        Lee el texto del input y convierte a float.
        Lanza TypeError si no es un número válido (equivalente a InputMismatchException).
        """
        raw = self.txt_valor.get().strip()
        if not raw:
            raise TypeError("Debe ingresar un valor numérico.")
        try:
            return float(raw)
        except ValueError:
            raise TypeError("El valor debe ser numérico para realizar el cálculo.")

    def procesar_logaritmo(self):
        """Procesa únicamente el logaritmo neperiano gestionando excepciones."""
        self.txt_salida.delete("1.0", tk.END)
        try:
            val = self.obtener_valor()
            res = CalculosNumericos.calcular_logaritmo_neperiano(val)
            self.log(f"Logaritmo neperiano ({val}) = {res}")
        except TypeError as e:
            self.log(f"[EXCEPCIÓN - InputMismatch] {e}")
        except ValueError as e:
            self.log(f"[EXCEPCIÓN - ArithMeticError] {e}")

    def procesar_raiz(self):
        """Procesa únicamente la raíz cuadrada gestionando excepciones."""
        self.txt_salida.delete("1.0", tk.END)
        try:
            val = self.obtener_valor()
            res = CalculosNumericos.calcular_raiz_cuadrada(val)
            self.log(f"Raíz cuadrada ({val}) = {res}")
        except TypeError as e:
            self.log(f"[EXCEPCIÓN - InputMismatch] {e}")
        except ValueError as e:
            self.log(f"[EXCEPCIÓN - ArithMeticError] {e}")

    def procesar_ambos(self):
        """Ejecuta la secuencia exacta descrita en el método main del texto guía."""
        self.txt_salida.delete("1.0", tk.END)
        raw_val = self.txt_valor.get().strip()
        self.log(f"Valor numérico = {raw_val if raw_val else '[Vacío]'}\n")

        # 1. Intento de Logaritmo Neperiano
        try:
            val = self.obtener_valor()
            res_log = CalculosNumericos.calcular_logaritmo_neperiano(val)
            self.log(f"Resultado Logaritmo = {res_log}")
        except TypeError:
            self.log("El valor debe ser numérico para calcular el logaritmo")
        except ValueError:
            self.log("El valor debe ser un número positivo para calcular el logaritmo")

        # 2. Intento de Raíz Cuadrada
        try:
            val = self.obtener_valor()
            res_raiz = CalculosNumericos.calcular_raiz_cuadrada(val)
            self.log(f"Resultado Raíz Cuadrada = {res_raiz}")
        except TypeError:
            self.log("El valor debe ser numérico para calcular la raíz cuadrada")
        except ValueError:
            self.log("El valor debe ser un número positivo para calcular la raíz cuadrada")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculosNumericosApp(root)
    root.mainloop()