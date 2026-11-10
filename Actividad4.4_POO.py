import tkinter as tk
from tkinter import ttk, scrolledtext


class Programador:
    """Clase que modela a un integrante de un equipo de programación."""
    def __init__(self, nombre: str, apellidos: str):
        self.nombre = nombre
        self.apellidos = apellidos

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellidos}"


class EquipoMaratonProgramacion:
    """Clase que modela un equipo para una maratón de programación."""
    def __init__(self, nombre_equipo: str, universidad: str, lenguaje_programacion: str):
        self.nombre_equipo = nombre_equipo
        self.universidad = universidad
        self.lenguaje_programacion = lenguaje_programacion
        self.programadores = []
        self.max_capacidad = 3

    def esta_lleno(self) -> bool:
        """Determina si el arreglo de programadores está lleno (máximo 3)."""
        return len(self.programadores) >= self.max_capacidad

    def anadir(self, programador: Programador):
        """Añade un programador si el equipo no está completo; de lo contrario lanza excepción."""
        if self.esta_lleno():
            raise Exception("El equipo está completo. No se pudo agregar programador.")
        self.programadores.append(programador)

    @staticmethod
    def validar_campo(campo: str):
        """
        Valida que un texto no tenga dígitos y que su longitud no supere los 20 caracteres.
        Lanza excepción si viola alguna restricción.
        """
        if any(c.isdigit() for c in campo):
            raise Exception("El nombre no puede tener dígitos.")
        if len(campo) > 20:
            raise Exception("La longitud no debe ser superior a 20 caracteres.")


class EquipoMaratonApp:
    """Interfaz Gráfica de Usuario para la gestión del equipo de programación."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Equipo Maratón de Programación - Página 418")
        self.root.geometry("600x580")
        self.root.resizable(False, False)

        self.equipo = None

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        lbl_titulo = ttk.Label(
            main_frame,
            text="Registro de Equipo de Maratón",
            font=("Helvetica", 14, "bold")
        )
        lbl_titulo.pack(pady=(0, 10))

        # Sección 1: Datos del Equipo
        frame_equipo = ttk.LabelFrame(main_frame, text=" Datos del Equipo ", padding="10")
        frame_equipo.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame_equipo, text="Nombre Equipo:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.txt_equipo = ttk.Entry(frame_equipo, width=28)
        self.txt_equipo.grid(row=0, column=1, pady=3, padx=5)

        ttk.Label(frame_equipo, text="Universidad:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.txt_universidad = ttk.Entry(frame_equipo, width=28)
        self.txt_universidad.grid(row=1, column=1, pady=3, padx=5)

        ttk.Label(frame_equipo, text="Lenguaje:").grid(row=2, column=0, sticky=tk.W, pady=3)
        self.txt_lenguaje = ttk.Entry(frame_equipo, width=28)
        self.txt_lenguaje.grid(row=2, column=1, pady=3, padx=5)

        self.btn_crear_equipo = ttk.Button(
            frame_equipo,
            text="Crear Equipo",
            command=self.crear_equipo
        )
        self.btn_crear_equipo.grid(row=3, column=0, columnspan=2, pady=(8, 2))

        # Sección 2: Datos de Integrantes
        frame_integrante = ttk.LabelFrame(main_frame, text=" Agregar Integrante ", padding="10")
        frame_integrante.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame_integrante, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.txt_prog_nombre = ttk.Entry(frame_integrante, width=28)
        self.txt_prog_nombre.grid(row=0, column=1, pady=3, padx=5)

        ttk.Label(frame_integrante, text="Apellidos:").grid(row=1, column=0, sticky=tk.W, pady=3)
        self.txt_prog_apellidos = ttk.Entry(frame_integrante, width=28)
        self.txt_prog_apellidos.grid(row=1, column=1, pady=3, padx=5)

        self.btn_agregar_prog = ttk.Button(
            frame_integrante,
            text="Añadir Programador",
            command=self.agregar_programador
        )
        self.btn_agregar_prog.grid(row=2, column=0, columnspan=2, pady=(8, 2))

        # Sección 3: Consola de Salida / Excepciones
        ttk.Label(main_frame, text="Consola de Estado / Excepciones:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(5, 2))

        self.txt_salida = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=65,
            height=10,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4"
        )
        self.txt_salida.pack(fill=tk.BOTH, expand=True)

    def log(self, mensaje: str, es_error: bool = False):
        """Escribe mensajes en el área de salida."""
        if es_error:
            self.txt_salida.insert(tk.END, f"[EXCEPCIÓN] {mensaje}\n")
        else:
            self.txt_salida.insert(tk.END, f"{mensaje}\n")
        self.txt_salida.see(tk.END)

    def crear_equipo(self):
        """Instancia el equipo de maratón."""
        nom = self.txt_equipo.get().strip()
        uni = self.txt_universidad.get().strip()
        leng = self.txt_lenguaje.get().strip()

        if not nom or not uni or not leng:
            self.log("Todos los campos del equipo son obligatorios.", es_error=True)
            return

        self.equipo = EquipoMaratonProgramacion(nom, uni, leng)
        self.txt_salida.delete("1.0", tk.END)
        self.log(f"Nombre del equipo = {self.equipo.nombre_equipo}")
        self.log(f"Universidad = {self.equipo.universidad}")
        self.log(f"Lenguaje de programación = {self.equipo.lenguaje_programacion}")
        self.log("Datos de los integrantes del equipo:")

    def agregar_programador(self):
        """Valida y añade un nuevo integrante al equipo gestionando excepciones."""
        if not self.equipo:
            self.log("Primero debe crear un equipo.", es_error=True)
            return

        nombre_p = self.txt_prog_nombre.get().strip()
        apellidos_p = self.txt_prog_apellidos.get().strip()

        if not nombre_p or not apellidos_p:
            self.log("Los campos Nombre y Apellidos son obligatorios.", es_error=True)
            return

        try:
            # Validar nombre del integrante
            EquipoMaratonProgramacion.validar_campo(nombre_p)
            # Validar apellidos del integrante
            EquipoMaratonProgramacion.validar_campo(apellidos_p)

            # Crear e intentar añadir al equipo
            prog = Programador(nombre_p, apellidos_p)
            self.equipo.anadir(prog)

            self.log(f"Nombre del integrante = {prog.nombre}")
            self.log(f"Apellidos del integrante = {prog.apellidos}")

            # Limpiar entradas de integrante
            self.txt_prog_nombre.delete(0, tk.END)
            self.txt_prog_apellidos.delete(0, tk.END)

        except Exception as e:
            self.log(str(e), es_error=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = EquipoMaratonApp(root)
    root.mainloop()