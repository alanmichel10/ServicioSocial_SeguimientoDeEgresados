from .entities.Trabajo import Trabajo 

class ModelTrabajo():
    @classmethod
    def nuevoTrabajo(self, db, trabajo,id):
        try:
            cursor = db.connection.cursor()

            if trabajo.estatus == 'Si':
                sql = """INSERT INTO trabajo (estatus,nombre, Horario_Laboral, Puesto_trabajo, Sector) 
                        VALUES (%s, %s, %s, %s, %s, %s)"""
                values = (
                    trabajo.estatus, trabajo.nombre, trabajo.Horario_Laboral, trabajo.Puesto_trabajo, trabajo.Sector
                )
            else:
                sql = """INSERT INTO trabajo (estatus) 
                        VALUES (%s)"""
                values = (
                    trabajo.estatus,
                )

            cursor.execute(sql, values)
            resultado = cursor.rowcount

            idTrabajo = cursor.lastrowid

            sqlGeneral = """UPDATE general 
                        SET trabajo=%s
                        WHERE cuenta=%s"""
            valuesGeneral = (idTrabajo, id)
            cursor.execute(sqlGeneral, valuesGeneral)

            db.connection.commit()
            
            
            return resultado
        except Exception as ex:
            raise Exception(ex)

    
    @classmethod
    def get_by_id(cls, db, correo_user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT Correo_Alu,estatus,nombre, Horario_Laboral, Puesto_trabajo, Sector FROM laboral WHERE Correo_Alu = '{}'".format(correo_user)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row:
                return Trabajo(row[0], row[1], row[2], row[3], row[4], row[5])
            else:
                return Trabajo()
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def validarTrabajo(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT Correo_Alumno FROM general WHERE Correo_Alumno = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            idTrabajo = row[0]
        
            if idTrabajo ==None:
                idTrabajo=0
                return idTrabajo
            if row:
                
                sqlTrabajo = "SELECT Correo_Alu FROM trabajo WHERE Correo_Alu = {}".format(row[0])
                cursor.execute(sqlTrabajo)
                trabajo= cursor.fetchone()
                print(trabajo)
                if trabajo:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def actualizarTrabajo(self, db, trabajo, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT Correo_Alumno FROM general WHERE Correo_Alumno = {}".format(id)
            cursor.execute(sql)
            idTrabajo = cursor.fetchone()
            idTrabajo = idTrabajo[0]
            if idTrabajo:
                if trabajo.estatus == 'Si':
                    sql = """UPDATE trabajo 
                            SET estatus = %s, nombre= %s, Horario_Laboral=%s, Puesto_trabajo=%s, Sector=%s
                            WHERE Correo_Alu=%s"""
                    values = (
                        trabajo.estatus, trabajo.nombre, trabajo.Horario_Laboral, trabajo.Puesto_trabajo, trabajo.Sector, idTrabajo
                        )
                else:
                    sql = """UPDATE trabajo 
                            SET estatus = %s, nombre=NULL, Horario_Laboral=NULL, Puesto_trabajo=NULL, Sector=NULL
                            WHERE Correo_Alu=%s"""
                    values = (
                        trabajo.estatus , idTrabajo
                        )
                cursor.execute(sql, values)
                db.connection.commit()
            
                resultado = cursor.rowcount
                return resultado
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
