from .entities.Estudios import Estudios 

class ModelEstudios():
    @classmethod
    def nuevoEstudios(self, db, estudios,id):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO estudios (centroUniversitario,carrera,cicloEgreso,nivelIngles,titulado,promedio) 
                     VALUES (%s,%s,%s,%s,%s)"""
            values = (
                    estudios.centroUniversitario, estudios.carrera, estudios.cicloEgreso,
                    estudios.nivelIngles, estudios.titulado, estudios.promedio
                )

            cursor.execute(sql, values)
            resultado = cursor.rowcount
            idEstudios = cursor.lastrowid

            sqlGeneral = """UPDATE general 
                        SET estudios=%s
                        WHERE cuenta=%s"""
            valuesGeneral=(idEstudios,id)
            cursor.execute(sqlGeneral, valuesGeneral)
            db.connection.commit()
            
            
            return resultado
        except Exception as ex:
            raise Exception(ex)

    
    @classmethod
    def get_by_id(cls, db, correo_user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT Correo_A,centroUniversitario,carrera,cicloEgreso,nivelIngles,titulado,promedio FROM estudios WHERE Correo_A = '{}'".format(correo_user)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row:
                return Estudios(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            else:
                return Estudios()
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def validarEstudio(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT Correo_Alumno FROM general WHERE Correo_Alumno = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            idEstudios = row[0]
        
            if idEstudios ==None:
                idEstudios=0
                return idEstudios
            if row:
                
                sqlEstudios = "SELECT Correo_A FROM estudios WHERE Correo_A = {}".format(row[0])
                cursor.execute(sqlEstudios)
                estudios= cursor.fetchone()
                print(estudios)
                if estudios:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def actualizarEstudios(self, db, estudios, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT Correo_Alumno FROM general WHERE Correo_Alumno = {}".format(id)
            cursor.execute(sql)
            idEstudios = cursor.fetchone()
            idEstudios = idEstudios[0]
            if idEstudios:
                sql = """UPDATE estudios 
                        SET centroUniversitario = %s, carrera= %s, cicloEgreso=%s, nivelIngles=%s, titulado=%s, promedio=%s
                        WHERE Correo_A=%s"""
                values = (
                    estudios.centro , estudios.carrera, estudios.ciclo, estudios.ingles, estudios.titulado, idEstudios
                    )
          
                cursor.execute(sql, values)
                db.connection.commit()
            
                resultado = cursor.rowcount
                return resultado
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
