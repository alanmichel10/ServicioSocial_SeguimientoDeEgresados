from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, logout_user, login_user, login_required, current_user
from config import config
import tempfile

# Modulos
from models.ModelUser import ModelUser
from models.ModelGeneral import ModelGeneral
from models.ModelEstudios import ModelEstudios
from models.ModelTrabajo import ModelTrabajo
from models.ModelAdmin import ModelAdmin
# Entities
from models.entities.User import User
from models.entities.General import General
from models.entities.Estudios import Estudios
from models.entities.Trabajo import Trabajo

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
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['correo'])
        # print(request.form['clave'])
        user = User(0, request.form['correo'], request.form['clave'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.clave:

                login_user(logged_user)
                
                
                return redirect(url_for('inicio'))
            else:
                flash("Contraseña incorrecta")
                return render_template('login/login.html')

        else:
            flash("Usuario no encontrado.")
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
@login_required 

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
