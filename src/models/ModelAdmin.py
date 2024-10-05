from .entities.Admin import Alumno
from .entities.Trabajo import Trabajo
from .entities.Estudios import Estudios
from .entities.General import General
from flask import send_file
import xlsxwriter
import io

from datetime import datetime
import tempfile
import logging


class ModelAdmin():
    
    @classmethod
    def getCarrerasCoordinador(self, db, coordinador_correo):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT cc.idCarrera, c.nombre 
                    FROM coordinador_carrera cc
                    JOIN carrera c ON cc.idCarrera = c.idCarrera
                    WHERE cc.correo = %s"""
            cursor.execute(sql, (coordinador_correo,))
            carreras = cursor.fetchall()
            print(f"Carreras encontradas para {coordinador_correo}: {carreras}")  # Para debugging
            return carreras
        except Exception as ex:
            print(f"Error en getCarrerasCoordinador: {ex}")  # Para debugging
            raise Exception(ex)

    @classmethod
    def getAspirantesCarreras(self, db, carreras):
        try:
            cursor = db.connection.cursor()
            carrera_ids = [carrera[0] for carrera in carreras]
            
            if not carrera_ids:
                # Si no hay carreras, devolver una lista vacía
                return []
            
            placeholders = ','.join(['%s' for _ in carrera_ids])
            sql = f"""
                SELECT 
                    g.nombre, 
                    g.apellidoP, 
                    g.apellidoM, 
                    g.celular, 
                    g.Correo_Alumno, 
                    e.nivelIngles, 
                    g.sexo, 
                    e.titulado
                FROM 
                    general g
                INNER JOIN 
                    estudios e ON g.Correo_Alumno = e.Correo_A
                INNER JOIN 
                    aspirante_carrera ac ON g.Correo_Alumno = ac.Correo_Alumno
                WHERE 
                    ac.idCarrera IN ({placeholders})
            """
            cursor.execute(sql, carrera_ids)
            aspirantes = cursor.fetchall()
            return aspirantes
        except Exception as ex:
            print(f"Error en getAspirantesCarreras: {ex}")  # Para debugging
            raise Exception(ex)

    @classmethod
    def registros(cls, db, id_carrera):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT g.Correo_Alumno, g.nombre, g.apellidoP, g.apellidoM,
                     g.celular, g.Correo_Alumno, e.nivelIngles, g.sexo, e.carrera, e.titulado
                     FROM general g
                     LEFT JOIN estudios e ON g.Correo_Alumno = e.Correo_A
                     JOIN aspirante_carrera ac ON g.Correo_Alumno = ac.Correo_Alumno
                     WHERE ac.idCarrera = %s"""
            cursor.execute(sql, (id_carrera,))
            rows = cursor.fetchall()
            alumnos = [Alumno(*row) for row in rows if len(row) == 10]
            return alumnos
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def cuentaTitulados(cls, db, id_carrera):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT COUNT(*) FROM estudios e
                     JOIN aspirante_carrera ac ON e.Correo_A = ac.Correo_Alumno
                     WHERE ac.idCarrera = %s AND e.titulado='Si'"""
            cursor.execute(sql, (id_carrera,))
            count = cursor.fetchone()[0]
            return count
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def laboral(cls, db, correo):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT estatus, nombre, Horario_Laboral, Puesto_Trabajo, Sector
                     FROM laboral WHERE Correo_Alu = %s"""
            cursor.execute(sql, (correo,))
            row = cursor.fetchone()

            if row is not None:
                return Trabajo(correo, row[0], row[1], row[2], row[3], row[4])
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def estudios(cls, db, correo):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT centroUniversitario, carrera, cicloEgreso, nivelIngles, titulado
                     FROM estudios WHERE Correo_A = %s"""
            cursor.execute(sql, (correo,))
            row = cursor.fetchone()

            if row is not None:
                return Estudios(correo, row[0], row[1], row[2], row[3], row[4])
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def general(self, db, correo):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT Correo_Alumno, sexo, codigoPostal, fechaNacimiento, celular, Pais, Estado, Ciudad
                     FROM general WHERE Correo_Alumno = %s"""
            cursor.execute(sql, (correo,))
            row = cursor.fetchone()
            if row != None:
                return General(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def informacion(cls, db, correo):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT general.Correo_Alumno, general.nombre, general.apellidoP, general.apellidoM,
            general.celular, general.Correo_Alumno, estudios.nivelIngles, general.sexo, estudios.carrera
            FROM general LEFT JOIN estudios ON general.Correo_Alumno = estudios.Correo_A
            WHERE general.Correo_Alumno = %s"""
            cursor.execute(sql, (correo,))
            row = cursor.fetchone()
            if row != None:
                return Alumno(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def descargarRegistros(cls, db, id_carrera):
        registros = cls.registros(db, id_carrera)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        now = datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")

        encabezados = ['Nombre(s)', 'Apellido paterno', 'Apellido materno', 'Numero de telefono', 'Correo electronico',
                       'Nivel de ingles', 'Genero', 'Carrera', 'Titulado']
        for col_num, encabezado in enumerate(encabezados):
            worksheet.write(0, col_num, encabezado)

        for fila_num, registro in enumerate(registros, start=1):
            worksheet.write(fila_num, 0, registro.nombre)
            worksheet.write(fila_num, 1, registro.apellidoP)
            worksheet.write(fila_num, 2, registro.apellidoM)
            worksheet.write(fila_num, 3, registro.telefono)
            worksheet.write(fila_num, 4, registro.correoElectronico)
            worksheet.write(fila_num, 5, registro.ingles)
            worksheet.write(fila_num, 6, registro.sexo)
            worksheet.write(fila_num, 7, registro.carrera)
            worksheet.write(fila_num, 8, registro.titulado)

        workbook.close()
        output.seek(0)
        nombre_archivo = f"registros_{fecha_actual}.xlsx"
        return send_file(output, attachment_filename=nombre_archivo, as_attachment=True)

  

    @classmethod
    def descargarRegistrosid(cls, db, correo):
        trabajo = cls.laboral(db, correo)
        estudios = cls.estudios(db, correo)
        general = cls.general(db, correo)
        informacion = cls.informacion(db, correo)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        worksheet_general = workbook.add_worksheet('Datos generales')
        worksheet_estudios = workbook.add_worksheet('Estudios')
        worksheet_laboral = workbook.add_worksheet('Informacion laboral')

        headers_general = ['Nombre(s)', 'Apellido paterno', 'Apellido materno', 'Correo electronico',
                        'Sexo', 'Codigo postal', 'Fecha de nacimiento',
                        'Numero de Telefono', 'País', 'Estado', 'Ciudad']

        headers_estudios = ['Centro Universitario / Escuela de prosedencia', 'Carrera(s)',
                            'Ciclo escolar de egreso', 'Nivel de ingles', 'Titulado']

        headers_laboral = ['Estatus', 'Nombre de la empresa',
                            'Horario Laboral', 'Puesto de Trabajo', 'Sector']

        for col_num, header in enumerate(headers_general):
            worksheet_general.write(0, col_num, header)

        if informacion and general:
            data_general = [informacion.nombre, informacion.apellidoP or '', informacion.apellidoM or '',
                            informacion.correoElectronico or '', informacion.sexo or '',
                            general.codigoPostal or '', general.fechaNacimiento or '', general.celular or '',
                            general.pais or '', general.estado or '', general.ciudad or '']

            for col_num, value in enumerate(data_general):
                worksheet_general.write(1, col_num, value)

        if estudios:
            for col_num, header in enumerate(headers_estudios):
                worksheet_estudios.write(0, col_num, header)

            data_estudios = [estudios.centroUniversitario or '', estudios.carrera or '', estudios.cicloEgreso or '',
                            estudios.nivelIngles or '', estudios.titulado or '']

            for col_num, value in enumerate(data_estudios):
                worksheet_estudios.write(1, col_num, value)

        if trabajo:
            for col_num, header in enumerate(headers_laboral):
                worksheet_laboral.write(0, col_num, header)

            data_laboral = [trabajo.estatus or '', trabajo.nombre or '', trabajo.horarioLaboral or '',
                            trabajo.puestoTrabajo or '', trabajo.sector or '']

            for col_num, value in enumerate(data_laboral):
                worksheet_laboral.write(1, col_num, value)

        workbook.close()

        return output.getvalue()

    @classmethod
    def cuentaTitulados(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT COUNT(*) FROM estudios WHERE titulado='Si'"""
            cursor.execute(sql)
            count = cursor.fetchone()[0]

            return count
        except Exception as ex:
            raise Exception(ex)