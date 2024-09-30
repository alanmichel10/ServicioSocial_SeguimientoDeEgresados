import random
import string


def generar_contrasena(longitud=10):
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(random.choice(caracteres) for i in range(longitud))
    return contrasena