from flask import Flask, render_template,redirect,url_for,flash
from flask_login import LoginManager, login_user, current_user,login_required,logout_user
from wtform_fields import *
from models import *

app=Flask(__name__)
app.secret_key='replace_later'
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://rafxar:password@localhost/gestor'
db=SQLAlchemy(app)
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/', methods=['GET','POST'])
def login():
    reg_form=RegistrationForm()
    log_form=LoginForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password= reg_form.password.data

        hashed_pswd = pbkdf2_sha256.hash(password)
        email=reg_form.email.data
        #Añade usuario a la BD
        user=User(usuario=username, contraseña=hashed_pswd,email=email)
        db.session.add(user)
        db.session.commit()
        #flash('Registrado con éxito! Por favor inicie sesion.','success')
        return redirect(url_for('login'))
    if log_form.validate_on_submit():
        user_object = User.query.filter_by(usuario=log_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('dashboard'))
        
    return render_template("index_true.html",reg_form=reg_form,log_form=log_form)

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if not current_user.is_authenticated:
        flash('Primero inicia sesión :D', 'danger')
        
    return render_template("/dashboard.html")

@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    flash('Sesion terminada', 'success')
    return redirect(url_for('login'))
if(__name__=='__main__'):
    app.run(debug=True)