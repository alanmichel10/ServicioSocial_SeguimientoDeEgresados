from flask_login import UserMixin

class Estudios(UserMixin):
        def __init__(self,idEstudios,centroUniversitario,carrera,cicloEscolar,nivelIngles,titulado) -> None:
            self.id=idEstudios
            self.centro= centroUniversitario
            self.carrera= carrera
            self.ciclo= cicloEscolar
            self.ingles= nivelIngles
            self.titulado= titulado
       