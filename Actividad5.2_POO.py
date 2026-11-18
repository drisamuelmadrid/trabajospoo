from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog


# ==============================================================================
# MODELO DEL HOTEL
# ==============================================================================

class Huesped:
    """Define un huésped del hotel que ocupará una habitación por ciertos días."""

    def __init__(self, nombres: str, apellidos: str, documento_identidad: int) -> None:
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__documento_identidad = documento_identidad
        self.__fecha_ingreso: datetime | None = None
        self.__fecha_salida: datetime | None = None

    def get_nombres(self) -> str:
        return self.__nombres

    def get_apellidos(self) -> str:
        return self.__apellidos

    def get_documento_identidad(self) -> int:
        return self.__documento_identidad

    def set_fecha_ingreso(self, fecha: datetime) -> None:
        self.__fecha_ingreso = fecha

    def get_fecha_ingreso(self) -> datetime | None:
        return self.__fecha_ingreso

    def set_fecha_salida(self, fecha: datetime) -> None:
        self.__fecha_salida = fecha

    def get_fecha_salida(self) -> datetime | None:
        return self.__fecha_salida

    def obtener_dias_alojamiento(self) -> int:
        """Calcula la cantidad de días de alojamiento del huésped."""
        if self.__fecha_ingreso is not None and self.__fecha_salida is not None:
            return (self.__fecha_salida - self.__fecha_ingreso).days
        return 0


class Habitacion:
    """Define una habitación de un hotel a ser ocupada y desocupada por un huésped."""

    def __init__(
        self, numero_habitacion: int, disponible: bool, precio_dia: float
    ) -> None:
        self.__numero_habitacion = numero_habitacion
        self.__disponible = disponible
        self.__precio_dia = precio_dia
        self.__huesped: Huesped | None = None

    def get_numero_habitacion(self) -> int:
        return self.__numero_habitacion

    def get_disponible(self) -> bool:
        return self.__disponible

    def set_disponible(self, disponible: bool) -> None:
        self.__disponible = disponible

    def get_precio_dia(self) -> float:
        return self.__precio_dia

    def get_huesped(self) -> Huesped | None:
        return self.__huesped

    def set_huesped(self, huesped: Huesped | None) -> None:
        self.__huesped = huesped


class Hotel:
    """Define un hotel que contiene diez habitaciones simples."""

    def __init__(self) -> None:
        self.lista_habitaciones: list[Habitacion] = [
            Habitacion(1, True, 120000.0),
            Habitacion(2, True, 120000.0),
            Habitacion(3, True, 120000.0),
            Habitacion(4, True, 120000.0),
            Habitacion(5, True, 120000.0),
            Habitacion(6, True, 160000.0),
            Habitacion(7, True, 160000.0),
            Habitacion(8, True, 160000.0),
            Habitacion(9, True, 160000.0),
            Habitacion(10, True, 160000.0),
        ]

    def buscar_fecha_ingreso_habitacion(self, numero: int) -> str:
        """Dado un número de habitación, devuelve la fecha de ingreso formateada."""
        for habitacion in self.lista_habitaciones:
            if habitacion.get_numero_habitacion() == numero:
                huesped = habitacion.get_huesped()
                if huesped is not None and huesped.get_fecha_ingreso() is not None:
                    return huesped.get_fecha_ingreso().strftime("%Y/%m/%d")
        return ""

    def buscar_habitacion_ocupada(self, numero: int) -> bool:
        """Determina si una habitación está ocupada a partir de su número."""
        for habitacion in self.lista_habitaciones:
            if (
                habitacion.get_numero_habitacion() == numero
                and not habitacion.get_disponible()
            ):
                return True
        return False


# ==============================================================================
# INTERFAZ GRÁFICA DE USUARIO (GUI)
# ==============================================================================

