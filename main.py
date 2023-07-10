from flask import Flask, render_template, redirect, url_for, request, flash 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#@login_required : solo da acceso a los usuarios que hayan iniciado sesion.

#Iniciamos Flask 
app = Flask(__name__)
#Le agregamos la DB y utilizamos sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
#Creamos la secret key 
app.config['SECRET_KEY'] = "lslsls"
#Inicializamos la db
db = SQLAlchemy(app)
#Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

#Creo el modelo de la base de datos
class Usuarios(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) #Le damos la primary key para que el id sea unico 
    user_name = db.Column(db.String(20),  nullable = False, unique = True)   #Null significa vacio, al asignar False a nullable no dejaremos que este campo quede vacio, Le asignamos unique True para que no se pueda repetir el mail en otra cuenta
    nombre = db.Column(db.String(100), nullable = False)
    rol = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    cedula = db.Column(db.String(50), nullable = False)
    telefono = db.Column(db.String(50), nullable = False)
    contraseña = db.Column(db.String(20), nullable = False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self,user_name,nombre, rol, email, cedula, telefono, contraseña):
        self.user_name = user_name
        self.nombre = nombre 
        self.rol = rol
        self.email = email 
        self.cedula = cedula
        self.telefono = telefono
        self.contraseña = contraseña 

#Creo la clase para almacenar las tareas
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    completada = db.Column(db.Boolean, default=False)

    def __init__(self, nombre, descripcion, completada=False):
        self.nombre = nombre
        self.descripcion = descripcion
        self.completada = completada

    # App context se encarga de que se ejecute create all en el contexto de flask, para evitar errores en la config de la db. 
with app.app_context():
        
        # Se encarga de crear las tablas que establecimos anteriormente 
    db.create_all()        

#Creamos la clase para los formularios
#Utilizo los validator de wtforms para que no quede un espacio del formulario vacio
class Datos_usuarios(FlaskForm):
    user_name = StringField ("Nombre de usuario", validators=[DataRequired()])
    nombre = StringField ("Nombre y Apellido", validators=[DataRequired()])
    rol = StringField ("Rol", validators=[DataRequired()])
    email = StringField ("E-mail", validators=[DataRequired()])
    cedula = StringField("Cedula de identidad", validators=[DataRequired()])
    telefono = StringField("Numero de telefono", validators=[DataRequired()])
    contraseña = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField ("Crear cuenta")

#Formulario para el login
class Formulario_login(FlaskForm):
    user_name = StringField ("Nombre de usuario", validators=[DataRequired()])
    contraseña = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField ("Iniciar Sesion")

#Formulario para las tareas
class FormularioTarea(FlaskForm):
    nombre = StringField("Nombre de la tarea", validators=[DataRequired()])
    descripcion = StringField("Describe la tarea", validators=[DataRequired()])
    submit = SubmitField("Agregar tarea")

#Pagina de inicio
@app.route("/")
def index():
    return render_template("homepage.html")

#Pagina de ADMIN
@app.route("/admins", methods = ["GET", "POST"])
@login_required
def admins():
    usuarios = Usuarios.query.all()
    #Le daremos acceso a esta pestaña solo a los admins de la pagina
    rol = current_user.rol
    if rol == "Admin":
        return render_template("admins.html",usuarios=usuarios)
    else:
        return render_template("dashboard.html")

#Iniciar sesion
@app.route("/login", methods = ["GET", "POST"])
def login():
    formulario = Formulario_login()
    #validamos el formulario cuando se envie
    if formulario.validate_on_submit():
        usuario = Usuarios.query.filter_by(user_name = formulario.user_name.data).first()
        
        if usuario and usuario.contraseña == formulario.contraseña.data:
            login_user(usuario)
            return redirect(url_for("dashboard"))
            
    return render_template("login.html",formulario = formulario)
#Logout
@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():   
    logout_user()
    return redirect(url_for("login"))

#DASHBOARD
@app.route('/dashboard', methods = ["GET", "POST"])
@login_required

def dashboard():
    tareas = Tarea.query.all()
    return render_template("dashboard.html",tareas=tareas)

