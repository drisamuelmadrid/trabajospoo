import tkinter as tk
from tkinter import ttk, scrolledtext

class PruebaExcepcionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prueba de Excepciones - Página 400")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        # Configuración de estilos
        style = ttk.Style()
        style.theme_use('clam')

        # Marco principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        lbl_titulo = ttk.Label(
            main_frame, 
            text="Simulador de Control de Excepciones", 
            font=("Helvetica", 14, "bold")
        )
        lbl_titulo.pack(pady=(0, 10))

        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.btn_ejecutar = ttk.Button(
            btn_frame, 
            text="Ejecutar Simulación", 
            command=self.ejecutar_simulacion
        )
        self.btn_ejecutar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_limpiar = ttk.Button(
            btn_frame, 
            text="Limpiar Pantalla", 
            command=self.limpiar_salida
        )
        self.btn_limpiar.pack(side=tk.LEFT)

        # Área de texto para la salida de la consola gráfica
        lbl_salida = ttk.Label(main_frame, text="Salida de ejecución:", font=("Helvetica", 10, "bold"))
        lbl_salida.pack(anchor=tk.W, pady=(5, 2))

        self.txt_salida = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            width=58, 
            height=14, 
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4"
        )
        self.txt_salida.pack(fill=tk.BOTH, expand=True)

    def log(self, mensaje):
        """Agrega texto al componente de salida gráfica."""
        self.txt_salida.insert(tk.END, mensaje + "\n")
        self.txt_salida.see(tk.END)

    def limpiar_salida(self):
        """Limpia el contenido del área de texto."""
        self.txt_salida.delete("1.0", tk.END)

    def ejecutar_simulacion(self):
        """Equivalente al método main de la página 400 en Java."""
        self.limpiar_salida()
        self.log("=== INICIANDO PRUEBA DE EXCEPCIONES ===\n")

        # --- Primer bloque try ---
        try:
            self.log("Ingresando al primer try")
            cociente = 10000 / 0  # Lanza ZeroDivisionError
            self.log("Después de la división")  # Esta línea no se ejecuta
        except ZeroDivisionError:
            self.log("División por cero")
        finally:
            self.log("Ingresando al primer finally")

        self.log("")  # Salto de línea decorativo

        # --- Segundo bloque try ---
        try:
            self.log("Ingresando al segundo try")
            objeto = None
            objeto.upper()  # Lanza AttributeError (equiv. a NullPointerException/Exception en Java)
            self.log("Imprimiendo objeto")  # Esta línea no se ejecuta
        except ZeroDivisionError:
            self.log("División por cero")
        except Exception:
            self.log("Ocurrió una excepción")
        finally:
            self.log("Ingresando al segundo finally")

        self.log("\n=== FIN DE LA EJECUCIÓN ===")


if __name__ == "__main__":
    root = tk.Tk()
    app = PruebaExcepcionesApp(root)
    root.mainloop()