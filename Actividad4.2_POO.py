import tkinter as tk
from tkinter import ttk, scrolledtext

class Vendedor:
    """Clase que modela a un vendedor y valida las restricciones de edad."""
    def __init__(self, nombre: str, apellidos: str):
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = None

    def verificar_edad(self, edad: int):
        """
        Verifica si la edad cumple los requisitos del sistema:
        - Si es menor de 18 años, lanza ValueError.
        - Si está en el rango de 0 a 120 (y >= 18), se asigna la edad.
        - En cualquier otro caso, lanza ValueError.
        """
        if edad < 18:
            raise ValueError("El vendedor debe ser mayor de 18 años.")
        if 0 <= edad < 120:
            self.edad = edad
        else:
            raise ValueError("La edad no puede ser negativa ni mayor a 120.")

    def imprimir(self) -> str:
        """Devuelve la información formateada del vendedor."""
        return (
            f"Nombre del vendedor = {self.nombre}\n"
            f"Apellidos del vendedor = {self.apellidos}\n"
            f"Edad del vendedor = {self.edad}"
        )


class VendedorApp:
    """Interfaz Gráfica de Usuario para el registro de vendedores."""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Registro de Vendedores - Página 406")
        self.root.geometry("520x480")
        self.root.resizable(False, False)

        # Estilo de la interfaz
        style = ttk.Style()
        style.theme_use('clam')

        # Contenedor principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Encabezado
        lbl_titulo = ttk.Label(
            main_frame,
            text="Verificación y Registro de Vendedor",
            font=("Helvetica", 14, "bold")
        )
        lbl_titulo.pack(pady=(0, 15))

        # Formulario de entrada
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(form_frame, text="Nombre:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.txt_nombre = ttk.Entry(form_frame, width=35)
        self.txt_nombre.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Apellidos:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.txt_apellidos = ttk.Entry(form_frame, width=35)
        self.txt_apellidos.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(form_frame, text="Edad:", font=("Helvetica", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.txt_edad = ttk.Entry(form_frame, width=35)
        self.txt_edad.grid(row=2, column=1, pady=5, padx=5)

        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.btn_guardar = ttk.Button(
            btn_frame,
            text="Validar e Instanciar",
            command=self.procesar_vendedor
        )
        self.btn_guardar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_limpiar = ttk.Button(
            btn_frame,
            text="Limpiar Campos",
            command=self.limpiar_campos
        )
        self.btn_limpiar.pack(side=tk.LEFT)

        # Consola de salida de resultados / excepciones
        ttk.Label(main_frame, text="Resultado / Excepción generada:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(5, 2))

        self.txt_salida = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=58,
            height=10,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4"
        )
        self.txt_salida.pack(fill=tk.BOTH, expand=True)

    def log(self, mensaje: str, es_error: bool = False):
        """Muestra mensajes en la consola gráfica."""
        if es_error:
            self.txt_salida.insert(tk.END, f"[EXCEPCIÓN CAPTURADA]\n{mensaje}\n\n")
        else:
            self.txt_salida.insert(tk.END, f"{mensaje}\n\n")
        self.txt_salida.see(tk.END)

    def limpiar_campos(self):
        """Restablece los campos de entrada y la pantalla de salida."""
        self.txt_nombre.delete(0, tk.END)
        self.txt_apellidos.delete(0, tk.END)
        self.txt_edad.delete(0, tk.END)
        self.txt_salida.delete("1.0", tk.END)

    def procesar_vendedor(self):
        """Captura datos, valida la edad y maneja excepciones lanzadas."""
        self.txt_salida.delete("1.0", tk.END)
        nombre = self.txt_nombre.get().strip()
        apellidos = self.txt_apellidos.get().strip()
        raw_edad = self.txt_edad.get().strip()

        if not nombre or not apellidos or not raw_edad:
            self.log("Error: Todos los campos (Nombre, Apellidos, Edad) son obligatorios.", es_error=True)
            return

        try:
            edad = int(raw_edad)
            # Instanciación y verificación de restricciones
            vendedor = Vendedor(nombre, apellidos)
            vendedor.verificar_edad(edad)
            
            # Si la edad es válida, se muestran los datos del vendedor
            self.log("=== DATOS DEL VENDEDOR ===")
            self.log(vendedor.imprimir())

        except ValueError as e:
            if "invalid literal for int()" in str(e):
                self.log("ValueError: La edad debe ser un número entero válido.", es_error=True)
            else:
                self.log(f"ValueError: {e}", es_error=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = VendedorApp(root)
    root.mainloop()