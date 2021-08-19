from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_app.models.user import User
from flask_app.controllers import users


@app.route("/show/<int:sighting_id>")
def view_instruct(sighting_id):
    if 'user_id' not in session:
        return redirect('/')
    
    sighting = Sighting.getOneById(sighting_id)
    user = User.getOneById(sighting.user_id)
    return render_template("show_info.html", sighting = sighting, user = user)

@app.route("/new/sighting")
def create_page():
    if 'user_id' not in session:
        return redirect('/')
    user = User.getOneById(session["user_id"])
    
    return render_template("report_sight.html", user= user)

@app.route("/create", methods=['POST'])
def add_new_re():
       
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "location" : request.form["location"],
        "what_happened" : request.form["what_happened"],
        "date_of_siting" : request.form["date_made"],
        "num_sasquatches" : request.form["num_sasquatches"],
        "user_id" : session["user_id"]
        }  
 
    if not Sighting.validate_sighting(data):
        return redirect("/new/sighting")
   
    Sighting.create(data)
    return redirect('/dashboard')


@app.route("/sighting/<int:sighting_id>/edit")
def edit_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/')
    
    sighting = Sighting.getOneById(sighting_id)
    user = User.getOneById(sighting.user_id)
    
    return render_template("edit.html", sighting = sighting, user = user)

@app.route("/edit/<int:sighting_id>", methods =["POST"])
def update_one(sighting_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": sighting_id,
        "location" : request.form["location"],
        "what_happened" : request.form["what_happened"],
        "date_of_siting" : request.form["date_made"],
        "num_sasquatches" : request.form["num_sasquatches"],
        "user_id" : session["user_id"]
        }   
   
    if not Sighting.validate_sighting(data):
        return redirect(f"/sighting/{sighting_id}/edit")
    Sighting.edit(data)
    return redirect('/dashboard')


@app.route("/sighting/<int:sighting_id>/delete")
def delete_one(sighting_id):
    if 'user_id' not in session:
        return redirect('/')
    
    Sighting.delete(sighting_id)
    return redirect('/dashboard')

