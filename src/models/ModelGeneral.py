from .entities.General import General 

class ModelGeneral():
    @classmethod
    def nuevoGeneral(self, db, general, id):
        try:
            cursor = db.connection.cursor()

            if general.codigoEstudiante:
                sql = """INSERT INTO general (Correo_Alumno,nombre,apellidoP,apellidoM,sexo,celular,codigoPostal,fechaNacimiento,Pais,Estado,Ciudad,Colonia,Nacionalidad) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values = (
                    general.Correo_Alumno, general.nombre, general.apellidoP, general.apellidoM,
                    general.sexo, general.celular, general.codigoPostal,
                    general.fechaNacimiento, general.Pais, general.Estado, general.Ciudad, general.Nacionalidad
                )
            else:
                sql = """INSERT INTO general (Correo_Alumno,nombre,apellidoP,apellidoM,sexo,celular,codigoPostal,fechaNacimiento,Pais,Estado,Ciudad,Colonia,Nacionalidad) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values = (
                    general.Correo_Alumno, general.nombre, general.apellidoP, general.apellidoM,
                    general.sexo, general.celular, general.codigoPostal,
                    general.fechaNacimiento, general.Pais, general.Estado, general.Ciudad, general.Nacionalidad
                )

            cursor.execute(sql, values)
            db.connection.commit()
            
            resultado = cursor.rowcount
            return resultado
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, correo_user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT Correo_Alumno,nombre,apellidoP,apellidoM,sexo,celular,codigoPostal,fechaNacimiento,Pais,Estado,Ciudad,Colonia,Nacionalidad FROM general WHERE Correo_Alumno = '{}'".format(correo_user)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return General(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def validarUsuario(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT Correo_Alumno FROM general WHERE Correo_Alumno = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return False
            else:
                return True
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def actualizarGeneral(self, db, general, id):
        try:
            cursor = db.connection.cursor()

            if general.codigoEstudiante:
                sql = """UPDATE general 
                        SET Correo_Alumno=%s, nombre=%s, apellidoP=%s, apellidoM=%s, sexo=%s, 
                            celular=%s, codigoPostal=%s, celular=%s, fechaNacimiento=%s, Pais=%s,
                            Estado=%s, Ciudad=%s, Nacionalidad=%s
                        WHERE cuenta=%s"""
                values = (
                    general.Correo_Alumno, general.nombre, general.apellidoP, general.apellidoM,
                    general.sexo, general.celular, general.codigoPostal,
                    general.fechaNacimiento, general.Pais, general.Estado, general.Ciudad, general.Nacionalidad
                )
            else:
                sql = """UPDATE general 
                        SET Correo_Alumno=%s, nombre=%s, apellidoP=%s, apellidoM=%s, sexo=%s, 
                            celular=%s, codigoPostal=%s, celular=%s, fechaNacimiento=%s, Pais=%s,
                            Estado=%s, Ciudad=%s, Nacionalidad=%s
                        WHERE cuenta=%s"""
                values = (
                    general.Correo_Alumno, general.nombre, general.apellidoP, general.apellidoM,
                    general.sexo, general.celular, general.codigoPostal,
                    general.fechaNacimiento, general.Pais, general.Estado, general.Ciudad, general.Nacionalidad
                )

            cursor.execute(sql, values)
            db.connection.commit()
            
            resultado = cursor.rowcount
            return resultado
        except Exception as ex:
            raise Exception(ex)
