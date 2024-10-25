import tkinter as tk
from tkinter import messagebox, ttk
from main import ColaCircularDoble

class InterfazEstacionamiento:
    def __init__(self, root):
        self.root = root
        self.root.title("Estacionamiento de Autos")
        self.root.geometry("400x400")
        self.root.configure(bg="#F0F0F0")
        self.estacionamiento = ColaCircularDoble()

        # Frame principal
        main_frame = tk.Frame(root, bg="#F0F0F0")
        main_frame.pack(pady=10, padx=10)

        # Etiquetas y entradas
        tk.Label(main_frame, text="Placas del auto:", bg="#F0F0F0", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.entry_placas = tk.Entry(main_frame)
        self.entry_placas.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(main_frame, text="Propietario:", bg="#F0F0F0", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w")
        self.entry_propietario = tk.Entry(main_frame)
        self.entry_propietario.grid(row=1, column=1, pady=5, padx=5)

        # Botón de ingreso
        self.boton_ingresar = tk.Button(main_frame, text="Ingresar Auto", command=self.ingresar_auto, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.boton_ingresar.grid(row=2, column=0, columnspan=2, pady=10)

        # Botón de salida
        self.boton_sacar = tk.Button(root, text="Sacar Auto", command=self.sacar_auto, bg="#FF5722", fg="white", font=("Arial", 10, "bold"))
        self.boton_sacar.pack(pady=5)

        # Lista de autos en el estacionamiento
        tk.Label(root, text="Autos en el estacionamiento:", bg="#F0F0F0", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Agregar scrollbar para lista de autos
        list_frame = tk.Frame(root)
        list_frame.pack()
        self.scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.lista_autos = tk.Listbox(list_frame, width=50, height=10, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lista_autos.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_autos.pack(side=tk.LEFT, fill=tk.BOTH)

    def ingresar_auto(self):
        placas = self.entry_placas.get()
        propietario = self.entry_propietario.get()

        if placas and propietario:
            mensaje = self.estacionamiento.ingresar_auto(placas, propietario)
            messagebox.showinfo("Ingreso Exitoso", mensaje)
            self.entry_placas.delete(0, tk.END)
            self.entry_propietario.delete(0, tk.END)
            self.actualizar_lista_autos()
        else:
            messagebox.showerror("Error", "Por favor, ingrese todos los datos.")

    def sacar_auto(self):
        mensaje = self.estacionamiento.sacar_auto()
        messagebox.showinfo("Salida de Auto", mensaje)
        self.actualizar_lista_autos()

    def actualizar_lista_autos(self):
        self.lista_autos.delete(0, tk.END)

        if not self.estacionamiento.esta_vacia():
            nodo_actual = self.estacionamiento.cabeza
            while True:
                auto_info = f"Placas: {nodo_actual.placas}, Propietario: {nodo_actual.propietario}, Hora entrada: {nodo_actual.hora_entrada.strftime('%H:%M:%S')}"
                self.lista_autos.insert(tk.END, auto_info)
                nodo_actual = nodo_actual.siguiente
                if nodo_actual == self.estacionamiento.cabeza:
                    break
        else:
            self.lista_autos.insert(tk.END, "No hay autos en el estacionamiento.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazEstacionamiento(root)
    root.mainloop()
