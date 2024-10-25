import random
from collections import deque

class Carro:
    def __init__(self):
        # El coche requiere uno de estos 5 colores
        self.color_requerido = random.choice(["amarillo", "rojo", "verde", "azul", "gris"])

class JuegoPintarCoches:
    def __init__(self):
        self.cola = deque()  # Cola de coches esperando
        self.carros_pintados = 0  # Contador de coches pintados
        self.cola_maxima = 5  # Límite de coches en la cola

    def agregar_carro(self):
        if len(self.cola) < self.cola_maxima:
            carro = Carro()
            self.cola.append(carro)
        else:
            return "perder"  # Si la cola llega a 5, el jugador pierde

    def pintar_carro(self, color_seleccionado):
        if self.cola:
            carro = self.cola[0]  # Ver el primer coche de la cola, pero no quitarlo aún
            if carro.color_requerido == color_seleccionado:
                self.cola.popleft()  # Solo quitar de la cola si el color es correcto
                self.carros_pintados += 1
                return True  # Pintado correctamente
            else:
                return False  # Color incorrecto, el coche sigue en la cola
        return None  # No hay coches en la cola