#Ruta de registro de usuario
@app.route("/register", methods = ["GET", "POST"] )
def register():
    nombre = None
    formulario = Datos_usuarios()

    #Validamos el formulario
    if request.method == "POST":
        #Hacemos un query a la base de datos a traves del email
        usuario = Usuarios.query.filter_by(email=formulario.email.data).first()
        #Si no hay un usuario con el mail ingresado agregalo a la base de datos.
        if usuario is None:
            user_name = request.form['user_name']
            nombre = request.form['nombre']
            rol = request.form['rol']
            email = request.form['email']
            cedula = request.form['cedula']
            telefono = request.form['telefono']
            contraseña = request.form['contraseña']
            
        #lo agregamos a la base de datos
            nuevo_usuario = Usuarios(user_name, nombre, rol, email, cedula, telefono, contraseña)
            db.session.add(nuevo_usuario)
            db.session.commit()

    usuarios_registrados = Usuarios.query.order_by(Usuarios.date_added)

    return render_template("register.html",  formulario = formulario, usuarios_registrados = usuarios_registrados)

# Actualizar datos en la DB
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = Datos_usuarios()
    usuario = Usuarios.query.get(id)
    if request.method == "POST":

        usuario.user_name = request.form['user_name']
        usuario.nombre = request.form['nombre']
        usuario.rol = request.form['rol']
        usuario.email = request.form['email']
        usuario.cedula = request.form['cedula']
        usuario.telefono = request.form['telefono']
        usuario.contraseña = request.form['contraseña']

        db.session.commit()
        print(current_user)

        return redirect(url_for('dashboard'))
    return render_template('update.html', form=form, usuario=usuario, id=id)

#Eliminar Usuario
@app.route("/eliminar_usuario/<int:id>", methods=["GET", "POST"])
@login_required
def eliminar_usuario(id):
    if current_user.rol != "Admin":
        return redirect(url_for("dashboard"))

    usuario_eliminar = Usuarios.query.get_or_404(id)
    rol = current_user.rol
    #verifica si el usuario actual es el admin
    if current_user.rol == "Admin":
        #si esxiste el usuario lo eliminamos
        db.session.delete(usuario_eliminar)
        db.session.commit()
        return redirect(url_for("dashboard"))
    
@app.route("/admin_edit/<int:id>", methods = ["GET","POST"])
@login_required
def admin_edit(id):
    if current_user.rol != "Admin":
        return redirect(url_for("dashboard"))

    
    usuario = Usuarios.query.get_or_404(id)
    #Le pasamos el objeto Usuario_editar para que los campos se rellenen automaticamente con los datos del usuario seleccionado
    formulario = Datos_usuarios(obj=usuario)
    
    if current_user.rol == "Admin":
        if request.method == 'POST' and formulario.validate():
            formulario.populate_obj(usuario)
            db.session.commit()

            return redirect(url_for('admins'))

    return render_template('update.html', formulario=formulario, usuario=usuario)

#Ruta para crear las tareas
@app.route("/agregar_tareas", methods=["GET", "POST"])
@login_required
def agregar_tareas():
    if current_user.rol != "Admin":
        return redirect(url_for("dashboard"))

    formulario = FormularioTarea()

    if request.method == "POST":
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']


        
        nueva_tarea = Tarea(nombre=nombre, descripcion=descripcion, )
        db.session.add(nueva_tarea)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("agregar_tareas.html", formulario=formulario)

#Para marcar la tarea como completada
@app.route("/marcar_completada/<int:id>", methods=["GET","POST"])
@login_required
def marcar_completada(id):
    tarea = Tarea.query.get_or_404(id)
    completa = True


    if current_user.rol != "Admin":
        return redirect(url_for('dashboard'))
    
    tarea.completada = True
    db.session.commit()

    return redirect(url_for("dashboard", tarea=tarea, completa=completa))

#Eliminar Tarea
@app.route("/eliminar_tarea/<int:id>", methods=["GET", "POST"])
@login_required
def eliminar_tarea(id):
    if current_user.rol != "Admin":
        return redirect(url_for("dashboard"))

    tarea_eliminar = Tarea.query.get_or_404(id)

    #verifica si el usuario actual es el admin
    if current_user.rol == "Admin":
        #si esxiste el usuario lo eliminamos
        db.session.delete(tarea_eliminar)
        db.session.commit()
        return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6500,debug=True)
