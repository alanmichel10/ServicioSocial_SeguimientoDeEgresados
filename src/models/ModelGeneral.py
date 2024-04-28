from .entities.General import General 

class ModelGeneral():
    @classmethod
    def nuevoGeneral(self, db, general, id):
        try:
            cursor = db.connection.cursor()

            if general.codigoEstudiante:
                sql = """INSERT INTO general (sexo, curp, codigoPostal, codigoEstudiante, estadoCivil, fechaNacimiento, lugarNacimiento, celular, posgrado, cuenta) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values = (
                    general.sexo, general.curp, general.codigoPostal, general.codigoEstudiante,
                    general.estadoCivil, general.fecha, general.lugarNacimiento,
                    general.numeroTelefono, general.posgrado, id
                )
            else:
                sql = """INSERT INTO general (sexo, curp, codigoPostal, estadoCivil, fechaNacimiento, lugarNacimiento, celular, posgrado, cuenta) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                values = (
                    general.sexo, general.curp, general.codigoPostal,
                    general.estadoCivil, general.fecha, general.lugarNacimiento,
                    general.numeroTelefono, general.posgrado, id
                )

            cursor.execute(sql, values)
            db.connection.commit()
            
            resultado = cursor.rowcount
            return resultado
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idGeneral,sexo,curp,codigoPostal,codigoEstudiante,estadoCivil,fechaNacimiento,lugarNacimiento,celular,posgrado FROM general WHERE cuenta = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return General(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def validarUsuario(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT cuenta FROM general WHERE cuenta = {}".format(id)
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
                        SET sexo=%s, curp=%s, codigoPostal=%s, codigoEstudiante=%s, estadoCivil=%s, 
                            fechaNacimiento=%s, lugarNacimiento=%s, celular=%s, posgrado=%s
                        WHERE cuenta=%s"""
                values = (
                    general.sexo, general.curp, general.codigoPostal, general.codigoEstudiante,
                    general.estadoCivil, general.fecha, general.lugarNacimiento,
                    general.numeroTelefono, general.posgrado, id
                )
            else:
                sql = """UPDATE general 
                        SET sexo=%s, curp=%s, codigoPostal=%s, estadoCivil=%s, 
                            fechaNacimiento=%s, lugarNacimiento=%s, celular=%s, posgrado=%s
                        WHERE cuenta=%s"""
                values = (
                    general.sexo, general.curp, general.codigoPostal,
                    general.estadoCivil, general.fecha, general.lugarNacimiento,
                    general.numeroTelefono, general.posgrado, id
                )

            cursor.execute(sql, values)
            db.connection.commit()
            
            resultado = cursor.rowcount
            return resultado
        except Exception as ex:
            raise Exception(ex)
