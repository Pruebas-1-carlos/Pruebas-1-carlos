"""
===========================================================
SISTEMA SOFTWARE FJ
Gestión de Clientes, Servicios y Reservas
===========================================================

✔ Programación Orientada a Objetos
✔ Abstracción
✔ Herencia
✔ Polimorfismo
✔ Encapsulación
✔ Manejo avanzado de excepciones
✔ Registro de logs en archivo
✔ Simulación de operaciones válidas e inválidas

NOTA: No se usa base de datos, solo listas y archivos.
"""
#correccion de codigo segundo commit
# =========================
# IMPORTACIONES NECESARIAS
# =========================
from abc import ABC, abstractmethod


# =========================
# SISTEMA DE LOGS
# =========================
def registrar_log(mensaje):
    """
    Guarda errores o eventos en un archivo de texto.
    Esto permite mantener el sistema funcionando sin detenerse.
    """
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(mensaje + "\n")


# =========================
# EXCEPCIONES PERSONALIZADAS
# =========================
class ErrorSistema(Exception):
    """Clase base de errores del sistema"""
    pass


class ErrorValidacion(ErrorSistema):
    """Errores en datos ingresados"""
    pass


class ErrorReserva(ErrorSistema):
    """Errores en el proceso de reservas"""
    pass


class ServicioNoDisponible(ErrorSistema):
    """Error cuando un servicio falla"""
    pass


# =========================
# CLASE CLIENTE (ENCAPSULACIÓN)
# =========================
class Cliente:
    """
    Representa un cliente del sistema
    Se aplican validaciones y encapsulación
    """

    def __init__(self, nombre, correo):
        # Validación de datos
        if not nombre:
            raise ErrorValidacion("El nombre no puede estar vacío")

        if "@" not in correo:
            raise ErrorValidacion("Correo inválido")

        # Atributos privados
        self.__nombre = nombre
        self.__correo = correo

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} - {self.__correo}"


# =========================
# CLASE ABSTRACTA SERVICIO
# =========================
class Servicio(ABC):
    """
    Clase abstracta base para todos los servicios
    Aquí aplicamos ABSTRACCIÓN
    """

    def __init__(self, nombre, precio_base):
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, tiempo):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# =========================
# CLASES HIJAS (HERENCIA + POLIMORFISMO)
# =========================
class ReservaSala(Servicio):
    """
    Servicio de alquiler de salas
    """

    def calcular_costo(self, horas):
        if horas <= 0:
            raise ErrorValidacion("Horas inválidas")
        return self.precio_base * horas

    def descripcion(self):
        return "Reserva de sala por horas"


class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de equipos
    """

    def calcular_costo(self, dias):
        if dias <= 0:
            raise ErrorValidacion("Días inválidos")
        return self.precio_base * dias

    def descripcion(self):
        return "Alquiler de equipos tecnológicos"


class Asesoria(Servicio):
    """
    Servicio de asesoría especializada
    """

    def calcular_costo(self, horas):
        if horas <= 0:
            raise ErrorValidacion("Horas inválidas")
        return (self.precio_base * horas) * 1.2  # recargo

    def descripcion(self):
        return "Asesoría especializada"


# =========================
# CLASE RESERVA
# =========================
class Reserva:
    """
    Integra cliente + servicio + duración
    Maneja estados y control de errores
    """

    def __init__(self, cliente, servicio, duracion):

        # Validación de duración
        if duracion <= 0:
            raise ErrorReserva("Duración inválida")

        if cliente is None:
            raise ErrorReserva("Cliente no válido")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def procesar(self):
        """
        Procesa la reserva con manejo robusto de errores
        """

        try:
            # Se intenta calcular el costo
            costo = self.servicio.calcular_costo(self.duracion)

        except ErrorValidacion as e:
            # Error específico
            self.estado = "Error"
            raise ErrorReserva("Error de validación en servicio") from e

        except Exception as e:
            # Error general
            self.estado = "Error"
            raise ErrorReserva("Error inesperado") from e

        else:
            # Si todo sale bien
            self.confirmar()
            return costo

        finally:
            # Siempre se ejecuta (útil para auditoría)
            registrar_log(f"Reserva procesada con estado: {self.estado}")


# =========================
# FUNCIÓN PRINCIPAL
# =========================
def ejecutar_simulacion():
    """
    Simula al menos 10 operaciones
    incluyendo errores y casos válidos
    """

    print("===== INICIO SIMULACIÓN =====")

    # Lista para almacenar clientes
    clientes = []

    # =========================
    # 1. Cliente válido
    # =========================
    try:
        c1 = Cliente("Carlos", "carlos@email.com")
        clientes.append(c1)
    except Exception as e:
        registrar_log(f"Error cliente 1: {e}")

    # =========================
    # 2. Cliente inválido
    # =========================
    try:
        c2 = Cliente("", "correo")
        clientes.append(c2)
    except Exception as e:
        registrar_log(f"Error cliente 2: {e}")

    # =========================
    # 3. Crear servicios
    # =========================
    sala = ReservaSala("Sala VIP", 100)
    equipo = AlquilerEquipo("Laptop", 50)
    asesoria = Asesoria("Consultoría", 200)

    # =========================
    # 4. Reserva válida
    # =========================
    try:
        r1 = Reserva(c1, sala, 2)
        print("Costo reserva sala:", r1.procesar())
    except Exception as e:
        registrar_log(f"Error reserva 1: {e}")

    # =========================
    # 5. Duración inválida
    # =========================
    try:
        r2 = Reserva(c1, sala, -1)
    except Exception as e:
        registrar_log(f"Error reserva 2: {e}")

    # =========================
    # 6. Error en servicio
    # =========================
    try:
        r3 = Reserva(c1, equipo, -5)
        r3.procesar()
    except Exception as e:
        registrar_log(f"Error reserva 3: {e}")

    # =========================
    # 7. Asesoría válida
    # =========================
    try:
        r4 = Reserva(c1, asesoria, 3)
        print("Costo asesoría:", r4.procesar())
    except Exception as e:
        registrar_log(f"Error reserva 4: {e}")

    # =========================
    # 8. Cliente inexistente
    # =========================
    try:
        r5 = Reserva(None, sala, 2)
        r5.procesar()
    except Exception as e:
        registrar_log(f"Error reserva 5: {e}")

    # =========================
    # 9. Reserva válida equipo
    # =========================
    try:
        r6 = Reserva(c1, equipo, 1)
        print("Costo equipo:", r6.procesar())
    except Exception as e:
        registrar_log(f"Error reserva 6: {e}")

    # =========================
    # 10. Otro caso válido
    # =========================
    try:
        r7 = Reserva(c1, sala, 5)
        print("Costo sala extendida:", r7.procesar())
    except Exception as e:
        registrar_log(f"Error reserva 7: {e}")

    print("===== FIN SIMULACIÓN =====")


# =========================
# EJECUCIÓN DEL PROGRAMA
# =========================
if __name__ == "__main__":
    ejecutar_simulacion()