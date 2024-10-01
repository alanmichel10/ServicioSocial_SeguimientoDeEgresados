from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_mysqldb import MySQL

from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager, logout_user, login_user, login_required, current_user
from config import config
import tempfile
import hashlib

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

        # Guardamos el tipo de posgrado y las selecciones en la sesión
        session['tipo_posgrado'] = tipo_posgrado
        session['carreras_interes'] = selecciones
        return redirect(url_for('fgeneral'))

    return render_template('formulario/seleccion.html')

# Página de Datos Generales
@app.route('/general', methods=['GET', 'POST'])
def fgeneral():
    if request.method == 'POST':
        nombre_gen = request.form['nombres']
        apellido_p = request.form['apellido_p']
        apellido_m = request.form['apellido_m']
        sexo = request.form['sexo']
        telefono = request.form['tel_contacto']
        correo = request.form['correo_alumno']
        c_postal = request.form['codigo_postal']
        pais = request.form['pais']
        estado = request.form['estado']
        ciudad = request.form['ciudad']
        colonia = request.form['colonia']
        nacionalidad = request.form['nacionalidad']
        f_nacimiento = request.form['f_nacimiento']

        # Obtener las carreras de interés y el tipo de posgrado de la sesión
        carreras_interes = session.get('carreras_interes', [])
        tipo_posgrado = session.get('tipo_posgrado', '')

        # Guardamos el correo en la variable global para usarlo después
        session['correo'] = correo

        insertGeneral(nombre_gen, apellido_p, apellido_m, sexo, telefono, correo, c_postal, pais, estado, ciudad, colonia, nacionalidad, f_nacimiento, carreras_interes, tipo_posgrado)
        return redirect(url_for('festudios'))
    
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
    if request.method == 'POST':
        user = User(0, request.form['correo'], request.form['clave'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            login_user(logged_user)
            return redirect(url_for('inicio'))
        else:
            flash("Credenciales incorrectas. Por favor, inténtalo de nuevo.", 'danger')
            return render_template('login/login.html')
    else:
        return render_template('login/login.html')


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
# @login_required ---------------------------------------------------

def inicio():
    if current_user.rol == 1:
        return redirect(url_for('admin'))
    else:    
        return render_template('panelPrincipal/inicio.html')
#InformacionPersonal
@app.route('/informacion')  
@login_required  
def informacion():
    return render_template('panelPrincipal/informacion/general.html',informacion_active="active")

@app.route('/informacion/general',methods=['GET','POST'])  
@login_required  
def general():
    id = current_user.id
    general = (ModelGeneral.get_by_id(db,id))

    if request.method == 'POST':
        validarUsuario= ModelGeneral.validarUsuario(db,id)
        general = General(0,request.form['sexo'],request.form['curp'],request.form['codigoPostal'],request.form['codigoEstudiante'],request.form['estadoCivil'],request.form['fechaNacimiento'],request.form['lugarNacimiento'],request.form['telefono'],request.form['posgrado'])
        if validarUsuario is True:
            registro= ModelGeneral.nuevoGeneral(db,general,id)
            if registro != None:
                flash("Registrado con exito")
                return redirect(url_for('general'))
            else:
                flash("Error al registrarse")
                return redirect(url_for('general'))
        else:
            actualizar = ModelGeneral.actualizarGeneral(db,general,id)
            if actualizar != None:
                flash("Datos actualizados correctamente")
                return redirect(url_for('general'))
            else:
                flash("Error al actualizar datos")
                return redirect(url_for('general'))
    else:
        if general:
            return render_template('panelPrincipal/informacion/general.html',form=general)
        else:
            return render_template('panelPrincipal/informacion/general.html')
        
    
@app.route('/informacion/estudios',methods=['GET','POST'])
@login_required
def estudios():
    id = current_user.id
    estudios = (ModelEstudios.get_by_id(db,id))
    
    if request.method == 'POST':
            validarEstudios= ModelEstudios.validarEstudio(db,id)
            estudios = Estudios(0,request.form['centroUniversitario'],request.form['carrera'],request.form['cicloEscolar'],request.form['nivelIngles'],request.form['titulado'])
            if validarEstudios is True:
                
                actualizar = ModelEstudios.actualizarEstudios(db,estudios,id)
                if actualizar != None:
                    flash("Datos actualizados correctamente")
                    return redirect(url_for('estudios'))
                else:
                    flash("Error al actualizar datos")
                    return redirect(url_for('estudios'))

            else:
                registro= ModelEstudios.nuevoEstudios(db,estudios,id)
                
                if registro != None:
                    flash("Registrado con exito")
                    return redirect(url_for('estudios'))
                else:
                    flash("Error al registrarse")
                    return redirect(url_for('estudios'))
    
    else:
        if estudios:
            return render_template('panelPrincipal/informacion/estudios.html',form = estudios)
        else:
            return render_template('panelPrincipal/informacion/estudios.html')   

@app.route('/informacion/laboral',methods=['GET','POST'])
@login_required
def laboral():
    id = current_user.id
    trabajo = (ModelTrabajo.get_by_id(db,id))
    if request.method == 'POST':
            validarTrabajo= ModelTrabajo.validarTrabajo(db,id)
            if request.form['estatus'] == 'Si':
                trabajo = Trabajo(0,request.form['estatus'],request.form['nombre'],request.form['ubicacion'],request.form['descripcion'],request.form['antiguedad'],request.form['jornada'])
            else:
                trabajo = Trabajo(0, request.form['estatus'])
         
            if validarTrabajo is True:
                
                actualizar = ModelTrabajo.actualizarTrabajo(db,trabajo,id)
                if actualizar != None:
                    flash("Datos actualizados correctamente")
                    return redirect(url_for('laboral'))
                else:
                    flash("Error al actualizar datos")
                    return redirect(url_for('laboral'))

            else:
                registro= ModelTrabajo.nuevoTrabajo(db,trabajo,id)
                
                if registro != None:
                    flash("Registrado con exito")
                    return redirect(url_for('laboral'))
                else:
                    flash("Error al registrarse")
                    return redirect(url_for('laboral'))
    
    else:
        if trabajo:
            return render_template('panelPrincipal/informacion/laboral.html',form = trabajo)
        else:
            return render_template('panelPrincipal/informacion/laboral.html')
    
@app.route('/tablon')
@login_required
def tablon():
    return render_template('panelPrincipal/tablon/tablon.html',general_active="active")

#---------------------------                 Dashboard                      -----------------------------------##

#Administrador
@app.route('/panelAdmin',endpoint='admin')
@login_required
@role_required(1)
def admin():
    
    registros = ModelAdmin.registros(db)
    cantidad = ModelAdmin.cuentaTitulados(db)
    
    return render_template('panelPrincipal/panelAdmin/dashboard/crud.html',form=registros, titulados= cantidad)


@app.route('/panelAdmin/vermas/<int:id>')
def vermas(id):
    trabajo = (ModelAdmin.laboral(db,id))
    estudios = (ModelAdmin.estudios(db,id))
    general = (ModelAdmin.general(db,id))
    informacion=(ModelAdmin.informacion(db,id))
    return render_template('panelPrincipal/panelAdmin/dashboard/vermas.html',trabajo=trabajo, estudios=estudios, general=general,form=informacion,id=id) 

#---------------------------                                       -----------------------------------##
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
    return redirect(url_for('login'))
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
