from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, idCuenta, correo, clave, nombre="", apellidoP="", apellidoM="",idRol='') -> None:
        self.id = idCuenta
        self.correo = correo
        self.clave = clave
        self.nombre = nombre
        self.apellidoP = apellidoP
        self.apellidoM = apellidoM
        self.rol=idRol
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
#print(generate_password_hash('facil'))