class VentanaIngreso(tk.Toplevel):
    """Ventana para ingresar los datos del huésped que ocupará una habitación."""

    def __init__(
        self, master: tk.Misc, hotel: Hotel, numero_habitacion_reservada: int
    ) -> None:
        super().__init__(master)
        self.hotel = hotel
        self.numero_habitacion_reservada = numero_habitacion_reservada
        self.title("Ingreso")
        self.resizable(False, False)
        self._centrar_ventana(300, 240)
        self.inicio()

    def _centrar_ventana(self, ancho: int, alto: int) -> None:
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self) -> None:
        """Organiza los componentes mediante gestor de malla (equivalente a GridBagLayout)."""
        contenedor = tk.Frame(self, padx=10, pady=10)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=1)

        # Fila 0: Habitación
        tk.Label(
            contenedor,
            text=f"Habitación: {self.numero_habitacion_reservada}",
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=3, pady=3)

        # Fila 1: Fecha de ingreso
        tk.Label(contenedor, text="Fecha (aaaa-mm-dd):", anchor="w").grid(
            row=1, column=0, sticky="ew", padx=3, pady=3
        )
        self.campo_fecha_ingreso = tk.Entry(contenedor)
        self.campo_fecha_ingreso.grid(row=1, column=1, sticky="ew", padx=3, pady=3)

        # Fila 2: Subtítulo Huésped
        tk.Label(contenedor, text="Huésped", anchor="w").grid(
            row=2, column=0, sticky="ew", padx=3, pady=3
        )

        # Fila 3: Nombre
        tk.Label(contenedor, text="Nombre:", anchor="w").grid(
            row=3, column=0, sticky="ew", padx=3, pady=3
        )
        self.campo_nombre = tk.Entry(contenedor)
        self.campo_nombre.grid(row=3, column=1, sticky="ew", padx=3, pady=3)

        # Fila 4: Apellidos
        tk.Label(contenedor, text="Apellidos:", anchor="w").grid(
            row=4, column=0, sticky="ew", padx=3, pady=3
        )
        self.campo_apellidos = tk.Entry(contenedor)
        self.campo_apellidos.grid(row=4, column=1, sticky="ew", padx=3, pady=3)

        # Fila 5: Documento de identidad
        tk.Label(contenedor, text="Doc. Identidad:", anchor="w").grid(
            row=5, column=0, sticky="ew", padx=3, pady=3
        )
        self.campo_documento_identidad = tk.Entry(contenedor)
        self.campo_documento_identidad.grid(
            row=5, column=1, sticky="ew", padx=3, pady=3
        )

        # Fila 6: Botones Aceptar y Cancelar
        self.aceptar = tk.Button(
            contenedor, text="Aceptar", command=self.registrar_ingreso
        )
        self.aceptar.grid(row=6, column=0, sticky="ew", padx=3, pady=6)

        self.cancelar = tk.Button(contenedor, text="Cancelar", command=self.destroy)
        self.cancelar.grid(row=6, column=1, sticky="ew", padx=3, pady=6)

    def registrar_ingreso(self) -> None:
        """Valida los campos y registra el ingreso del huésped en la habitación."""
        for habitacion in self.hotel.lista_habitaciones:
            if (
                habitacion.get_numero_habitacion()
                == self.numero_habitacion_reservada
            ):
                fecha_ingresada = self.campo_fecha_ingreso.get().strip()
                try:
                    fecha = datetime.strptime(fecha_ingresada, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror(
                        "Mensaje",
                        "La fecha no está en el formato solicitado",
                        parent=self,
                    )
                    return

                try:
                    nombres = self.campo_nombre.get().strip()
                    apellidos = self.campo_apellidos.get().strip()
                    doc_texto = self.campo_documento_identidad.get().strip()

                    if not nombres or not apellidos or not doc_texto:
                        raise ValueError("Campos vacíos")

                    documento = int(doc_texto)

                    huesped = Huesped(nombres, apellidos, documento)
                    huesped.set_fecha_ingreso(fecha)
                    habitacion.set_huesped(huesped)
                    habitacion.set_disponible(False)

                    messagebox.showinfo(
                        "Mensaje", "El huésped ha sido registrado", parent=self
                    )
                    self.destroy()
                    return
                except ValueError:
                    messagebox.showerror(
                        "Error",
                        "Campo nulo o error en formato de número",
                        parent=self,
                    )
                    return


class VentanaHabitaciones(tk.Toplevel):
    """Ventana que muestra las diez habitaciones del hotel y su disponibilidad."""

    def __init__(self, master: tk.Tk, hotel: Hotel) -> None:
        super().__init__(master)
        self.hotel = hotel
        self.title("Habitaciones")
        self.resizable(False, False)
        self._centrar_ventana(740, 240)
        self.inicio()

    def _centrar_ventana(self, ancho: int, alto: int) -> None:
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self) -> None:
        """Crea las etiquetas de estado de las 10 habitaciones y el selector."""
        for idx, habitacion in enumerate(self.hotel.lista_habitaciones):
            col = idx % 5
            fila = idx // 5
            pos_x = 20 + col * 140
            pos_y = 30 if fila == 0 else 110

            tk.Label(
                self,
                text=f"Habitación {habitacion.get_numero_habitacion()}",
                anchor="w",
            ).place(x=pos_x, y=pos_y, width=120, height=23)

            estado = (
                "Disponible" if habitacion.get_disponible() else "No disponible"
            )
            tk.Label(self, text=estado, anchor="w").place(
                x=pos_x, y=pos_y + 20, width=120, height=23
            )

        tk.Label(self, text="Habitación a reservar:", anchor="w").place(
            x=230, y=180, width=140, height=23
        )

        self.var_habitacion = tk.IntVar(value=1)
        self.campo_habitacion_seleccionada = tk.Spinbox(
            self, from_=1, to=10, textvariable=self.var_habitacion
        )
        self.campo_habitacion_seleccionada.place(x=375, y=180, width=45, height=23)

        self.boton_aceptar = tk.Button(
            self, text="Aceptar", command=self.seleccionar_habitacion
        )
        self.boton_aceptar.place(x=460, y=178, width=100, height=26)

    def seleccionar_habitacion(self) -> None:
        """Verifica disponibilidad y abre la ventana de ingreso si está libre."""
        try:
            numero = int(self.campo_habitacion_seleccionada.get())
            if numero < 1 or numero > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Número de habitación inválido", parent=self
            )
            return

        if not self.hotel.buscar_habitacion_ocupada(numero):
            ventana_ingreso = VentanaIngreso(self.master, self.hotel, numero)
            self.destroy()
            ventana_ingreso.focus_set()
        else:
            messagebox.showinfo(
                "Mensaje", "La habitación está ocupada", parent=self
            )


