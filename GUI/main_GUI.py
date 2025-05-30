import tkinter as tk
from tkinter import ttk
from event_gui import EventManagerApp
from venue_gui import VenueManagerApp
from event_venue_gui import EventVenueManagerApp
from supplier_gui import SupplierManagerApp
from staff_gui import StaffManagerApp
from ticket_gui import TicketManagerApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestión de Eventos")
    root.geometry("1000x800")

    tabs = ttk.Notebook(root)
    tabs.pack(expand=1, fill="both")

    # Pasa el Notebook a cada interfaz
    event_app = EventManagerApp(tabs)
    venue_app = VenueManagerApp(tabs)
    assign_app = EventVenueManagerApp(tabs)
    supplier_app = SupplierManagerApp(tabs)
    staff_app = StaffManagerApp(tabs)
    ticket_app = TicketManagerApp(tabs)

    root.mainloop()
