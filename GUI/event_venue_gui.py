import tkinter as tk
from tkinter import ttk, messagebox
import requests
from URL import DATABASE_URL as URL

class EventVenueManagerApp:
    def __init__(self, tabs):
        self.tabs = tabs
        self.event_venue_tab()


    def event_venue_tab(self):
        # Crea la pestaña de event_venues
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Assignar Localidad a Evento")
        frm_top = ttk.Frame(tab, padding=10)
        frm_top.pack()  # tabs arriba

        # Crea las cajas de texto y el botón para asigna localidades a eventos
        ttk.Label(frm_top, text="ID de la localidad").grid(row=0, column=0, sticky="e")
        self.vn_name = tk.Entry(frm_top, width=40)
        self.vn_name.grid(row=0, column=1)

        ttk.Label(frm_top, text="ID del Evento").grid(row=1, column=0, sticky="e")
        self.vn_type = tk.Entry(frm_top, width=40)
        self.vn_type.grid(row=1, column=1)


        ttk.Button(frm_top, text="Asignar la localidad al Evento", command=self.create_assig).grid(row=3, column=1, pady=10) # Botón

        # ----- Sección de abajo: consultar y eliminar -----
        frm_bottom = ttk.LabelFrame(tab, text="Asignaciones - Localidades", padding=10)
        frm_bottom.pack(fill="x", padx=10, pady=5)

        # Botón para consultar
        ttk.Button(frm_bottom, text="Consultar", command=self.load_assig).grid(row=0, column=0, sticky="w")

        # Eliminar por ID
        ttk.Label(frm_bottom, text="ID a eliminar:").grid(row=1, column=0, sticky="e", pady=5)
        self.delete_event_venue_id = tk.Entry(frm_bottom, width=10)
        self.delete_event_venue_id.grid(row=1, column=1, sticky="w")
        ttk.Button(frm_bottom, text="Eliminar Asignacion", command=self.delete_event).grid(row=1, column=2, padx=10)

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


        self.assig_list = tk.Text(list_frame, wrap="none", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.assig_list.pack(expand=True, fill="both")

        self.assig_list.pack(expand=True, fill="both")

        # Configurar scrollbars
        scrollbar_y.config(command=self.assig_list.yview)
        scrollbar_x.config(command=self.assig_list.xview)


    def create_assig(self):
        data = {
            "vn_id": self.vn_name.get(),
            "ev_id": self.vn_type.get()
        }

        try:
            res = requests.post(f"{URL}/event_venues", json=data)
            if res.status_code == 201:
                messagebox.showinfo("Éxito", "Localidad asignada al evento correctamente.")
                # Limpia los campos de entrada
                self.vn_name.delete(0, tk.END)
                self.vn_type.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Error {res.status_code}: {res.json().get('Error')}")
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))

    def load_assig(self):
        try:
            res = requests.get(f"{URL}/event_venues")
            if res.status_code == 200:
                localidades = res.json()
                self.assig_list.config(state="normal")
                self.assig_list.delete(1.0, tk.END)
                for l in localidades:
                    linea = f"ID: {l['ev_ven_id']} |- ID EVENTO: {l['ev_id']} | ID LOCALIDAD: {l['vn_id']}\n"
                    self.assig_list.insert(tk.END, linea)
                self.assig_list.config(state="disabled")
            else:
                messagebox.showerror("Error", "No se encontraron localidades.")
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    def delete_event(self):
        assig_id = self.delete_event_venue_id.get()
        if not assig_id.isdigit():
            messagebox.showerror("Error", "Debes ingresar un ID válido.")
            return

        try:
            res = requests.delete(f"{URL}/event_venues/{assig_id}")
            if res.status_code == 200:
                messagebox.showinfo("Éxito", "Assignacion eliminada correctamente.")
                self.delete_event_venue_id.delete(0, tk.END)
                self.load_assig()
            else:
                messagebox.showerror("Error", res.json().get("Error", "No se pudo eliminar"))
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))