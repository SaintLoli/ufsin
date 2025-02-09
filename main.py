from flask import Flask, render_template, request, redirect, url_for
from classes.DB_helper import  DBHelper
from classes.PCInfo import PCInfo

app = Flask(__name__, template_folder="layout")
database = DBHelper()


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # PC = PCInfo()
        if database.check_user(request.form['login'], request.form["pass"]):
            # return redirect(url_for('admin_panel'))
            return redirect(url_for('check_data'))

    return render_template("login.html")


@app.route("/registration", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        database.add_user(login=request.form["login"],
                          password=request.form["pass"],
                          fio=request.form["FIO"])

        return redirect(url_for("check_data"))

    return render_template("registration.html")


@app.route("/admin_home")
def admin_panel():
    return render_template("admin_home.html")


@app.route("/check_data", methods=["GET", "POST"])
def check_data():
    PC = PCInfo()

    return render_template("check.html", cpu=PC.processor,
                                         motherboard=PC.motherboard,
                                         gpu=PC.video_card)


if __name__ == '__main__':
    app.run(debug=True)
