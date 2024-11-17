from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session, flash
from flask_mysqldb import MySQL

from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from flask_login import LoginManager, logout_user, login_user, login_required, current_user
from config import config
import tempfile
import hashlib
import re

# Modulos
from models.ModelUser import ModelUser
from models.ModelGeneral import ModelGeneral
from models.ModelEstudios import ModelEstudios
from models.ModelTrabajo import ModelTrabajo
from models.ModelAdmin import ModelAdmin

# Modulos Formulario
from models.ModelFGeneral import  insertGeneral
from models.ModelFEstudios import insertEstudios
from models.ModelFLaboral import insertLaboral
from models.ModelCorreo import enviar_correo

# Entities
from models.entities.User import User
from models.entities.General import General
from models.entities.Estudios import Estudios
from models.entities.Trabajo import Trabajo


def get_var():
    correo = request.form.get('correo')
    return correo

def set_var(x):
     global correo
     correo = x

app = Flask(__name__)

csrf = CSRFProtect()

db = MySQL(app)


login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

def role_required(required_role):
    def decorator(func):
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.rol == required_role:
                return func(*args, **kwargs)
            else:
                return redirect(url_for('inicio'))
        return wrapper
    return decorator

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
     return render_template('index.html')
#---------------------- -----------------------#Formulario--------------------------------------------#


# Página de Selección
@app.route('/seleccion', methods=['GET', 'POST'])
def fseleccion():
    if request.method == 'POST':
        tipo_posgrado = request.form.get('posgradoInput')
        selecciones = request.form.getlist('seleccionesPosgrado')

        # Validación en el backend
        if not tipo_posgrado:
            flash('Debes seleccionar un tipo de posgrado', 'error')
            return render_template('formulario/seleccion.html')
        
        if not selecciones:
            flash('Debes seleccionar al menos una opción de posgrado', 'error')
            return render_template('formulario/seleccion.html')

        # Guardamos el tipo de posgrado y las selecciones en la sesión
        session['tipo_posgrado'] = tipo_posgrado
        session['carreras_interes'] = selecciones
        return redirect(url_for('fgeneral'))

    return render_template('formulario/seleccion.html')

# Página de Datos Generales
@app.route('/general', methods=['GET', 'POST'])
def fgeneral():
    if request.method == 'GET':
        return render_template('formulario/Generales.html')

    try:
        # Obtener los datos del formulario
        nombre_gen = request.form.get('nombres', '').strip()
        apellido_p = request.form.get('apellido_p', '').strip()
        apellido_m = request.form.get('apellido_m', '').strip()
        sexo = request.form.get('sexo', '')
        telefono = request.form.get('tel_contacto', '').strip()
        correo = request.form.get('correo_alumno', '').strip()
        c_postal = request.form.get('codigo_postal', '').strip()
        pais = request.form.get('pais', '').strip()
        estado = request.form.get('estado', '')
        ciudad = request.form.get('ciudad', '').strip()
        colonia = request.form.get('colonia', '').strip()
        nacionalidad = request.form.get('nacionalidad', '').strip()
        f_nacimiento = request.form.get('f_nacimiento', '')

        # Validaciones del backend
        errores = []

        # Validar campos de texto
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', nombre_gen):
            errores.append('El nombre solo debe contener letras')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', apellido_p):
            errores.append('El apellido paterno solo debe contener letras')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$', apellido_m):
            errores.append('El apellido materno solo debe contener letras')

        # Validar teléfono
        if not re.match(r'^[0-9]{10}$', telefono):
            errores.append('El teléfono debe tener 10 dígitos numéricos')

        # Validar correo
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', correo):
            errores.append('El correo electrónico no es válido')

        # Validar código postal
        if not re.match(r'^[0-9]{5}$', c_postal):
            errores.append('El código postal debe tener 5 dígitos numéricos')

        # Validar fecha de nacimiento
        try:
            fecha_nac = datetime.strptime(f_nacimiento, '%Y-%m-%d')
            hoy = datetime.now()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

            if fecha_nac > hoy:
                errores.append('La fecha de nacimiento no puede ser futura')
            elif edad < 18:
                errores.append('Debes ser mayor de 18 años')
        except ValueError:
            errores.append('Fecha de nacimiento inválida')

        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('formulario/Generales.html')

        # Obtener datos de la sesión
        carreras_interes = session.get('carreras_interes', [])
        tipo_posgrado = session.get('tipo_posgrado', '')

        try:
            # Intentar insertar los datos
            insertGeneral(nombre_gen, apellido_p, apellido_m, sexo, telefono, correo,
                          c_postal, pais, estado, ciudad, colonia, nacionalidad,
                          f_nacimiento, carreras_interes, tipo_posgrado)

            # Si llegamos aquí, la inserción fue exitosa
            session['correo'] = correo
            return redirect(url_for('festudios'))

        except ValueError as e:
            # Error específico para correo duplicado
            flash(str(e), 'error')
            return render_template('formulario/Generales.html')

    except Exception as e:
        # Cualquier otro error no manejado
        flash('Ocurrió un error al procesar tu registro. Por favor, intenta de nuevo.', 'error')
        print(f"Error inesperado: {str(e)}")  # Para debugging
        return render_template('formulario/Generales.html')

    
