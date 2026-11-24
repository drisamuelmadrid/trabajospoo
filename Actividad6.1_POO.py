import os
import tkinter as tk
from tkinter import messagebox


# =====================================================================
# 1. CLASE MODELO: Representa la entidad Contacto
# =====================================================================
class Contacto:
    def __init__(self, nombre: str, numero: int):
        self.nombre = nombre.strip()
        self.numero = int(numero)

    def a_formato_archivo(self) -> str:
        """Convierte el objeto al formato 'Nombre!Numero' del material guía."""
        return f"{self.nombre}!{self.numero}"

    @staticmethod
    def desde_linea(linea: str):
        """Crea un objeto Contacto a partir de una línea del archivo de texto."""
        partes = linea.strip().split("!")
        if len(partes) == 2 and partes[1].isdigit():
            return Contacto(partes[0], int(partes[1]))
        return None


# =====================================================================
# 2. CLASE DE PERSISTENCIA: Gestiona el CRUD en 'friendsContact.txt'
# =====================================================================
class GestorContactos:
    def __init__(self, ruta_archivo: str = "friendsContact.txt"):
        self.ruta_archivo = ruta_archivo
        # Crea el archivo si no existe
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w", encoding="utf-8"):
                pass

    def _leer_todos(self) -> list[Contacto]:
        """Método auxiliar que carga todos los contactos desde el archivo."""
        contactos = []
        with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                contacto = Contacto.desde_linea(linea)
                if contacto:
                    contactos.append(contacto)
        return contactos

    def _guardar_todos(self, contactos: list[Contacto]) -> None:
        """Método auxiliar que sobrescribe el archivo con la lista actualizada."""
        with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
            for contacto in contactos:
                archivo.write(contacto.a_formato_archivo() + "\n")

    def create(self, nuevo_contacto: Contacto) -> tuple[bool, str]:
        """CREATE: Agrega un contacto si el nombre o número no existen."""
        contactos = self._leer_todos()
        for c in contactos:
            if c.nombre.lower() == nuevo_contacto.nombre.lower() or c.numero == nuevo_contacto.numero:
                return False, "El nombre o el número ya existen en el archivo."

        with open(self.ruta_archivo, "a", encoding="utf-8") as archivo:
            archivo.write(nuevo_contacto.a_formato_archivo() + "\n")
        return True, "Contacto agregado exitosamente."

    def read(self, nombre_buscar: str = "") -> tuple[bool, str, list[Contacto]]:
        """READ: Busca un contacto por nombre o devuelve todos si está vacío."""
        contactos = self._leer_todos()
        if not nombre_buscar.strip():
            return True, f"Se encontraron {len(contactos)} contacto(s).", contactos

        for c in contactos:
            if c.nombre.lower() == nombre_buscar.strip().lower():
                return True, f"Contacto encontrado: {c.nombre} - {c.numero}", [c]

        return False, "Contacto no encontrado.", []

    def update(self, nombre: str, nuevo_numero: int) -> tuple[bool, str]:
        """UPDATE: Actualiza el número de un contacto existente por su nombre."""
        contactos = self._leer_todos()
        encontrado = False

        for c in contactos:
            if c.nombre.lower() == nombre.strip().lower():
                c.numero = nuevo_numero
                encontrado = True
                break

        if not encontrado:
            return False, "No se encontró el contacto para actualizar."

        self._guardar_todos(contactos)
        return True, "Contacto actualizado exitosamente."

    def delete(self, nombre: str) -> tuple[bool, str]:
        """DELETE: Elimina un contacto del archivo por su nombre."""
        contactos = self._leer_todos()
        nuevos_contactos = [
            c for c in contactos if c.nombre.lower() != nombre.strip().lower()
        ]

        if len(nuevos_contactos) == len(contactos):
            return False, "No se encontró el contacto para eliminar."

        self._guardar_todos(nuevos_contactos)
        return True, "Contacto eliminado exitosamente."


