from .entities.User import User
from werkzeug.security import check_password_hash, generate_password_hash
import hashlib

class ModelUser():
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT idCuenta, correo, clave FROM cuenta
                     WHERE correo = %s"""
            cursor.execute(sql, (user.correo,))
            row = cursor.fetchone()
            if row != None:
                stored_password = row[2]
                # Hashea la contraseña ingresada
                return User(row[0], row[1], None)
                
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idCuenta, correo, idRol FROM cuenta WHERE idCuenta = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def nuevoUsuario(self,db,user): 
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO cuenta (correo, clave, nombre, apellidoP, apellidoM,idRol) 
                    VALUES (%s,%s,%s,%s,%s,%s)"""
            hashedClave=generate_password_hash(user.clave)
            values=(user.correo,hashedClave,user.nombre,user.apellidoP,user.apellidoM,2)
            cursor.execute(sql,values)
            db.connection.commit() 
            resultado=cursor.rowcount
            return resultado
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def validarUsuario(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql="""SELECT idCuenta, correo, clave, nombre FROM cuenta
                   WHERE correo='{}'""".format(user.correo)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row!= None:
                return False
            else:
                return True
        except Exception as ex:
            raise Exception(ex)
        
    

    @classmethod
    def actualizarUsuario(self,db,user): 
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE cuenta SET nombre=%s, apellidoP= %s, apellidoM= %s 
                     WHERE idCuenta = %s"""
            values=(user.nombre,user.apellidoP,user.apellidoM,user.id)
            cursor.execute(sql,values)
            db.connection.commit()
            return None
        except Exception as ex:
            raise Exception(ex)