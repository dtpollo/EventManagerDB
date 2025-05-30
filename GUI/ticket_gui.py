import tkinter as tk
from tkinter import ttk, messagebox
import requests
from URL import DATABASE_URL as URL

class TicketManagerApp:
    def __init__(self, tabs):
        self.tabs = tabs
        self.ticket_tab()


    def ticket_tab(self):
        # Crea la pestaña de tickets
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Compra de Tickets")
        frm_top = ttk.Frame(tab, padding=10)
        frm_top.pack()  # tabs arriba

        # Crea las cajas de texto y el botón para gestionar el Asistente
        ttk.Label(frm_top, text="Fecha de Compra (YYYY-MM-DD)").grid(row=0, column=0, sticky="e")
        self.purchase_date = tk.Entry(frm_top, width=40)
        self.purchase_date.grid(row=0, column=1)

        ttk.Label(frm_top, text="Nombre del Asistente").grid(row=1, column=0, sticky="e")
        self.att_name = tk.Entry(frm_top, width=40)
        self.att_name.grid(row=1, column=1)

        ttk.Label(frm_top, text="Apellido del Asistente").grid(row=2, column=0, sticky="e")
        self.att_last_name = tk.Entry(frm_top, width=40)
        self.att_last_name.grid(row=2, column=1)

        ttk.Label(frm_top, text="Email del Asistente").grid(row=3, column=0, sticky="e")
        self.att_email = tk.Entry(frm_top, width=40)
        self.att_email.grid(row=3, column=1)

        ttk.Label(frm_top, text="Telefono del Asistente (09..)").grid(row=4, column=0, sticky="e")
        self.att_phone = tk.Entry(frm_top, width=40)
        self.att_phone.grid(row=4, column=1)

        ttk.Label(frm_top, text="Tipo de Ticket").grid(row=5, column=0, sticky="e")
        self.tic_type_var = tk.StringVar()
        self.tic_type = ttk.Combobox(frm_top, textvariable=self.tic_type_var, state="readonly", width=37)
        self.tic_type['values'] = ["General", "VIP", "Premium"]
        self.tic_type.grid(row=5, column=1)
        self.tic_type.current(0)  # selecciona "General" por defecto


        ttk.Label(frm_top, text="ID del evento").grid(row=6, column=0, sticky="e")
        self.ev_id = tk.Entry(frm_top, width=40)
        self.ev_id.grid(row=6, column=1)

        ttk.Button(frm_top, text="Comprar Ticket", command=self.create_attendee_and_ticket).grid(row=7, column=1, pady=10) # Botón

        # ----- Sección de abajo: consultar y eliminar -----
        frm_bottom = ttk.LabelFrame(tab, text="Tickets", padding=10)
        frm_bottom.pack(fill="x", padx=10, pady=5)

        # Botón para consultar
        ttk.Button(frm_bottom, text="Consultar", command=self.load_purchase).grid(row=0, column=0, sticky="w")

        # Eliminar por ID
        ttk.Label(frm_bottom, text="ID a eliminar:").grid(row=1, column=0, sticky="e", pady=5)
        self.delete_tic_id = tk.Entry(frm_bottom, width=10)
        self.delete_tic_id.grid(row=1, column=1, sticky="w")
        ttk.Button(frm_bottom, text="Eliminar Ticket", command=self.delete_ticket).grid(row=1, column=2, padx=10)

        # Lista de tickets
        list_frame = ttk.Frame(frm_bottom)
        list_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        frm_bottom.rowconfigure(2, weight=1)
        frm_bottom.columnconfigure(0, weight=1)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(list_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = ttk.Scrollbar(list_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")


        self.purchase_list = tk.Text(list_frame, wrap="none", yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.purchase_list.pack(expand=True, fill="both")

        # Configurar scrollbars
        scrollbar_y.config(command=self.purchase_list.yview)
        scrollbar_x.config(command=self.purchase_list.xview)

    def create_attendee_and_ticket(self):
        data1 = {
            "att_name": self.att_name.get(),
            "att_last_name": self.att_last_name.get(),
            "att_email": self.att_email.get(),
            "att_phone": self.att_phone.get(),
        }

        data2 = {
            "tic_type": self.tic_type_var.get(),
            "tic_status_id": 1,
            "ev_id": self.ev_id.get(),
        }


        try:
            res1 = requests.post(f"{URL}/attendees", json=data1)
            if res1.status_code != 201:
                messagebox.showerror("Error", f"Error {res1.status_code}: {res1.json().get('Error')}")
                return
            attendee_id = res1.json().get("att_id")

            res2 = requests.post(f"{URL}/tickets", json=data2)
            if res2.status_code != 201:
                messagebox.showerror("Error", f"Error {res2.status_code}: {res2.json().get('Error')}")
                return
            ticket_id = res2.json().get("tic_id")

            data3 = {
            "purchase_date": self.purchase_date.get(),
            "purchase_type": "Box Office",
            "att_id": attendee_id,
            "tic_id": ticket_id,
            }

            res3 = requests.post(f"{URL}/purchases", json=data3)
            if res3.status_code == 201:
                messagebox.showinfo("Éxito", "Ticket comprado correctamente.")
                # Limpiar campos
                self.att_name.delete(0, tk.END)
                self.att_last_name.delete(0, tk.END)
                self.att_email.delete(0, tk.END)
                self.att_phone.delete(0, tk.END)
                self.tic_type.delete(0, tk.END)
                self.ev_id.delete(0, tk.END)
                self.purchase_date.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Error {res3.status_code}: {res3.json().get('Error')}")

        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))

    def load_purchase(self):
        try:
            res1 = requests.get(f"{URL}/purchases")
            res2 = requests.get(f"{URL}/tickets")

            if res1.status_code == 200 and res2.status_code == 200:
                compras = res1.json()
                tickets = res2.json()

                # Crea un diccionario para acceder rápido por tic_id
                ticket_dict = {t["tic_id"]: t for t in tickets}

                self.purchase_list.config(state="normal")
                self.purchase_list.delete(1.0, tk.END)

                for compra in compras:
                    tic_id = compra["tic_id"]
                    ticket = ticket_dict.get(tic_id, {})
                    linea = f"ID Ticket : {ticket.get('tic_id')} | ID Asistente: {compra.get('att_id')} | Tipo de Ticket: {ticket.get('tic_type')} | Fecha: {compra.get('purchase_date')} | Estado {ticket.get('tic_status_id')}\n"
                    self.purchase_list.insert(tk.END, linea)
                self.purchase_list.config(state="disabled")
            else:
                messagebox.showerror("Error", "No se encontraron compras.")
        except Exception as e:
            messagebox.showerror("Error de conexion", str(e))

    def delete_ticket(self):
        ticket_id = self.delete_tic_id.get()
        if not ticket_id.isdigit():
            messagebox.showerror("Error", "Debes ingresar un ID válido.")
            return

        try:
            res = requests.delete(f"{URL}/tickets/{ticket_id}")
            if res.status_code == 200:
                messagebox.showinfo("Éxito", "Ticket eliminado correctamente.")
                self.delete_tic_id.delete(0, tk.END)
                self.load_purchase()
            else:
                messagebox.showerror("Error", res.json().get("Error", "No se pudo eliminar"))
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
