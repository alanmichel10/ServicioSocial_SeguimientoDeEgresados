from flask_login import UserMixin

class Estudios(UserMixin):
        def __init__(self,Correo_A,centroUniversitario,carrera,cicloEgreso,nivelIngles,titulado,promedio) -> None:
            self.correo=Correo_A
            self.centro= centroUniversitario
            self.carrera= carrera
            self.ciclo= cicloEgreso
            self.ingles= nivelIngles
            self.titulado= titulado
            self.promedio= promedio
       