from .entities.Admin import Alumno
from .entities.Trabajo import Trabajo
from .entities.Estudios import Estudios
from .entities.General import General
from flask import send_file
import xlsxwriter
import io
from datetime import datetime
import tempfile

class ModelAdmin():
    @classmethod
    def registros(cls,db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT idGeneral,cuenta.nombre,cuenta.apellidoP, cuenta.apellidoM,
            celular, cuenta.correo, estudios.nivelIngles, sexo, posgrado FROM general left join
            cuenta on cuenta = cuenta.idCuenta left join estudios on estudios=estudios.idEstudios """
            cursor.execute(sql)
            rows = cursor.fetchall()
            alumnos = [Alumno(*row) for row in rows if len(row) == 9]
            return alumnos
        except Exception as ex:
            raise Exception(ex)
    @classmethod
    def laboral(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT trabajo FROM general WHERE idGeneral = {}".format(id)
            cursor.execute(sql)
            idTrabajo = cursor.fetchone()
            
            idTrabajo = idTrabajo[0]
            if idTrabajo is None:
                return None

            
            sql2 = "SELECT idTrabajo,estatus,nombre,ubicacion,descripcion,antiguedad,jornadaLaboral FROM trabajo WHERE idTrabajo = {}".format(idTrabajo)
            
            cursor.execute(sql2)
            row = cursor.fetchone()

            if row is not None:
                return Trabajo(row[0], row[1], row[2], row[3], row[4], row[5])
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def estudios(cls, db, id):
        try:
            cursor = db.connection.cursor()

            sql = "SELECT estudios FROM general WHERE idGeneral = {}".format(id)
            cursor.execute(sql)
            idEstudios = cursor.fetchone()
            idEstudios = idEstudios[0]
            if idEstudios is None:
                return None

            
            sql1 = "SELECT idEstudios, centroUniversitario, carrera, cicloEgreso, nivelIngles, titulado FROM estudios WHERE idEstudios = {}".format(idEstudios)
            cursor.execute(sql1)
            row = cursor.fetchone()

            if row is not None:
                return Estudios(row[0], row[1], row[2], row[3], row[4], row[5])
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def general(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idGeneral,sexo,curp,codigoPostal,codigoEstudiante,estadoCivil,fechaNacimiento,lugarNacimiento,celular,posgrado FROM general WHERE idGeneral = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return General(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    @classmethod
    def informacion(cls,db,id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT idGeneral,cuenta.nombre,cuenta.apellidoP, cuenta.apellidoM,
            celular, cuenta.correo, estudios.nivelIngles, sexo, posgrado FROM general left join
            cuenta on cuenta = cuenta.idCuenta left join estudios on estudios=estudios.idEstudios WHERE idGeneral = {}""".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Alumno(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])

            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def descargarRegistros(cls, db):
        registros = cls.registros(db)

        # Crear un libro de trabajo y una hoja de cálculo
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        now = datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")

        encabezados = ['Nombre(s)', 'Apellido paterno', 'Apellido materno', 'Numero de telefono', 'Correo electronico',
                       'Nivel de ingles', 'Genero', 'Posgrado al que aspira']
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
            worksheet.write(fila_num, 7, registro.posgrado)

        workbook.close()
        output.seek(0)
        nombre_archivo = f"registros_{fecha_actual}.xlsx"
        return send_file(output, attachment_filename=nombre_archivo, as_attachment=True)
    @classmethod
    def descargarRegistrosid(cls, db, id):
        trabajo = cls.laboral(db, id)
        estudios = cls.estudios(db, id)
        general = cls.general(db, id)
        informacion = cls.informacion(db, id)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        worksheet_general = workbook.add_worksheet('Datos generales')
        worksheet_estudios = workbook.add_worksheet('Estudios')
        worksheet_laboral = workbook.add_worksheet('Informacion laboral')

        headers_general = ['Nombre(s)', 'Apellido paterno', 'Apellido materno', 'Correo electronico',
                        'Sexo', 'CURP', 'Codigo postal', 'Codigo estudiante',
                        'Estado civil', 'Fecha de nacimiento', 'Lugar de nacimiento',
                        'Numero de Telefono', 'Posgrado al que aspira']

        headers_estudios = ['Centro Universitario / Escuela de prosedencia', 'Carrera(s)',
                            'Ciclo escolar de egreso', 'Nivel de ingles', 'Titulado']

        headers_laboral = ['Tenia o tiene un empleo formal?', 'Nombre de la empresa',
                            'Ubicacion de la empresa', 'Descripción de las Responsabilidades Laborales',
                            'Cuánto tiempo tenía laborando en la institución u organización',
                            'Cuántas horas trabaja?']

        for col_num, header in enumerate(headers_general):
            worksheet_general.write(0, col_num, header)

        # Verificar si hay datos en la sección 'Datos generales' antes de escribir
        if informacion and general:
            data_general = [informacion.nombre, informacion.apellidoP or '', informacion.apellidoM or '',
                            informacion.correoElectronico or '', informacion.sexo or '', general.curp or '',
                            general.codigoPostal or '', general.codigoEstudiante or '', general.estadoCivil or '',
                            general.fecha or '', general.lugarNacimiento or '', general.numeroTelefono or '',
                            informacion.posgrado or '']

            for col_num, value in enumerate(data_general):
                worksheet_general.write(1, col_num, value)

        # Verificar si hay datos en la sección 'Estudios' antes de escribir
        if estudios:
            for col_num, header in enumerate(headers_estudios):
                worksheet_estudios.write(0, col_num, header)

            data_estudios = [estudios.centro or '', estudios.carrera or '', estudios.ciclo or '',
                            estudios.ingles or '', estudios.titulado or '']

            for col_num, value in enumerate(data_estudios):
                worksheet_estudios.write(1, col_num, value)

        # Verificar si hay datos en la sección 'Informacion laboral' antes de escribir
        if trabajo:
            for col_num, header in enumerate(headers_laboral):
                worksheet_laboral.write(0, col_num, header)

            data_laboral = [trabajo.estatus or '', trabajo.nombre or '', trabajo.ubicacion or '',
                            trabajo.descripcion or '', trabajo.antiguedad or '', trabajo.jornada or '']

            for col_num, value in enumerate(data_laboral):
                worksheet_laboral.write(1, col_num, value)

        workbook.close()

        return output.getvalue()

    @classmethod
    def cuentaTitulados(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT titulado FROM estudios WHERE titulado='Si'"""
            cursor.execute(sql)
            rows = cursor.fetchall()

            cantidad = len(rows)

            return cantidad
        except Exception as ex:
            raise Exception(ex)
    