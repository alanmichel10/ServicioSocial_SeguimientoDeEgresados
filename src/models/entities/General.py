from flask_login import UserMixin

class General(UserMixin):
        def __init__(self,idCuenta,sexo,curp,cp,codigoEstudiante,estadoCivil,fechaNacimiento,lugarNacimiento,telefono,posgrado) -> None:
            self.id=idCuenta
            self.sexo= sexo
            self.curp= curp
            self.codigoPostal= cp
            self.codigoEstudiante= codigoEstudiante
            self.estadoCivil= estadoCivil
            self.fecha= fechaNacimiento
            self.lugarNacimiento= lugarNacimiento
            self.numeroTelefono= telefono
            self.posgrado= posgrado