# Página de Datos de Estudios
@app.route('/estudios', methods=['GET', 'POST'])
def festudios():
    if request.method == 'POST':
        uni_proce = request.form['nivel']
        carrera = request.form['carrera']
        titulado = request.form['titulado']
        ciclo = request.form['ciclo']
        ingles = request.form['ingles']
        promedio = request.form['promedio']
        insertEstudios(uni_proce, carrera, titulado, ciclo, ingles, promedio, session['correo'])
        return redirect(url_for('flaboral'))

    return render_template('formulario/Estudios.html')

# Página de Datos de Laboral
@app.route('/laboral', methods=['GET', 'POST'])
def flaboral():
    if request.method == 'POST':
        siOno = request.form['trabajasiono']
        lugar = request.form['lugardetrabajo']
        horario = request.form['horariolaboral']
        puesto = request.form['puestolaboral']
        sector = request.form['sector']
        correo = session.get('correo')

        if not correo:
            print("Error: Correo no puede ser nulo")
            flash('Error: Correo no puede ser nulo')
            return redirect(url_for('laboral'))

        contrasena, correo_usuario = insertLaboral(siOno, lugar, horario, puesto, sector, correo)

        destinatario = correo_usuario  # Usando el correo registrado
        asunto = "Confirmación de Registro"
        mensaje_base = "Gracias por registrarte. Tu información ha sido recibida con éxito."
        mensaje_extra = """
        
        Bienvenido a nuestra comunidad de egresados.

        Nos complace informarte que tu información ha sido registrada con éxito. Gracias por tu interés en nuestros programas de posgrado.

        Para obtener más información y continuar con el proceso, por favor, inicia sesión con la cuenta y contraseña que se te proporcionaron en este correo. Puedes hacerlo a través del siguiente enlace: LINK DEL LOGIN.

        Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos.

        ¡Que tengas un excelente día!


        """

        enviar_correo(destinatario, asunto, mensaje_base, contrasena, correo_usuario, mensaje_extra)
    
        flash('Registro completo')
        return redirect(url_for('home'))
    
    return render_template('formulario/Laboral.html')


#---------------------- #Login----------------------------------------------------------------------#