class VentanaSalida(tk.Toplevel):
    """Ventana para registrar la salida de un huésped y calcular su pago."""

    def __init__(self, master: tk.Tk, hotel: Hotel, numero: int) -> None:
        super().__init__(master)
        self.hotel = hotel
        self.numero_habitacion = numero
        self.habitacion_ocupada: Habitacion | None = None
        self.title("Salida huéspedes")
        self.resizable(False, False)
        self._centrar_ventana(270, 275)
        self.inicio()

    def _centrar_ventana(self, ancho: int, alto: int) -> None:
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self) -> None:
        """Organiza los componentes mediante gestor de malla (equivalente a GridBagLayout)."""
        contenedor = tk.Frame(self, padx=12, pady=10)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)

        # Fila 0: Número de habitación
        tk.Label(
            contenedor, text=f"Habitación: {self.numero_habitacion}", anchor="w"
        ).grid(row=0, column=0, sticky="ew", padx=3, pady=3)

        # Fila 1: Fecha de ingreso
        fecha_ing = self.hotel.buscar_fecha_ingreso_habitacion(
            self.numero_habitacion
        )
        tk.Label(
            contenedor, text=f"Fecha de ingreso: {fecha_ing}", anchor="w"
        ).grid(row=1, column=0, sticky="ew", padx=3, pady=3)

        # Fila 2 y 3: Fecha de salida
        tk.Label(
            contenedor, text="Fecha de salida (aaaa-mm-dd):", anchor="w"
        ).grid(row=2, column=0, sticky="ew", padx=3, pady=3)

        self.campo_fecha_salida = tk.Entry(contenedor)
        self.campo_fecha_salida.grid(row=3, column=0, sticky="ew", padx=3, pady=3)

        # Fila 4: Botón Calcular
        self.calcular = tk.Button(
            contenedor, text="Calcular", command=self.calcular_pago
        )
        self.calcular.grid(row=4, column=0, sticky="ew", padx=3, pady=4)

        # Fila 5: Cantidad de días
        self.cantidad_dias = tk.Label(
            contenedor, text="Cantidad de días:", anchor="w"
        )
        self.cantidad_dias.grid(row=5, column=0, sticky="ew", padx=3, pady=3)

        # Fila 6: Total a pagar
        self.total_pago = tk.Label(contenedor, text="Total: $", anchor="w")
        self.total_pago.grid(row=6, column=0, sticky="ew", padx=3, pady=3)

        # Fila 7: Botón RegistrarSalida (inicialmente deshabilitado)
        self.registrar_salida = tk.Button(
            contenedor,
            text="RegistrarSalida",
            state="disabled",
            command=self.confirmar_salida,
        )
        self.registrar_salida.grid(row=7, column=0, sticky="ew", padx=3, pady=4)

    def calcular_pago(self) -> None:
        """Valida la fecha de salida y calcula días y valor total."""
        fecha_s = self.campo_fecha_salida.get().strip()
        for habitacion in self.hotel.lista_habitaciones:
            if habitacion.get_numero_habitacion() == self.numero_habitacion:
                self.habitacion_ocupada = habitacion
                try:
                    fecha2 = datetime.strptime(fecha_s, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror(
                        "Mensaje",
                        "La fecha no está en el formato solicitado",
                        parent=self,
                    )
                    return

                huesped = habitacion.get_huesped()
                if huesped is None or huesped.get_fecha_ingreso() is None:
                    return

                fecha1 = huesped.get_fecha_ingreso()
                if fecha1 < fecha2:
                    huesped.set_fecha_salida(fecha2)
                    cantidad = huesped.obtener_dias_alojamiento()
                    self.cantidad_dias.config(
                        text=f"Cantidad de días: {cantidad}"
                    )
                    valor = cantidad * habitacion.get_precio_dia()
                    self.total_pago.config(text=f"Total: ${valor:.1f}")
                    self.registrar_salida.config(state="normal")
                else:
                    messagebox.showerror(
                        "Mensaje",
                        "La fecha de salida es menor que la de ingreso",
                        parent=self,
                    )
                return

    def confirmar_salida(self) -> None:
        """Libera la habitación y confirma la salida del huésped."""
        if self.habitacion_ocupada is not None:
            self.habitacion_ocupada.set_huesped(None)
            self.habitacion_ocupada.set_disponible(True)
            messagebox.showinfo(
                "Mensaje",
                "Se ha registrado la salida del huésped",
                parent=self,
            )
            self.destroy()


class VentanaPrincipal(tk.Tk):
    """Ventana principal de la aplicación de gestión del hotel."""

    def __init__(self, hotel: Hotel) -> None:
        super().__init__()
        self.hotel = hotel
        self.title("Hotel")
        self.resizable(False, False)
        self._centrar_ventana(280, 380)
        self.inicio()

    def _centrar_ventana(self, ancho: int, alto: int) -> None:
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def inicio(self) -> None:
        """Crea la barra de menús con las opciones de consulta y salida."""
        barra_menu = tk.Menu(self)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)

        menu_opciones.add_command(
            label="Consultar habitaciones",
            command=self.abrir_consultar_habitaciones,
        )
        menu_opciones.add_command(
            label="Salida de huéspedes",
            command=self.abrir_salida_huespedes,
        )

        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.config(menu=barra_menu)

    def abrir_consultar_habitaciones(self) -> None:
        VentanaHabitaciones(self, self.hotel)

    def abrir_salida_huespedes(self) -> None:
        numero_texto = simpledialog.askstring(
            "Salida de huéspedes",
            "Ingrese número de habitación",
            parent=self,
        )
        if numero_texto is None:
            return

        try:
            numero = int(numero_texto.strip())
            if numero < 1 or numero > 10:
                messagebox.showinfo(
                    "Mensaje",
                    "El número de habitación debe estar entre 1 y 10",
                    parent=self,
                )
            elif self.hotel.buscar_habitacion_ocupada(numero):
                VentanaSalida(self, self.hotel, numero)
            else:
                messagebox.showinfo(
                    "Mensaje",
                    "La habitación ingresada no ha sido ocupada",
                    parent=self,
                )
        except ValueError:
            messagebox.showerror(
                "Error",
                "Campo nulo o error en formato de número",
                parent=self,
            )


# ==============================================================================
# PUNTO DE ENTRADA
# ==============================================================================

class Principal:
    """Punto de ingreso al programa de ingreso y salida de huéspedes."""

    @staticmethod
    def main() -> None:
        hotel = Hotel()
        mi_ventana_principal = VentanaPrincipal(hotel)
        mi_ventana_principal.mainloop()


if __name__ == "__main__":
    Principal.main()