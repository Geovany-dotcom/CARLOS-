import datetime

class NodoAuto:
    def __init__(self, placas, propietario, hora_entrada):
        self.placas = placas
        self.propietario = propietario
        self.hora_entrada = hora_entrada
        self.siguiente = None
        self.anterior = None

class ColaCircularDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def esta_vacia(self):
        return self.cabeza is None

    def ingresar_auto(self, placas, propietario):
        hora_entrada = datetime.datetime.now()
        nuevo_auto = NodoAuto(placas, propietario, hora_entrada)

        if self.esta_vacia():
            self.cabeza = nuevo_auto
            self.cola = nuevo_auto
            nuevo_auto.siguiente = nuevo_auto
            nuevo_auto.anterior = nuevo_auto
        else:
            nuevo_auto.siguiente = self.cabeza
            nuevo_auto.anterior = self.cola
            self.cola.siguiente = nuevo_auto
            self.cabeza.anterior = nuevo_auto
            self.cola = nuevo_auto
        
        return f"Auto con placas {placas} ingresado exitosamente a las {hora_entrada}."

    def sacar_auto(self):
        if self.esta_vacia():
            return "No hay autos en el estacionamiento."

        auto_salida = self.cabeza
        hora_salida = datetime.datetime.now()
        duracion = (hora_salida - auto_salida.hora_entrada).total_seconds()
        costo = duracion * 2  # $2.00 por segundo

        if self.cabeza == self.cola:  # Solo hay un auto en la cola
            self.cabeza = None
            self.cola = None
        else:
            self.cabeza = self.cabeza.siguiente
            self.cabeza.anterior = self.cola
            self.cola.siguiente = self.cabeza

        return (f"Auto con placas {auto_salida.placas} del propietario {auto_salida.propietario} "
                f"salió a las {hora_salida}. Costo del estacionamiento: ${costo:.2f}")

# Ejemplo para pruebas:
if __name__ == "__main__":
    estacionamiento = ColaCircularDoble()
    print(estacionamiento.ingresar_auto("ABC123", "Juan Perez"))
    print(estacionamiento.sacar_auto())
