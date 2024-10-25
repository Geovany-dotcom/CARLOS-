import tkinter as tk
from tkinter import messagebox
from main import ColaCircularDoble

class InterfazEstacionamiento:
    def __init__(self, root):
        self.root = root
        self.root.title("Estacionamiento")
        self.estacionamiento = ColaCircularDoble()

        # Etiquetas y entradas
        self.label_placas = tk.Label(root, text="Placas del auto:")
        self.label_placas.pack()

        self.entry_placas = tk.Entry(root)
        self.entry_placas.pack()

        self.label_propietario = tk.Label(root, text="Propietario:")
        self.label_propietario.pack()

        self.entry_propietario = tk.Entry(root)
        self.entry_propietario.pack()

        # Botón de ingreso
        self.boton_ingresar = tk.Button(root, text="Ingresar Auto", command=self.ingresar_auto)
        self.boton_ingresar.pack()

        # Botón de salida
        self.boton_sacar = tk.Button(root, text="Sacar Auto", command=self.sacar_auto)
        self.boton_sacar.pack()

    def ingresar_auto(self):
        placas = self.entry_placas.get()
        propietario = self.entry_propietario.get()

        if placas and propietario:
            mensaje = self.estacionamiento.ingresar_auto(placas, propietario)
            messagebox.showinfo("Ingreso Exitoso", mensaje)
            self.entry_placas.delete(0, tk.END)
            self.entry_propietario.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Por favor, ingrese todos los datos.")

    def sacar_auto(self):
        mensaje = self.estacionamiento.sacar_auto()
        messagebox.showinfo("Salida de Auto", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazEstacionamiento(root)
    root.mainloop()
