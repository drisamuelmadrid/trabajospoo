from enum import Enum
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


# ==============================================================================
# ENUMERACIONES
# ==============================================================================

class TipoCargo(Enum):
    """Dato enumerado que especifica el tipo de cargo que tiene un empleado."""
    DIRECTIVO = "DIRECTIVO"
    ESTRATEGICO = "ESTRATÉGICO"
    OPERATIVO = "OPERATIVO"


class TipoGenero(Enum):
    """Dato enumerado que especifica el tipo de género que tiene un empleado."""
    MASCULINO = "MASCULINO"
    FEMENINO = "FEMENINO"


# ==============================================================================
# MODELO Y LÓGICA DE NÓMINA
# ==============================================================================

class Empleado:
    """Modela un empleado de una empresa y calcula su salario mensual."""

    def __init__(
        self,
        nombre: str,
        apellidos: str,
        cargo: TipoCargo,
        genero: TipoGenero,
        salario_dia: float,
        dias_trabajados: int,
        otros_ingresos: float,
        pagos_salud: float,
        aporte_pensiones: float,
    ) -> None:
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__cargo = cargo
        self.__genero = genero
        self.__salario_dia = salario_dia
        self.__dias_trabajados = dias_trabajados
        self.__otros_ingresos = otros_ingresos
        self.__pagos_salud = pagos_salud
        self.__aporte_pensiones = aporte_pensiones

    def get_nombre(self) -> str:
        return self.__nombre

    def get_apellidos(self) -> str:
        return self.__apellidos

    def get_cargo(self) -> TipoCargo:
        return self.__cargo

    def get_genero(self) -> TipoGenero:
        return self.__genero

    def get_salario_dia(self) -> float:
        return self.__salario_dia

    def get_dias_trabajados(self) -> int:
        return self.__dias_trabajados

    def get_otros_ingresos(self) -> float:
        return self.__otros_ingresos

    def get_pagos_salud(self) -> float:
        return self.__pagos_salud

    def get_aporte_pensiones(self) -> float:
        return self.__aporte_pensiones

    def calcular_nomina(self) -> float:
        """Calcula el salario mensual del empleado."""
        return (
            (self.__salario_dia * self.__dias_trabajados)
            + self.__otros_ingresos
            - self.__pagos_salud
            - self.__aporte_pensiones
        )


class ListaEmpleados:
    """Define una lista de objetos Empleado y el total de la nómina."""

    def __init__(self) -> None:
        self.lista: list[Empleado] = []
        self.total_nomina: float = 0.0

    def agregar_empleado(self, empleado: Empleado) -> None:
        """Agrega un empleado a la lista de empleados."""
        self.lista.append(empleado)

    def calcular_total_nomina(self) -> float:
        """Calcula la nómina total mensual de la empresa."""
        self.total_nomina = 0.0
        for e in self.lista:
            self.total_nomina += e.calcular_nomina()
        return self.total_nomina

    def obtener_matriz(self) -> list[list[str]]:
        """Convierte los datos de la lista de empleados en una matriz para la tabla."""
        datos: list[list[str]] = []
        self.total_nomina = 0.0
        for e in self.lista:
            sueldo = e.calcular_nomina()
            datos.append([e.get_nombre(), e.get_apellidos(), f"{sueldo:.2f}"])
            self.total_nomina += sueldo
        return datos

    def convertir_texto(self) -> str:
        """Convierte los datos de la lista de empleados a formato de texto."""
        texto = ""
        for e in self.lista:
            texto += (
                f"Nombre = {e.get_nombre()}\n"
                f"Apellidos = {e.get_apellidos()}\n"
                f"Cargo = {e.get_cargo().value}\n"
                f"Género = {e.get_genero().value}\n"
                f"Salario = ${e.get_salario_dia()}\n"
                f"Días trabajados = {e.get_dias_trabajados()}\n"
                f"Otros ingresos = ${e.get_otros_ingresos()}\n"
                f"Pagos salud = ${e.get_pagos_salud()}\n"
                f"Aportes pensiones = ${e.get_aporte_pensiones()}\n"
                f"---------\n"
            )
        texto += f"Total nómina = ${self.calcular_total_nomina():.2f}"
        return texto


# ==============================================================================
# INTERFAZ GRÁFICA DE USUARIO (GUI)
# ==============================================================================

