from flask_login import UserMixin

class General(UserMixin):
        def __init__(self,idCuenta,sexo,curp,codigoEstudiante,fechaNacimiento,lugarNacimiento,telefono,posgrado) -> None:
            self.id=idCuenta
            self.sexo= sexo
            self.curp= curp
            self.codigoEstudiante= codigoEstudiante
            self.fecha= fechaNacimiento
            self.lugarNacimiento= lugarNacimiento
            self.numeroTelefono= telefono
            self.posgrado= posgrado