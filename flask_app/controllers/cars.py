from flask_app import app
from flask_app.models import user, car
from flask import render_template, redirect, request, session
from flask_app.controllers import users

# Create a new car
@app.route("/new",methods=['POST','GET'])
def new_car():
    if request.method == 'GET':
        user_in_session = user.User.read_one_user(session['user_id'])
        return render_template("add_car.html", active_user=user_in_session)
    if request.method == 'POST':
        if "user_id" in session:
            if not car.Car.validate_car_data(request.form):
                return redirect("/new")
            else:
                new_car = {
                    "price":request.form["price"],
                    "model":request.form["model"],
                    "make":request.form["make"],
                    "year":request.form["year"],
                    "description":request.form["description"],
                    "user_id":request.form["user_id"]
                }
                car.Car.save_car(new_car)
                return redirect("/dashboard")
        if "user_id" not in session:
            return redirect("/")

# Read a car
@app.route("/view/<int:car_id>")
def view_car(car_id):
    if 'user_id' in session:
        the_car_in_session = car.Car.read_one_car(car_id)
        the_car_seller = user.User.read_one_user(the_car_in_session.user_id)
        return render_template("view_car.html", the_car = the_car_in_session,the_car_seller=the_car_seller)

# Update a car
@app.route("/edit/<int:car_id>",methods=['POST','GET'])
def edit_car(car_id):
    if request.method == 'GET':
        active_car = car.Car.read_one_car(car_id)
        return render_template("edit_car.html", active_car=active_car)
    if request.method == 'POST':
        if 'user_id' in session:
            print("[ Update Car Route ]")
            updated_data = {
                "id":request.form["id"],
                "price":request.form["price"], 
                "model": request.form["model"],
                "make":request.form["make"],"year":request.form["year"],"description":request.form["description"]
            }
            car.Car.update_car_data(updated_data)
            return redirect("/dashboard")
        if 'user_id' not in session:
            return redirect("/")

# Delete \ Purchase a car
@app.route("/purchase/car/<int:car_id>")
def purchase_car(car_id):
    if "user_id" in session:
        print("[ Route Purchase Car ]")
        car.Car.delete_car(car_id)
        return redirect("/dashboard")
    if "user_id" not in session:
        return redirect("/")