class VentanaAgregarEmpleado(tk.Toplevel):
    """Ventana para ingresar los datos de un empleado y agregarlo a la lista."""

    def __init__(self, master: tk.Tk, lista: ListaEmpleados) -> None:
        super().__init__(master)
        self.lista = lista
        self.title("Agregar Empleado")
        self.resizable(False, False)
        self._centrar_ventana(310, 410)
        self.inicio()

    def _centrar_ventana(self, ancho: int, alto: int) -> None:
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self) -> None:
        """Crea la ventana con sus diferentes componentes gráficos."""
        # Nombre
        tk.Label(self, text="Nombre:").place(x=20, y=20, width=135, height=23)
        self.campo_nombre = tk.Entry(self)
        self.campo_nombre.place(x=165, y=20, width=115, height=23)

        # Apellidos
        tk.Label(self, text="Apellidos:").place(x=20, y=50, width=135, height=23)
        self.campo_apellidos = tk.Entry(self)
        self.campo_apellidos.place(x=165, y=50, width=115, height=23)

        # Cargo (ComboBox)
        tk.Label(self, text="Cargo:").place(x=20, y=80, width=135, height=23)
        self.campo_cargo = ttk.Combobox(
            self,
            values=["Directivo", "Estratégico", "Operativo"],
            state="readonly",
        )
        self.campo_cargo.current(0)
        self.campo_cargo.place(x=165, y=80, width=115, height=23)

        # Género (RadioButtons)
        tk.Label(self, text="Género:").place(x=20, y=110, width=100, height=30)
        self.var_genero = tk.StringVar(value="Masculino")
        self.masculino = tk.Radiobutton(
            self, text="Masculino", variable=self.var_genero, value="Masculino"
        )
        self.masculino.place(x=165, y=110, width=100, height=25)

        self.femenino = tk.Radiobutton(
            self, text="Femenino", variable=self.var_genero, value="Femenino"
        )
        self.femenino.place(x=165, y=138, width=100, height=25)

        # Salario por día
        tk.Label(self, text="Salario por día:").place(x=20, y=170, width=135, height=23)
        self.campo_salario_dia = tk.Entry(self)
        self.campo_salario_dia.place(x=165, y=170, width=115, height=23)

        # Días trabajados al mes (Spinner 1 a 31)
        tk.Label(self, text="Días trabajados al mes:").place(
            x=20, y=200, width=140, height=23
        )
        self.var_dias = tk.IntVar(value=30)
        self.campo_numero_dias = tk.Spinbox(
            self, from_=1, to=31, textvariable=self.var_dias
        )
        self.campo_numero_dias.place(x=165, y=200, width=50, height=23)

        # Otros ingresos
        tk.Label(self, text="Otros ingresos:").place(x=20, y=230, width=135, height=23)
        self.campo_otros_ingresos = tk.Entry(self)
        self.campo_otros_ingresos.place(x=165, y=230, width=115, height=23)

        # Pagos por salud
        tk.Label(self, text="Pagos por salud:").place(x=20, y=260, width=135, height=23)
        self.campo_aportes_salud = tk.Entry(self)
        self.campo_aportes_salud.place(x=165, y=260, width=115, height=23)

        # Aportes pensiones
        tk.Label(self, text="Aportes pensiones:").place(
            x=20, y=290, width=135, height=23
        )
        self.campo_pensiones = tk.Entry(self)
        self.campo_pensiones.place(x=165, y=290, width=115, height=23)

        # Botones Agregar y Borrar
        self.agregar = tk.Button(self, text="Agregar", command=self.anadir_empleado)
        self.agregar.place(x=30, y=335, width=105, height=28)

        self.limpiar = tk.Button(self, text="Borrar", command=self.limpiar_campos)
        self.limpiar.place(x=165, y=335, width=95, height=28)

    def limpiar_campos(self) -> None:
        """Borra los campos de texto ingresados en la ventana."""
        self.campo_nombre.delete(0, tk.END)
        self.campo_apellidos.delete(0, tk.END)
        self.campo_salario_dia.delete(0, tk.END)
        self.var_dias.set(30)
        self.campo_otros_ingresos.delete(0, tk.END)
        self.campo_aportes_salud.delete(0, tk.END)
        self.campo_pensiones.delete(0, tk.END)

    def anadir_empleado(self) -> None:
        """Valida los datos y agrega un empleado a la lista."""
        item_seleccionado = self.campo_cargo.get()
        if item_seleccionado == "Directivo":
            tipo_c = TipoCargo.DIRECTIVO
        elif item_seleccionado == "Estratégico":
            tipo_c = TipoCargo.ESTRATEGICO
        else:
            tipo_c = TipoCargo.OPERATIVO

        if self.var_genero.get() == "Masculino":
            tipo_g = TipoGenero.MASCULINO
        else:
            tipo_g = TipoGenero.FEMENINO

        try:
            valor1 = self.campo_nombre.get().strip()
            valor2 = self.campo_apellidos.get().strip()
            if not valor1 or not valor2:
                raise ValueError("Campo vacío")

            valor3 = float(self.campo_salario_dia.get())
            valor4 = int(self.campo_numero_dias.get())
            if not (1 <= valor4 <= 31):
                raise ValueError("Días fuera de rango")

            valor5 = float(self.campo_otros_ingresos.get())
            valor6 = float(self.campo_aportes_salud.get())
            valor7 = float(self.campo_pensiones.get())

            empleado = Empleado(
                valor1, valor2, tipo_c, tipo_g, valor3, valor4, valor5, valor6, valor7
            )
            self.lista.agregar_empleado(empleado)

            messagebox.showinfo(
                "Mensaje", "El empleado ha sido agregado", parent=self
            )
            self.limpiar_campos()
        except ValueError:
            messagebox.showerror(
                "Error", "Campo nulo o error en formato de número", parent=self
            )


