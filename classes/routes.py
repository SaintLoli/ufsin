from flask import Flask, render_template, request, redirect, url_for
from classes.DB_helper import  DBHelper
from classes.PCInfo import PCInfo

app = Flask(__name__, template_folder="../layout")
database = DBHelper()

"""
Информация о пользователе
"""
USER_ID = ''


@app.route('/', methods=["GET", "POST"])
def login():
    global USER_ID

    if request.method == "POST":
        # PC = PCInfo()
        if database.check_user(request.form['login'], request.form["pass"]):
            USER_ID = database.get_user_id(request.form['login'])
            return redirect(url_for('admin_panel'))

    return render_template("login.html")


@app.route("/registration", methods=["GET", "POST"])
def register():
    global USER_ID
    if request.method == "POST":
        database.add_user(login=request.form["login"],
                          password=request.form["pass"],
                          fio=request.form["FIO"],
                          number=request.form["number"],
                          tubel_number=request.form["tubel_number"])

        USER_ID = database.get_user_id(request.form['login'])
        return redirect(url_for("check_data"))

    return render_template("registration.html")


@app.route("/admin_home")
def admin_panel():
    PC = database.get_computer_info(int(USER_ID))
    print(PC)
    return render_template("admin_home.html",
                           motherboard=PC[1],
                           cpu=PC[0],
                           gpu=PC[2],
                           ram=PC[3],
                           s_number=PC[5],
                           year=PC[4],
                           monitor=database.get_item("monitor", int(USER_ID)),
                           tel=database.get_item("tel", int(USER_ID)))


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
