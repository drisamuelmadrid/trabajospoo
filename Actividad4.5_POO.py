import os
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext


class LeerArchivo:
    """Clase que contiene la lógica para la lectura de archivos de texto."""

    @staticmethod
    def leer_contenido(ruta_archivo: str) -> list:
        """
        Lee un archivo de texto línea por línea.
        Lanza FileNotFoundError u OSError si ocurre una falla al abrir o leer.
        """
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError("No se encontró el archivo en la ruta especificada.")

        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return archivo.readlines()
        except Exception as e:
            raise OSError(f"Error de E/S al intentar leer el archivo: {e}")


class LeerArchivoApp:
    """Interfaz Gráfica de Usuario para el lector de archivos .txt."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Lectura de Archivos - Página 427")
        self.root.geometry("580x460")
        self.root.resizable(False, False)

        # Estilo visual de la GUI
        style = ttk.Style()
        style.theme_use("clam")

        # Contenedor principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        lbl_titulo = ttk.Label(
            main_frame,
            text="Lector de Archivos de Texto (.txt)",
            font=("Helvetica", 14, "bold"),
        )
        lbl_titulo.pack(pady=(0, 15))

        # Marco de ruta y selección de archivo
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            file_frame, text="Ruta del archivo:", font=("Helvetica", 10, "bold")
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.txt_ruta = ttk.Entry(file_frame, width=34)
        # Se establece por defecto la ruta indicada en la solución del libro
        self.txt_ruta.insert(0, "C:/prueba.txt")
        self.txt_ruta.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_buscar = ttk.Button(
            file_frame, text="Buscar...", command=self.examinar_archivo
        )
        self.btn_buscar.pack(side=tk.LEFT)

        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.btn_leer = ttk.Button(
            btn_frame, text="Leer Archivo", command=self.procesar_lectura
        )
        self.btn_leer.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_limpiar = ttk.Button(
            btn_frame, text="Limpiar Pantalla", command=self.limpiar_pantalla
        )
        self.btn_limpiar.pack(side=tk.LEFT)

        # Consola / Área de salida
        ttk.Label(
            main_frame,
            text="Contenido del archivo / Mensaje de Estado:",
            font=("Helvetica", 10, "bold"),
        ).pack(anchor=tk.W, pady=(5, 2))

        self.txt_salida = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=65,
            height=13,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#d4d4d4",
        )
        self.txt_salida.pack(fill=tk.BOTH, expand=True)

    def examinar_archivo(self):
        """Abre un diálogo interactivo para seleccionar archivos del sistema."""
        ruta_seleccionada = filedialog.askopenfilename(
            title="Seleccionar archivo de texto",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
        )
        if ruta_seleccionada:
            self.txt_ruta.delete(0, tk.END)
            self.txt_ruta.insert(0, ruta_seleccionada)

    def log(self, mensaje: str, es_error: bool = False):
        """Muestra texto en la pantalla de salida."""
        if es_error:
            self.txt_salida.insert(tk.END, f"[EXCEPCIÓN] {mensaje}\n")
        else:
            self.txt_salida.insert(tk.END, mensaje)
        self.txt_salida.see(tk.END)

    def limpiar_pantalla(self):
        """Limpia el visor de texto."""
        self.txt_salida.delete("1.0", tk.END)

    def procesar_lectura(self):
        """Ejecuta la lectura del archivo y gestiona la captura de excepciones."""
        self.limpiar_pantalla()
        ruta = self.txt_ruta.get().strip()

        if not ruta:
            self.log("Debe ingresar o buscar una ruta válida de archivo.", es_error=True)
            return

        try:
            lineas = LeerArchivo.leer_contenido(ruta)
            if not lineas:
                self.log("El archivo está vacío.")
            else:
                for linea in lineas:
                    self.log(linea)
        except (FileNotFoundError, OSError) as e:
            # En caso de excepción se muestra el mensaje especificado en la guía
            self.log("No se pudo leer el archivo.", es_error=True)
            self.log(f"Detalle técnico: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LeerArchivoApp(root)
    root.mainloop()