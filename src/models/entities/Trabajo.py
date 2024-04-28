class Trabajo():
        def __init__(self,idTrabajo,estatus,nombre=None, ubicacion=None, descripcion=None, antiguedad=None, jornadaLaboral=None) -> None:
            self.id=idTrabajo
            self.estatus= estatus
            self.nombre= nombre
            self.ubicacion= ubicacion
            self.descripcion= descripcion
            self.antiguedad = antiguedad
            self.jornada = jornadaLaboral
       