# Ejemplo de herencia y polimorfismo
class Animal:
    def hablar(self):
        pass

class Perro(Animal):
    # CARLOS: Agregué este comentario para explicar que aquí 
    # se aplica polimorfismo al sobrescribir el método.
    def hablar(self):
        return "Guau!"