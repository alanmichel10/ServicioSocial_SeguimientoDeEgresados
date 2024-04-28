from .entities.Trabajo import Trabajo 

class ModelTrabajo():
    @classmethod
    def nuevoTrabajo(self, db, trabajo,id):
        try:
            cursor = db.connection.cursor()

            if trabajo.estatus == 'Si':
                sql = """INSERT INTO trabajo (estatus, nombre, ubicacion, descripcion, antiguedad, jornadalaboral) 
                        VALUES (%s, %s, %s, %s, %s, %s)"""
                values = (
                    trabajo.estatus, trabajo.nombre, trabajo.ubicacion, trabajo.descripcion, trabajo.antiguedad, trabajo.jornada
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
    def get_by_id(cls, db, id):
        try:
            cursor = db.connection.cursor()

            sql = "SELECT trabajo FROM general WHERE cuenta = {}".format(id)
            cursor.execute(sql)
            idTrabajo = cursor.fetchone()
           
            if idTrabajo ==None:
                idTrabajo=0
                return idTrabajo
            if idTrabajo is not None:
                idTrabajo = idTrabajo[0]
                if idTrabajo is not None:
                    sql = "SELECT idTrabajo,estatus,nombre,ubicacion,descripcion,antiguedad,jornadaLaboral FROM trabajo WHERE idTrabajo = {}".format(idTrabajo)
                    cursor.execute(sql)
                    row = cursor.fetchone()

                    if row:
                        return Trabajo(row[0], row[1], row[2], row[3], row[4], row[5],row[6])
                    else:
                        return Trabajo()
                else:
                    return None
            else:
                return Trabajo()
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def validarTrabajo(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT trabajo FROM general WHERE cuenta = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            idTrabajo = row[0]
        
            if idTrabajo ==None:
                idTrabajo=0
                return idTrabajo
            if row:
                
                sqlTrabajo = "SELECT idTrabajo FROM trabajo WHERE idTrabajo = {}".format(row[0])
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
            sql = "SELECT trabajo FROM general WHERE cuenta = {}".format(id)
            cursor.execute(sql)
            idTrabajo = cursor.fetchone()
            idTrabajo = idTrabajo[0]
            if idTrabajo:
                if trabajo.estatus == 'Si':
                    sql = """UPDATE trabajo 
                            SET estatus = %s, nombre= %s, ubicacion=%s, descripcion=%s, antiguedad=%s, jornadaLaboral=%s
                            WHERE idtrabajo=%s"""
                    values = (
                        trabajo.estatus , trabajo.nombre, trabajo.ubicacion, trabajo.descripcion, trabajo.antiguedad, trabajo.jornada, idTrabajo
                        )
                else:
                    sql = """UPDATE trabajo 
                            SET estatus = %s, nombre=NULL, ubicacion=NULL, descripcion=NULL, antiguedad=NULL, jornadaLaboral=NULL
                            WHERE idtrabajo=%s"""
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
