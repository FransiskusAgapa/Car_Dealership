from flask_app import app
from flask_app.models import user, car
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt # deal with password
bcrypt = Bcrypt(app)
from flask_app.controllers import cars

@app.route("/")
def regs_logs():
    return render_template("index.html")

@app.route("/register/new/user",methods=['POST'])
def try_register():
    if not user.User.validate_user_registration(request.form):
        return redirect("/")
    else:
        # create password hash
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(f"[ Password_hash: {pw_hash} ]")
        new_user = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash
        }
        active_user_id = user.User.save_user(new_user)
        # store user-id into active session
        session['user_id'] = active_user_id
        print(f"Active user_id: {active_user_id} Registered")
        return redirect("/dashboard")

@app.route("/login/user",methods=['POST'])
def try_login():
    if not user.User.validate_user_login(request.form):
        return redirect("/")
    else:
        # check if username exists
        user_data = {
            "email":request.form["email"]
        }
        the_user_by_email = user.User.get_by_user_email(user_data)
        # if user does not exist
        if not the_user_by_email:
            flash("Invalid Email / Password")
            return redirect("/")
        if not bcrypt.check_password_hash(the_user_by_email.password,request.form["password"]):
            flash("Invalid Email / Password")
            return redirect("/")
        if "user_id" not in session:
            session["user_id"] = the_user_by_email.id
        return redirect("/dashboard")
            
@app.route("/dashboard")
def car_dealership():
    if "user_id" in session:
        user_in_session = user.User.read_one_user(session['user_id'])
        all_cars = car.Car.get_all_cars_with_users()
        return render_template("user_dashboard.html",active_user = user_in_session,all_cars = all_cars)
    if "user_id" not in session:
        return redirect("/")

@app.route("/logout")
def try_logout():
    if "user_id" in session:
        session.clear()
    return redirect("/")



