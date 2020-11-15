
from flask_login import LoginManager, login_user, current_user,login_required,logout_user
from wtform_fields import *
from models import *


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
    eventitos=Evento.query.filter(Evento.Usuarios_r.any()).all()
    #CAMBIAR ESTA CONSULTA PARA QUE SOLO APAREZCAN LOS DEL USUARIO
    cantidad=len(eventitos)
    evento_form=EventoForm()
    upe_form=UE()
    if upe_form.validate_on_submit():
        idi=Evento.query.filter(Evento.id_evento==upe_form.id_e.data).first()
        if upe_form.delete.data:
            ev=Evento.query.filter(Evento.id_evento==idi.id_evento).first()
            db.session.delete(ev)
            db.session.commit()
            print("Dont preocupeis")
            return redirect(url_for('dashboard'))
        #Evento.query.filter_by(id_evento=idi.id_evento).update({"id_evento":upe_form.id_e.data,"nombre":upe_form.nombre.data,"fecha_inicial":idi.fecha_inicial,"fecha_final":idi.fecha_final,"ubicacion":upe_form.ubicacion.data,"descripcion":upe_form.descripcion.data})
        idi.nombre=upe_form.nombre.data
        idi.fecha_inicial=upe_form.fecha_inicial.data
        idi.fecha_final=upe_form.fecha_final.data
        idi.ubicacion=upe_form.ubicacion.data
        idi.descripcion=upe_form.descripcion.data
        db.session.commit()
        return redirect(url_for('dashboard')) 
        
    if evento_form.validate_on_submit():
        nom=evento_form.nombre.data
        fi=evento_form.fecha_inicial.data
        ff=evento_form.fecha_final.data
        ub=evento_form.ubicacion.data
        desc=evento_form.descripcion.data
        
        id_temp=current_user.get_id()
        evento=Evento(nombre=nom, fecha_inicial=fi, fecha_final=ff, ubicacion=ub, descripcion=desc)
        db.session.add(evento)
        db.session.commit()
        current_user.eventos.append(evento)
        db.session.commit()
        return redirect(url_for('dashboard')) 
    return render_template("/dashboard_true.html",ev_form=evento_form,evs=eventitos,cont=cantidad,up_e=upe_form)
@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    flash('Sesion terminada', 'success')
    return redirect(url_for('login'))
#this is our update route where we are going to update our employee

if(__name__=='__main__'):
    app.run(debug=True)