# =====================================================================
# 3. CLASE INTERFAZ GRÁFICA (GUI): Formulario con botones CRUD
# =====================================================================
class InterfazContactos:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Gestión de Contactos - POO Actividad 6")
        self.root.geometry("460x420")
        self.root.resizable(False, False)

        self.gestor = GestorContactos("friendsContact.txt")

        self._construir_interfaz()
        self._actualizar_lista_visual()

    def _construir_interfaz(self):
        # Título
        lbl_titulo = tk.Label(
            self.root,
            text="Agenda de Contactos (friendsContact.txt)",
            font=("Arial", 13, "bold"),
        )
        lbl_titulo.pack(pady=12)

        # Marco de formulario
        frame_form = tk.Frame(self.root)
        frame_form.pack(pady=5)

        tk.Label(frame_form, text="Nombre:", font=("Arial", 10)).grid(
            row=0, column=0, padx=8, pady=6, sticky="e"
        )
        self.entry_nombre = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_nombre.grid(row=0, column=1, padx=8, pady=6)

        tk.Label(frame_form, text="Número:", font=("Arial", 10)).grid(
            row=1, column=0, padx=8, pady=6, sticky="e"
        )
        self.entry_numero = tk.Entry(frame_form, width=30, font=("Arial", 10))
        self.entry_numero.grid(row=1, column=1, padx=8, pady=6)

        # Marco de botones CRUD (Create, Read, Update, Delete)
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=12)

        btn_create = tk.Button(
            frame_botones, text="Create", width=9, bg="#4CAF50", fg="white",
            font=("Arial", 10, "bold"), command=self.accion_create
        )
        btn_create.grid(row=0, column=0, padx=5)

        btn_read = tk.Button(
            frame_botones, text="Read", width=9, bg="#2196F3", fg="white",
            font=("Arial", 10, "bold"), command=self.accion_read
        )
        btn_read.grid(row=0, column=1, padx=5)

        btn_update = tk.Button(
            frame_botones, text="Update", width=9, bg="#FF9800", fg="white",
            font=("Arial", 10, "bold"), command=self.accion_update
        )
        btn_update.grid(row=0, column=2, padx=5)

        btn_delete = tk.Button(
            frame_botones, text="Delete", width=9, bg="#F44336", fg="white",
            font=("Arial", 10, "bold"), command=self.accion_delete
        )
        btn_delete.grid(row=0, column=3, padx=5)

        # Lista visual para evidenciar los cambios en el archivo
        tk.Label(
            self.root, text="Registros actuales en el archivo:", font=("Arial", 9, "bold")
        ).pack(pady=(5, 2))

        self.listbox_contactos = tk.Listbox(self.root, width=52, height=9, font=("Consolas", 10))
        self.listbox_contactos.pack(pady=5)
        self.listbox_contactos.bind("<<ListboxSelect>>", self._seleccionar_de_lista)

        # Botón auxiliar para limpiar campos
        tk.Button(
            self.root, text="Limpiar campos", font=("Arial", 9), command=self._limpiar_campos
        ).pack(pady=4)

    def _limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_numero.delete(0, tk.END)

    def _actualizar_lista_visual(self):
        self.listbox_contactos.delete(0, tk.END)
        _, _, contactos = self.gestor.read()
        for c in contactos:
            self.listbox_contactos.insert(tk.END, f"{c.nombre}  |  {c.numero}")

    def _seleccionar_de_lista(self, event):
        seleccion = self.listbox_contactos.curselection()
        if seleccion:
            texto = self.listbox_contactos.get(seleccion[0])
            nombre, numero = [parte.strip() for parte in texto.split("|")]
            self._limpiar_campos()
            self.entry_nombre.insert(0, nombre)
            self.entry_numero.insert(0, numero)

    # --- Eventos de los 4 botones CRUD ---
    def accion_create(self):
        nombre = self.entry_nombre.get().strip()
        numero = self.entry_numero.get().strip()

        if not nombre or not numero:
            messagebox.showwarning("Campos vacíos", "Ingresa el nombre y el número.")
            return
        if not numero.isdigit():
            messagebox.showerror("Error de formato", "El número debe contener solo dígitos.")
            return

        exito, mensaje = self.gestor.create(Contacto(nombre, int(numero)))
        if exito:
            messagebox.showinfo("Create", mensaje)
            self._limpiar_campos()
            self._actualizar_lista_visual()
        else:
            messagebox.showwarning("Create", mensaje)

    def accion_read(self):
        nombre = self.entry_nombre.get().strip()
        exito, mensaje, encontrados = self.gestor.read(nombre)
        self._actualizar_lista_visual()

        if exito and nombre:
            self.entry_numero.delete(0, tk.END)
            self.entry_numero.insert(0, str(encontrados[0].numero))
            messagebox.showinfo("Read", mensaje)
        elif not exito:
            messagebox.showwarning("Read", mensaje)

    def accion_update(self):
        nombre = self.entry_nombre.get().strip()
        numero = self.entry_numero.get().strip()

        if not nombre or not numero:
            messagebox.showwarning("Campos vacíos", "Ingresa el nombre existente y el nuevo número.")
            return
        if not numero.isdigit():
            messagebox.showerror("Error de formato", "El número debe contener solo dígitos.")
            return

        exito, mensaje = self.gestor.update(nombre, int(numero))
        if exito:
            messagebox.showinfo("Update", mensaje)
            self._limpiar_campos()
            self._actualizar_lista_visual()
        else:
            messagebox.showwarning("Update", mensaje)

    def accion_delete(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Campo vacío", "Ingresa el nombre del contacto a eliminar.")
            return

        exito, mensaje = self.gestor.delete(nombre)
        if exito:
            messagebox.showinfo("Delete", mensaje)
            self._limpiar_campos()
            self._actualizar_lista_visual()
        else:
            messagebox.showwarning("Delete", mensaje)


if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazContactos(ventana)
    ventana.mainloop()