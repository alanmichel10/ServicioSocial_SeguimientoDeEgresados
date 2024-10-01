from flask_login import UserMixin

class General(UserMixin):
        def __init__(self,Correo_Alumno,nombre,apellidoP,apellidoM,sexo,celular,codigoPostal,fechaNacimiento,Pais,Estado,Ciudad,Colonia,Nacionalidad) -> None:
            self.correo=Correo_Alumno
            self.nombre= nombre
            self.apellidoP = apellidoP
            self.apellidoM = apellidoM
            self.sexo= sexo
            self.numeroTelefono= celular
            self.codigoPostal= codigoPostal
            self.fecha= fechaNacimiento
            self.pais= Pais
            self.estado= Estado
            self.ciudad= Ciudad
            self.colonia= Colonia
            self.nacionalidad= Nacionalidad