@app.route('/login', methods=['GET', 'POST'])
def login():
    current_route = request.path
    if request.method == 'POST':
        user = User(0, request.form['correo'], request.form['clave'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            login_user(logged_user)
            return redirect(url_for('inicio'))
        else:
            flash("Credenciales incorrectas. Por favor, inténtalo de nuevo.", 'danger')
            return render_template('login/login.html', current_route=current_route)
    else:
        return render_template('login/login.html', current_route=current_route)


#---------------------- ----------------------------------------------------------------------#
#Crear cuenta
@app.route('/crearCuenta',methods=['GET','POST'])    
def crearCuenta():
    if request.method == 'POST':
        if not request.form['correo'] or not request.form['clave'] or not request.form['confirmarClave'] or not request.form['nombre'] or not request.form['apellidoP'] or not request.form['apellidoM']:
            flash("Llene todos los campos.")
            return render_template('login/crearCuenta.html')
        elif request.form['clave'] == request.form['confirmarClave']:
            user = User(0, request.form['correo'], request.form['clave'], request.form['nombre'],request.form['apellidoP'], request.form['apellidoM'])
            validarRespuestas= ModelUser.validarUsuario(db,user)
            if validarRespuestas is True:
                registro=ModelUser.nuevoUsuario(db,user)
                if registro != None:
                    flash("Registrado con exito")
                    return redirect(url_for('login'))
                else:
                    flash("Error al registrarse")
                    return render_template('login/crearCuenta.html')
            else:
                flash("El correo ya esta registrado")
                return render_template('login/crearCuenta.html')

        else:
            flash("Las contraseñas no coinciden")
            return render_template('login/crearCuenta.html')
    else:
        return render_template('login/crearCuenta.html')

##------------------------                                                         ------------------------------------##
#Actualizar datos
@app.route('/ajustes',methods=['GET','POST'])    
def ajustes():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['apellidoP'] or not request.form['apellidoM']:
            flash("Llene todos los campos.")
            return render_template('panelPrincipal/inicio.html', inicio_active="link-secondary")       
        else:   
            id = current_user.id
            user= ModelUser.get_by_id(db,id)
            print(user.nombre)
            user.nombre = request.form['nombre']
            user.apellidoP  = request.form['apellidoP']
            user.apellidoM = request.form['apellidoM']
            ModelUser.actualizarUsuario(db,user)
            flash("Datos actualizados correctamente")
            
            return redirect(url_for('inicio'))
    else:
        return render_template('panelPrincipal/inicio.html', inicio_active="link-secondary")
##------------------------                                                         ------------------------------------##
#Paginas
#Inicio
@app.route('/inicio')  
@login_required
def inicio():
    if current_user.rol == 1:
        return redirect(url_for('admin'))
    else:
        # Supongamos que ModelGeneral almacena los datos que necesitas para el form
        correo_user = current_user.correo
        general = ModelGeneral.get_by_id(db, correo_user)
        
        return render_template('panelPrincipal/inicio.html', current_user=current_user, form=general)

@app.route('/informacion', methods=['GET', 'POST'])  
@login_required  
def informacion():
    return render_template('panelPrincipal/informacion/general.html', current_user=current_user, informacion_active="active")

@app.route('/informacion/general', methods=['GET', 'POST'])  
@login_required  
def general():
    correo_user = current_user.correo
    general = ModelGeneral.get_by_id(db, correo_user)
    return render_template('panelPrincipal/informacion/general.html', current_user=current_user, form=general)
    
@app.route('/informacion/estudios', methods=['GET', 'POST'])
@login_required
def estudios():
    correo_user = current_user.correo
    estudios = ModelEstudios.get_by_id(db, correo_user)
    return render_template('panelPrincipal/informacion/estudios.html', current_user=current_user, form=estudios)

@app.route('/informacion/laboral', methods=['GET', 'POST'])
@login_required
def laboral():
    correo_user = current_user.correo
    trabajo = ModelTrabajo.get_by_id(db, correo_user)
    return render_template('panelPrincipal/informacion/laboral.html', current_user=current_user, form=trabajo)
        
@app.route('/tablon')
@login_required
def tablon():
    return render_template('panelPrincipal/tablon/tablon.html', current_user=current_user, general_active="active")


#---------------------------                 Dashboard                      -----------------------------------##
#DASHBOARD COORDINADORES
@app.route('/panelAdmin', endpoint='admin')
@login_required
@role_required(1) 
def admin():
    coordinador_correo = current_user.correo
    # Obtenemos las carreras completas (con ID)
    carreras_completas = ModelAdmin.getCarrerasCoordinador(db, coordinador_correo)
    
    # Extraemos solo los nombres de las carreras para el header
    nombres_carreras = [carrera[1] for carrera in carreras_completas]  # Esto dará solo los nombres
    
    aspirantes = ModelAdmin.getAspirantesCarreras(db, carreras_completas)  # Mantenemos la tupla completa para las consultas
    cantidad = ModelAdmin.cuentaTitulados(db)
    
    # Obtener el filtro de la solicitud
    filtro_titulado = request.args.get('filtro_titulado')
    
    # Obtener todos los datos de aspirantes
    datosaspirantes = ModelAdmin.getAllAspirantesData(db, carreras_completas)
    
    # Filtrar los aspirantes según el estado de titulación
    if filtro_titulado == "titulados":
        datosaspirantes = [aspirante for aspirante in datosaspirantes if aspirante[22] == 'Si']
    elif filtro_titulado == "no_titulados":
        datosaspirantes = [aspirante for aspirante in datosaspirantes if aspirante[22] == 'No']
    elif filtro_titulado == "en_proceso":
        datosaspirantes = [aspirante for aspirante in datosaspirantes if aspirante[22] == 'En Proceso']

    return render_template('panelPrincipal/panelAdmin/dashboard/crud.html', 
                           aspirantes=aspirantes, 
                           titulados=cantidad, 
                           carreras=carreras_completas,  # Mantenemos la tupla completa para otras funcionalidades
                           nombre_carrera=nombres_carreras[0],  # Enviamos solo el nombre de la primera carrera para el header
                           datosaspirantes=datosaspirantes)

@app.route('/panelAdmin/vermas/<string:id>')
@login_required
def vermas(id):
    general = ModelAdmin.general(db, id)
    estudios = ModelAdmin.estudios(db, id)
    laboral = ModelAdmin.laboral(db, id)
    carrera_id = ModelAdmin.get_carrera_id(db, id)  # Necesitas implementar esta función
    
    return render_template('panelPrincipal/panelAdmin/dashboard/vermas.html',
                           general=general,
                           estudios=estudios,
                           laboral=laboral,
                           carrera_id=carrera_id)
    
    
    
#---------------------------                                       -----------------------------------##

@app.route('/descargar_excel')
@login_required
def descargar_excel():
    try:
        coordinador_correo = current_user.correo
        carreras = ModelAdmin.getCarrerasCoordinador(db, coordinador_correo)
        
        output = ModelAdmin.descargarRegistros(db, carreras)
        return send_file(
            output,
            as_attachment=True,
            download_name='aspirantes.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        flash(f'Error al descargar el Excel: {str(e)}', 'error')
        return redirect(url_for('admin'))


@app.route('/registros')
def descargar():
    registros = ModelAdmin.descargarRegistros(db)

    return registros
@app.route('/registros/id', methods=['GET'])
def descargar_registros():
    id_param = request.args.get('id')
    
    archivo_data = ModelAdmin.descargarRegistrosid(db, id_param)
    nombre_archivo = f"registros{id_param}.xlsx"
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(archivo_data)

    return send_file(temp_file.name, as_attachment=True, download_name=nombre_archivo)
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
# requerir login
@app.route('/protected')
@login_required
def protected():
    return "<h1>Inicia sesion para acceder al sitio</h1>"
def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404



if __name__ == '__main__':
    app.config.from_object(config['development'])
    
    csrf.init_app(app)
    
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.run()
