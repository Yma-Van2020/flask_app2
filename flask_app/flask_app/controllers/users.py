from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt   
bcrypt = Bcrypt(app)  
from flask_app.models.user import User
from flask_app.models.sighting import Sighting

@app.route("/")
def index():
    
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    
    if not User.validate_user(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
        
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }

    user_id = User.create(data)
    session["user_id"] = user_id 
    return redirect('/')

    
@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["lemail"] }
    user_in_db = User.get_by_email(data)
    
    if not user_in_db:
        flash("* Invalid Email/Password", "lemail")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['lpassword']):
        flash("* Invalid Email/Password", "lpassword")
        return redirect("/")
    
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()   
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login before trying to go to dashboard page')
        return redirect('/')
    data = {
        "id":session['user_id']
    }
    user = User.getOneById(session['user_id'])
    sightings = Sighting.getAll()
    
    
    return render_template('dashboard.html',user=user, sightings = sightings)
