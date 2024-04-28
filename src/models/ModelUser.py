from .entities.User import User
from werkzeug.security import check_password_hash, generate_password_hash

class ModelUser():
    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql="""SELECT idCuenta, correo, clave, nombre FROM cuenta
                   WHERE correo='{}'""".format(user.correo)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.clave), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idCuenta, correo, nombre,apellidoP,apellidoM,idRol FROM cuenta WHERE idCuenta = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2],row[3],row[4],row[5])
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