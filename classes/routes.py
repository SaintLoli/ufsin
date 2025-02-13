from flask import Flask, render_template, request, redirect, url_for
from classes.PCInfo import PCInfo
from classes.Filler import *

app = Flask(__name__, template_folder="../layout")
database = DBHelper()


'''Информация о пользователе'''
USER_ID = ''


@app.route('/', methods=["GET", "POST"])
def login():
    global USER_ID

    if request.method == "POST":
        if database.check_user(request.form['login'], request.form["pass"]):
            USER_ID = database.get_user_id(request.form['login'])
            return redirect(url_for('admin_panel'))

    return render_template("login.html")


@app.route("/registration", methods=["GET", "POST"])
def register():
    global USER_ID

    fill_departments()

    if request.method == "POST":
        database.add_user(login=request.form["login"],
                          password=request.form["pass"],
                          fio=request.form["FIO"],
                          number=request.form["number"],
                          tubel_number=request.form["tubel_number"],
                          dep=request.form["department"])

        USER_ID = database.get_user_id(request.form['login'])
        return redirect(url_for("check_data"))

    return render_template("registration.html", departments=DEPARTMENTS)


@app.route("/admin_home")
def admin_panel():
    PC = database.get_computer_info(int(USER_ID))
    fill_devices(USER_ID)

    return render_template("admin_home.html",
                           devices=DEVICES)


@app.route("/admin_home/staff")
def staff():
    fill_users()
    return render_template("staff.html", users=USERS)


@app.route("/admin_home/sklad")
def sklad():
    fill_warehouses()
    return render_template("sklad.html", warehouses=WAREHOUSES)


@app.route("/admin_home/otchet")
def otchet():

    if request.method == "POST":
        print(request.form["start_date"])
        print(request.form["end_date"])


    return render_template("otchet.html")


@app.route("/admin_home/departments")
def departments():
    fill_departments()
    return render_template("departments.html",
                           departments=DEPARTMENTS)


@app.route("/check_data", methods=["GET", "POST"])
def check_data():
    PC = PCInfo()
    if request.method == "POST":
        database.add_computer_info(user_id=USER_ID,
                                   cpu=request.form["cpu"],
                                   motherboard=request.form["motherboard"],
                                   gpu=request.form["gpu"],
                                   ram=request.form["ram"],
                                   year=request.form["year"],
                                   s_number=request.form["s_number"])


    return render_template("check.html", cpu=PC.processor,
                                         motherboard=PC.motherboard,
                                         gpu=PC.video_card)



if __name__ == '__main__':
    app.run(debug=True)