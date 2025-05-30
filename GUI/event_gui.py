import tkinter as tk
from tkinter import ttk, messagebox
import requests
from URL import DATABASE_URL as URL

class EventManagerApp:
    def __init__(self, tabs):
        self.tabs = tabs
        self.event_tab()

    def event_tab(self):
        # Crea la pestaña de eventos
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Eventos")
        frm_top = ttk.Frame(tab, padding=10)
        frm_top.pack() # tabs arriba 

        # Crea las cajas de texto y el botón para crear eventos
        ttk.Label(frm_top, text="Nombre del evento").grid(row=0, column=0, sticky="e")
        self.ev_name = tk.Entry(frm_top, width=40)
        self.ev_name.grid(row=0, column=1)

        ttk.Label(frm_top, text="Descripcion").grid(row=1, column=0, sticky="e")
        self.ev_desc = tk.Entry(frm_top, width=40)
        self.ev_desc.grid(row=1, column=1)

        ttk.Label(frm_top, text="Fecha (YYYY-MM-DD)").grid(row=2, column=0, sticky="e")
        self.ev_date = tk.Entry(frm_top, width=40)
        self.ev_date.grid(row=2, column=1)

        ttk.Button(frm_top, text="Crear evento", command=self.create_event).grid(row=3, column=1, pady=10) # Botón 

        # ----- Sección de abajo: consultar y eliminar -----
        frm_bottom = ttk.LabelFrame(tab, text="Gestión de eventos", padding=10)
        frm_bottom.pack(fill="x", padx=10, pady=5)

        # Botón para consultar
        ttk.Button(frm_bottom, text="Consultar eventos", command=self.load_events).grid(row=0, column=0, sticky="w")

        # Eliminar por ID
        ttk.Label(frm_bottom, text="ID a eliminar:").grid(row=1, column=0, sticky="e", pady=5)
        self.delete_event_id = tk.Entry(frm_bottom, width=10)
        self.delete_event_id.grid(row=1, column=1, sticky="w")
        ttk.Button(frm_bottom, text="Eliminar evento", command=self.delete_event).grid(row=1, column=2, padx=10)

        # Lista de eventos
        list_frame = ttk.Frame(frm_bottom)
        list_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        frm_bottom.rowconfigure(2, weight=1)
        frm_bottom.columnconfigure(0, weight=1)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(list_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")


        self.event_list = tk.Text(list_frame, wrap="none", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.event_list.pack(expand=True, fill="both")

        self.event_list.pack(expand=True, fill="both")

        # Configurar scrollbars
        scrollbar_y.config(command=self.event_list.yview)
        scrollbar_x.config(command=self.event_list.xview)


    def create_event(self):
        data = {
            "ev_name": self.ev_name.get(),
            "ev_description": self.ev_desc.get(),
            "ev_date": self.ev_date.get()
        }

        try:
            res = requests.post(f"{URL}/events", json=data)
            if res.status_code == 201:
                messagebox.showinfo("Exito", "Evento creado correctamente.")
                # Limpia los campos de entrada
                self.ev_name.delete(0, tk.END)
                self.ev_desc.delete(0, tk.END)
                self.ev_date.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Error {res.status_code}: {res.json().get('Error')}")
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    def load_events(self):
        try:
            res = requests.get(f"{URL}/events")
            if res.status_code == 200:
                eventos = res.json()
                self.event_list.config(state="normal")
                self.event_list.delete(1.0, tk.END)
                for e in eventos:
                    linea = f"ID: {e['ev_id']} |- Nombre: {e['ev_name']} | Fecha: {e['ev_date']}\n"
                    self.event_list.insert(tk.END, linea)
                self.event_list.config(state="disabled")
            else:
                messagebox.showerror("Error", "No se encontraron eventos.")
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    def delete_event(self):
        event_id = self.delete_event_id.get()
        if not event_id.isdigit():
            messagebox.showerror("Error", "Debes ingresar un ID valido.")
            return

        try:
            res = requests.delete(f"{URL}/events/{event_id}")
            if res.status_code == 200:
                messagebox.showinfo("Exito", "Evento eliminado correctamente.")
                self.delete_event_id.delete(0, tk.END)
                self.load_events()
            else:
                messagebox.showerror("Error", res.json().get("Error", "No se pudo eliminar"))
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))