import os
import tkinter as tk
from tkinter import messagebox
from main import JuegoPintarCoches
import threading
import time
from PIL import Image, ImageTk

class InterfazPintarCoches:
    def __init__(self, root):
        self.root = root
        self.juego = JuegoPintarCoches()
        
        self.tiempo_espera = 5  # Tiempo inicial entre la llegada de coches
        self.tiempo_transcurrido = 0  # Cronómetro

        self.root.title("Juego Pintar Coches")
        self.root.geometry("600x500")
        self.root.config(bg="lightgray")

        # Ruta del directorio de imágenes
        directorio_imagenes = os.path.join(os.path.dirname(__file__), "imagenes")
        
        # Cargar las imágenes de los coches pintados en varios colores
        self.imagenes_coche = self.cargar_imagenes_coches(directorio_imagenes)

        # Mostrar la imagen del coche (coche base)
        self.imagen_label = tk.Label(self.root, image=self.imagenes_coche['default'], bg="lightgray")
        self.imagen_label.pack(pady=10)

        # Mostrar la lista de coches pendientes
        self.cola_frame = tk.Frame(self.root, bg="lightgray")
        self.cola_frame.pack(pady=10)

        # Paleta de colores para pintar
        self.paleta_frame = tk.Frame(self.root, bg="lightgray")
        self.paleta_frame.pack(pady=10)
        self.color_seleccionado = tk.StringVar()
        self.paleta_colores = {
            "amarillo": "yellow",
            "rojo": "red",
            "verde": "green",
            "azul": "blue",
            "gris": "gray"
        }
        
        for color_espanol, color_ingles in self.paleta_colores.items():
            tk.Radiobutton(self.paleta_frame, text=color_espanol.capitalize(), variable=self.color_seleccionado, 
                           value=color_espanol, bg=color_ingles, indicatoron=0, width=10, height=2, 
                           selectcolor="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

        # Botón para confirmar el color
        self.boton_pintar = tk.Button(self.root, text="Pintar Coche", command=self.pintar_carro, bg="black", fg="white", font=("Arial", 12, "bold"))
        self.boton_pintar.pack(pady=10)

        # Mostrar coches pintados
        self.carros_pintados_label = tk.Label(self.root, text="Coches pintados: 0", bg="lightgray", font=("Arial", 12, "bold"))
        self.carros_pintados_label.pack(pady=10)

        # Contador de tiempo
        self.cronometro_label = tk.Label(self.root, text="Tiempo: 0 segundos", bg="lightgray", font=("Arial", 12, "bold"))
        self.cronometro_label.pack(pady=10)

        # Botón para volver a intentar (se mostrará solo cuando pierdas)
        self.boton_volver_a_intentar = tk.Button(self.root, text="Volver a Intentar", command=self.reiniciar_juego, bg="red", fg="white", font=("Arial", 12, "bold"))
        self.boton_volver_a_intentar.pack(pady=10)
        self.boton_volver_a_intentar.pack_forget()  # Ocultamos el botón inicialmente

        self.juego_activo = True
        self.iniciar_llegada_coches()
        self.actualizar_cronometro()

    def cargar_imagenes_coches(self, directorio_imagenes):
        # Cargar imágenes de coche en diferentes colores
        imagenes = {}
        colores = ["amarillo", "rojo", "verde", "azul", "gris"]
        
        for color in colores:
            ruta_imagen = os.path.join(directorio_imagenes, f"coche_{color}.png")  # Asegúrate de tener imágenes nombradas adecuadamente
            imagen_coche = Image.open(ruta_imagen).resize((200, 100))
            imagenes[color] = ImageTk.PhotoImage(imagen_coche)

        # Imagen por defecto
        imagenes['default'] = ImageTk.PhotoImage(Image.open(os.path.join(directorio_imagenes, "coche_base.png")).resize((200, 100)))

        return imagenes

    def pintar_carro(self):
        color_seleccionado = self.color_seleccionado.get()
        if not color_seleccionado:
            messagebox.showwarning("Selecciona un color", "Por favor, selecciona un color para pintar.")
            return

        resultado = self.juego.pintar_carro(color_seleccionado)
        if resultado is True:
            self.actualizar_imagen_coche(color_seleccionado)  # Cambiar la imagen del coche

            # Acelerar el tiempo entre la llegada de coches
            self.tiempo_espera = max(1, self.tiempo_espera - 0.5)  # Disminuir el tiempo, mínimo 1 segundo

        # Si el color es incorrecto, no hacemos nada ni mostramos mensajes

        self.actualizar_cola()
        self.carros_pintados_label.config(text=f"Coches pintados: {self.juego.carros_pintados}")

    def actualizar_imagen_coche(self, color):
        # Actualizar la imagen del coche según el color pintado
        if color in self.imagenes_coche:
            self.imagen_label.config(image=self.imagenes_coche[color])
        else:
            self.imagen_label.config(image=self.imagenes_coche['default'])

    def iniciar_llegada_coches(self):
        def llegada():
            while self.juego_activo:
                resultado = self.juego.agregar_carro()
                if resultado == "perder":
                    self.juego_activo = False
                    messagebox.showerror("¡Perdiste!", "Demasiados coches en la cola. Juego terminado.")
                    self.mostrar_boton_volver_a_intentar()  # Mostrar el botón para volver a intentar
                    break
                self.actualizar_cola()
                time.sleep(self.tiempo_espera)  # Utilizar el tiempo de espera dinámico que se reduce
        threading.Thread(target=llegada).start()

    def actualizar_cola(self):
        # Limpiar la lista actual de la interfaz
        for widget in self.cola_frame.winfo_children():
            widget.destroy()

        # Mostrar los coches en cola
        for i, carro in enumerate(self.juego.cola):
            tk.Label(self.cola_frame, text=f"Coche {i+1}: {carro.color_requerido}", bg="lightgray", font=("Arial", 10, "bold")).pack(pady=5)

    def actualizar_cronometro(self):
        def cronometro():
            while self.juego_activo:
                self.tiempo_transcurrido += 1
                self.cronometro_label.config(text=f"Tiempo: {self.tiempo_transcurrido} segundos")
                time.sleep(1)
        threading.Thread(target=cronometro).start()

    def mostrar_boton_volver_a_intentar(self):
        # Mostrar el botón de "Volver a intentar"
        self.boton_volver_a_intentar.pack()

    def reiniciar_juego(self):
        # Reiniciar el estado del juego
        self.juego = JuegoPintarCoches()
        self.tiempo_espera = 5
        self.tiempo_transcurrido = 0
        self.carros_pintados_label.config(text="Coches pintados: 0")
        self.cronometro_label.config(text="Tiempo: 0 segundos")
        self.boton_volver_a_intentar.pack_forget()  # Ocultar el botón al reiniciar
        self.juego_activo = True
        self.iniciar_llegada_coches()
        self.actualizar_cronometro()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazPintarCoches(root)
    root.mainloop()
