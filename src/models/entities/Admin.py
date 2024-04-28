class Alumno:
    def __init__(self, id, nombre, apellidoP, apellidoM, telefono, correoElectronico, ingles, sexo, posgrado):
        self.id = id
        self.nombre = nombre
        self.apellidoP = apellidoP
        self.apellidoM = apellidoM
        self.telefono = telefono
        self.correoElectronico = correoElectronico
        self.ingles = ingles
        self.sexo = sexo
        self.posgrado = posgrado
    def __str__(self):
        return f"Alumno({self.id},{self.nombre},{self.apellidoP},{self.apellidoM},{self.telefono},{self.correoElectronico},{self.ingles},{self.sexo},{self.posgrado})"