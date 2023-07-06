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

class Formulario_login(FlaskForm):
    user_name = StringField ("Nombre de usuario", validators=[DataRequired()])
    contraseña = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField ("Iniciar Sesion")


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
    return redirect(url_for("index"))

#DASHBOARD
@app.route('/dashboard', methods = ["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")



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

    if request.method == "POST" and form.validate():
        current_user.user_name = form.user_name.data
        current_user.rol = form.rol.data
        current_user.email = form.email.data
        current_user.nombre = form.nombre.data
        current_user.cedula = form.cedula.data
        current_user.telefono = form.telefono.data
        current_user.contraseña = form.contraseña.data
        db.session.commit()

        return redirect(url_for('dashboard'))

    form.user_name.data = current_user.user_name
    form.rol.data = current_user.rol
    form.email.data = current_user.email
    form.nombre.data = current_user.nombre
    form.cedula.data = current_user.cedula
    form.telefono.data = current_user.telefono

    return render_template('update.html', form=form, current_user=current_user, id=id)

#Eliminar Usuario
@app.route("/eliminar_usuario/<int:id>", methods=["GET", "POST"])
@login_required
def eliminar_usuario(id):
    usuario_eliminar = Usuarios.query.get_or_404(id)
    rol = current_user.rol
    #verifica si el usuario actual es el admin
    if current_user.rol == "Admin":
        #si esxiste el usuario lo eliminamos
        db.session.delete(usuario_eliminar)
        db.session.commit()
        return redirect(url_for("dashboard"))
    
@app.route("/editar_usuario/<int:id>", methods = ["GET","POST"])
@login_required
def editar_usuario(id):
    
    usuario_editar = Usuarios.query.get_or_404(id)
    #Le pasamos el objeto Usuario_editar para que los campos se rellenen automaticamente con los datos del usuario seleccionado
    formulario = Datos_usuarios(obj=usuario_editar)
    
    if current_user.rol == "Admin":
        if request.method == 'POST' and formulario.validate():
            formulario.populate_obj(usuario_editar)
            db.session.commit()

            return redirect(url_for('admins'))

    return render_template('editar_usuario.html', formulario=formulario, usuario_editar=usuario_editar)



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6500,debug=True)




# from flask import Flask , render_template, request

# import os

# app = Flask(__name__)

# @app.route('/')
# def landing_page():
#   return render_template('landing_page.html')

# @app.route('/home')
# def home():
#   return render_template('homepage.html')

# @app.route('/login')
# def login():
#   return render_template('login.html')

# @app.route('/register')
# def register():
#   return render_template('register.html')

# @app.route('/dashboard')
# def dashboard():
#   return render_template('dashboard.html')


# if __name__ == '__main__':
#   app.run(host='127.0.0.1', port= 6500, debug = True)