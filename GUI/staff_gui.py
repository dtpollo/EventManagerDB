import tkinter as tk
from tkinter import ttk, messagebox
import requests
from URL import DATABASE_URL as URL

class StaffManagerApp:
    def __init__(self, tabs):
        self.tabs = tabs
        self.staff_tab()


    def staff_tab(self):
        # Crea la pestaña de staff
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Gestión de Personal")
        frm_top = ttk.Frame(tab, padding=10)
        frm_top.pack()  # tabs arriba

        # Crea las cajas de texto y el botón para gestionar el Trabajador
        ttk.Label(frm_top, text="Nombre del Trabajador").grid(row=0, column=0, sticky="e")
        self.stf_name = tk.Entry(frm_top, width=40)
        self.stf_name.grid(row=0, column=1)

        ttk.Label(frm_top, text="Apellido del Trabajador").grid(row=1, column=0, sticky="e")
        self.stf_last_name = tk.Entry(frm_top, width=40)
        self.stf_last_name.grid(row=1, column=1)

        ttk.Label(frm_top, text="ID de la Empresa").grid(row=2, column=0, sticky="e")
        self.sup_id = tk.Entry(frm_top, width=40)
        self.sup_id.grid(row=2, column=1)

        ttk.Label(frm_top, text="Rol en la Empresa").grid(row=3, column=0, sticky="e")
        self.stf_role = tk.Entry(frm_top, width=40)
        self.stf_role.grid(row=3, column=1)

        ttk.Label(frm_top, text="Tareas Asignadas").grid(row=4, column=0, sticky="e")
        self.stf_tasks = tk.Entry(frm_top, width=40)
        self.stf_tasks.grid(row=4, column=1)

        ttk.Button(frm_top, text="Crear Trabajador", command=self.create_assigSTF).grid(row=5, column=1, pady=10) # Botón

        # ----- Sección de abajo: consultar y eliminar -----
        frm_bottom = ttk.LabelFrame(tab, text="Asignaciones - Trabajadores", padding=10)
        frm_bottom.pack(fill="x", padx=10, pady=5)

        # Botón para consultar
        ttk.Button(frm_bottom, text="Consultar", command=self.load_assigSTF).grid(row=0, column=0, sticky="w")

        # Eliminar por ID
        ttk.Label(frm_bottom, text="ID a eliminar:").grid(row=1, column=0, sticky="e", pady=5)
        self.delete_stf_id = tk.Entry(frm_bottom, width=10)
        self.delete_stf_id.grid(row=1, column=1, sticky="w")
        ttk.Button(frm_bottom, text="Eliminar Trabajador", command=self.delete_staff).grid(row=1, column=2, padx=10)

        # Lista de trabajadores
        list_frame = ttk.Frame(frm_bottom)
        list_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        frm_bottom.rowconfigure(2, weight=1)
        frm_bottom.columnconfigure(0, weight=1)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(list_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")


        self.assigSTF_list = tk.Text(list_frame, wrap="none", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.assigSTF_list.pack(expand=True, fill="both")

        self.assigSTF_list.pack(expand=True, fill="both")

        # Configurar scrollbars
        scrollbar_y.config(command=self.assigSTF_list.yview)
        scrollbar_x.config(command=self.assigSTF_list.xview)
        
    def create_assigSTF(self):
        data = {
            "stf_name": self.stf_name.get(),
            "stf_last_name": self.stf_last_name.get(),
            "stf_tasks": self.stf_tasks.get(),
            "stf_role": self.stf_role.get(),
            "sup_id": self.sup_id.get()
        }

        try:
            res = requests.post(f"{URL}/staff", json=data)
            if res.status_code == 201:
                messagebox.showinfo("Éxito", "Trabajador creado correctamente.")
                # Limpia los campos de entrada
                self.stf_name.delete(0, tk.END)
                self.stf_last_name.delete(0, tk.END)
                self.stf_tasks.delete(0, tk.END)
                self.stf_role.delete(0, tk.END)
                self.sup_id.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Error {res.status_code}: {res.json().get('Error')}")
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))

    def load_assigSTF(self):
        try:
            res = requests.get(f"{URL}/staff")
            if res.status_code == 200:
                trabajadores = res.json()
                self.assigSTF_list.config(state="normal")
                self.assigSTF_list.delete(1.0, tk.END)
                for l in trabajadores:
                    linea = f"ID Tra./Emp. : {l['stf_id']} | {l['sup_id']} |- Nombre: {l['stf_name']} | Apellido: {l['stf_last_name']} | Rol: {l['stf_role']} | Tareas: {l['stf_tasks']}\n"
                    self.assigSTF_list.insert(tk.END, linea)
                self.assigSTF_list.config(state="disabled")
            else:
                messagebox.showerror("Error", "No se encontraron trabajadores.")
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    def delete_staff(self):
        assig_id = self.delete_stf_id.get()
        if not assig_id.isdigit():
            messagebox.showerror("Error", "Debes ingresar un ID válido.")
            return

        try:
            res = requests.delete(f"{URL}/staff/{assig_id}")
            if res.status_code == 200:
                messagebox.showinfo("Éxito", "Trabajador eliminado correctamente.")
                self.delete_stf_id.delete(0, tk.END)
                self.load_assig()
            else:
                messagebox.showerror("Error", res.json().get("Error", "No se pudo eliminar"))
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
