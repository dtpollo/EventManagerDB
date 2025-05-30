import tkinter as tk
from tkinter import ttk, messagebox
import requests
from URL import DATABASE_URL as URL

class VenueManagerApp:
    def __init__(self, tabs):
        self.tabs = tabs
        self.venue_tab()


    def venue_tab(self):
        # Crea la pestaña de venues
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Localidades")
        frm_top = ttk.Frame(tab, padding=10)
        frm_top.pack()  # tabs arriba

        # Crea las cajas de texto y el botón para crear venues
        ttk.Label(frm_top, text="Nombre de la Localidad").grid(row=0, column=0, sticky="e")
        self.vn_name = tk.Entry(frm_top, width=40)
        self.vn_name.grid(row=0, column=1)

        ttk.Label(frm_top, text="Tipo (General, VIP, Premium)").grid(row=1, column=0, sticky="e")
        self.vn_type = tk.Entry(frm_top, width=40)
        self.vn_type.grid(row=1, column=1)

        ttk.Label(frm_top, text="Capacidad de la Localidad").grid(row=2, column=0, sticky="e")
        self.vn_capacity = tk.Entry(frm_top, width=40)
        self.vn_capacity.grid(row=2, column=1)

        ttk.Button(frm_top, text="Crear Localidad", command=self.create_venue).grid(row=3, column=1, pady=10) # Botón

        # ----- Sección de abajo: consultar y eliminar -----
        frm_bottom = ttk.LabelFrame(tab, text="Localidades", padding=10)
        frm_bottom.pack(fill="x", padx=10, pady=5)

        # Botón para consultar
        ttk.Button(frm_bottom, text="Consultar", command=self.load_venues).grid(row=0, column=0, sticky="w")

        # Eliminar por ID
        ttk.Label(frm_bottom, text="ID a eliminar:").grid(row=1, column=0, sticky="e", pady=5)
        self.delete_event_id = tk.Entry(frm_bottom, width=10)
        self.delete_event_id.grid(row=1, column=1, sticky="w")
        ttk.Button(frm_bottom, text="Eliminar localidad", command=self.delete_event).grid(row=1, column=2, padx=10)

        # Lista de localidades
        list_frame = ttk.Frame(frm_bottom)
        list_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        frm_bottom.rowconfigure(2, weight=1)
        frm_bottom.columnconfigure(0, weight=1)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(list_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")


        self.venue_list = tk.Text(list_frame, wrap="none", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.venue_list.pack(expand=True, fill="both")

        self.venue_list.pack(expand=True, fill="both")

        # Configurar scrollbars
        scrollbar_y.config(command=self.venue_list.yview)
        scrollbar_x.config(command=self.venue_list.xview)


    def create_venue(self):
        data = {
            "vn_name": self.vn_name.get(),
            "vn_type": self.vn_type.get(),
            "vn_capacity": self.vn_capacity.get()
        }

        try:
            res = requests.post(f"{URL}/venues", json=data)
            if res.status_code == 201:
                messagebox.showinfo("Exito", "Localidad creada correctamente.")
                # Limpia los campos de entrada
                self.vn_name.delete(0, tk.END)
                self.vn_type.delete(0, tk.END)
                self.vn_capacity.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Error {res.status_code}: {res.json().get('Error')}")
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    def load_venues(self):
        try:
            res = requests.get(f"{URL}/venues")
            if res.status_code == 200:
                localidades = res.json()
                self.venue_list.config(state="normal")
                self.venue_list.delete(1.0, tk.END)
                for l in localidades:
                    linea = f"ID: {l['vn_id']} |- Nombre: {l['vn_name']} | Tipo: {l['vn_type']} | Capacidad: {l['vn_capacity']}\n"
                    self.venue_list.insert(tk.END, linea)
                self.venue_list.config(state="disabled")
            else:
                messagebox.showerror("Error", "No se encontraron localidades.")
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    def delete_event(self):
        venue_id = self.delete_event_id.get()
        if not venue_id.isdigit():
            messagebox.showerror("Error", "Debes ingresar un ID valido.")
            return

        try:
            res = requests.delete(f"{URL}/venues/{venue_id}")
            if res.status_code == 200:
                messagebox.showinfo("Exito", "Localidad eliminada correctamente.")
                self.delete_event_id.delete(0, tk.END)
                self.load_venues()
            else:
                messagebox.showerror("Error", res.json().get("Error", "No se pudo eliminar"))
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))