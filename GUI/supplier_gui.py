import tkinter as tk
from tkinter import ttk, messagebox
import requests
from URL import DATABASE_URL as URL

class SupplierManagerApp:
    def __init__(self, tabs):
        self.tabs = tabs
        self.supplier_tab()

    def supplier_tab(self):
        # Crea la pestaña de suppliers
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Proveedores")
        frm_top = ttk.Frame(tab, padding=10)
        frm_top.pack() # tabs arriba 

        # Crea las cajas de texto y el botón para crear proveedores
        ttk.Label(frm_top, text="Nombre del proveedor").grid(row=0, column=0, sticky="e")
        self.sup_name = tk.Entry(frm_top, width=40)
        self.sup_name.grid(row=0, column=1)

        ttk.Label(frm_top, text="Descripcion del servicio").grid(row=1, column=0, sticky="e")
        self.sup_service = tk.Entry(frm_top, width=40)
        self.sup_service.grid(row=1, column=1)

        ttk.Label(frm_top, text="Contacto").grid(row=2, column=0, sticky="e")
        self.sup_contact = tk.Entry(frm_top, width=40)
        self.sup_contact.grid(row=2, column=1)

        ttk.Button(frm_top, text="Crear proveedor", command=self.create_supplier).grid(row=3, column=1, pady=10) # Botón

        # ----- Sección de abajo: consultar y eliminar -----
        frm_bottom = ttk.LabelFrame(tab, text="Proveedores", padding=10)
        frm_bottom.pack(fill="x", padx=10, pady=5)

        # Botón para consultar
        ttk.Button(frm_bottom, text="Consultar proveedores", command=self.load_suppliers).grid(row=0, column=0, sticky="w")

        # Eliminar por ID
        ttk.Label(frm_bottom, text="ID a eliminar:").grid(row=1, column=0, sticky="e", pady=5)
        self.delete_supplier_id = tk.Entry(frm_bottom, width=10)
        self.delete_supplier_id.grid(row=1, column=1, sticky="w")
        ttk.Button(frm_bottom, text="Eliminar proveedor", command=self.delete_supplier).grid(row=1, column=2, padx=10)

        # Lista de proveedores
        list_frame = ttk.Frame(frm_bottom)
        list_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        frm_bottom.rowconfigure(2, weight=1)
        frm_bottom.columnconfigure(0, weight=1)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(list_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")


        self.sup_list = tk.Text(list_frame, wrap="none", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.sup_list.pack(expand=True, fill="both")

        self.sup_list.pack(expand=True, fill="both")

        # Configurar scrollbars
        scrollbar_y.config(command=self.sup_list.yview)
        scrollbar_x.config(command=self.sup_list.xview)


    def create_supplier(self):
        data = {
            "sup_company_name": self.sup_name.get(),
            "sup_service_type": self.sup_service.get(),
            "sup_contact_number": self.sup_contact.get()
        }

        try:
            res = requests.post(f"{URL}/suppliers", json=data)
            if res.status_code == 201:
                messagebox.showinfo("Exito", "Proveedor creado correctamente.")
                # Limpia los campos de entrada
                self.sup_name.delete(0, tk.END)
                self.sup_service.delete(0, tk.END)
                self.sup_contact.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Error {res.status_code}: {res.json().get('Error')}")
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    def load_suppliers(self):
        try:
            res = requests.get(f"{URL}/suppliers")
            if res.status_code == 200:
                proveedores = res.json()
                self.sup_list.config(state="normal")
                self.sup_list.delete(1.0, tk.END)
                for p in proveedores:
                    linea = f"ID: {p['sup_id']} |- Nombre: {p['sup_company_name']} | Contacto: {p['sup_contact_number']} | Servicio: {p['sup_service_type']}\n"
                    self.sup_list.insert(tk.END, linea)
                self.sup_list.config(state="disabled")
            else:
                messagebox.showerror("Error", "No se encontraron proveedores.")
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    def delete_supplier(self):
        supplier_id = self.delete_supplier_id.get()
        if not supplier_id.isdigit():
            messagebox.showerror("Error", "Debes ingresar un ID valido.")
            return

        try:
            res = requests.delete(f"{URL}/suppliers/{supplier_id}")
            if res.status_code == 200:
                messagebox.showinfo("Exito", "Proveedor eliminado correctamente.")
                self.delete_supplier_id.delete(0, tk.END)
                self.load_suppliers()
            else:
                messagebox.showerror("Error", res.json().get("Error", "No se pudo eliminar"))
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))