class VentanaNomina(tk.Toplevel):
    """Ventana que muestra en formato tabla la lista de empleados y la nómina total."""

    def __init__(self, master: tk.Tk, lista: ListaEmpleados) -> None:
        super().__init__(master)
        self.lista = lista
        self.title("Nómina de Empleados")
        self.resizable(False, False)
        self._centrar_ventana(380, 260)
        self.inicio()

    def _centrar_ventana(self, ancho: int, alto: int) -> None:
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self) -> None:
        """Crea la ventana con la tabla de empleados y el total de nómina."""
        tk.Label(self, text="Lista de empleados:").place(x=20, y=10, width=150, height=23)

        datos = self.lista.obtener_matriz()
        columnas = ("NOMBRE", "APELLIDOS", "SUELDO")

        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=5)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=110, anchor="center")

        for fila in datos:
            self.tabla.insert("", tk.END, values=fila)

        self.tabla.place(x=20, y=45, width=340, height=130)

        self.nomina = tk.Label(
            self,
            text=f"Total nómina mensual = $ {self.lista.total_nomina:.2f}",
        )
        self.nomina.place(x=20, y=195, width=300, height=23)


class VentanaPrincipal(tk.Tk):
    """Ventana principal de la aplicación de nómina con barra de menús."""

    def __init__(self) -> None:
        super().__init__()
        self.empleados = ListaEmpleados()
        self.title("Nómina")
        self.resizable(False, False)
        self._centrar_ventana(280, 380)
        self.inicio()

    def _centrar_ventana(self, ancho: int, alto: int) -> None:
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self) -> None:
        """Crea la barra de menús y sus opciones."""
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)

        menu_opciones.add_command(
            label="Agregar empleado", command=self.abrir_agregar_empleado
        )
        menu_opciones.add_command(
            label="Calcular nómina", command=self.abrir_calcular_nomina
        )
        menu_opciones.add_separator()
        menu_opciones.add_command(
            label="Guardar archivo", command=self.guardar_archivo
        )

        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

    def abrir_agregar_empleado(self) -> None:
        VentanaAgregarEmpleado(self, self.empleados)

    def abrir_calcular_nomina(self) -> None:
        VentanaNomina(self, self.empleados)

    def guardar_archivo(self) -> None:
        """Solicita una carpeta y genera el archivo Nómina.txt."""
        directorio_elegido = filedialog.askdirectory(
            parent=self, title="Seleccionar carpeta"
        )
        if directorio_elegido:
            try:
                contenido = self.empleados.convertir_texto()
                ruta_archivo = os.path.join(directorio_elegido, "Nómina.txt")
                with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                    archivo.write(contenido)

                nombre_carpeta = (
                    os.path.basename(directorio_elegido) or directorio_elegido
                )
                texto = (
                    f"El archivo de la nómina Nómina.txt se ha creado en {nombre_carpeta}"
                )
                messagebox.showinfo("Mensaje", texto, parent=self)
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo guardar el archivo: {e}", parent=self
                )


# ==============================================================================
# PUNTO DE ENTRADA
# ==============================================================================

class Principal:
    """Punto de ingreso al programa de la nómina de empleados."""

    @staticmethod
    def main() -> None:
        mi_ventana_principal = VentanaPrincipal()
        mi_ventana_principal.mainloop()


if __name__ == "__main__":
    Principal.main()