from flask import Flask, render_template, request
from classes.DB_helper import  DBHelper

app = Flask(__name__, template_folder="layout")
database = DBHelper()

@app.route('/')
@app.route('/login')
def login():
    if database.check_user(request.form["login"], password=request.form["pass"]):
        return render_template("home.html")

    return render_template("login.html")


@app.route("/registration", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        database.add_user(login=request.form["login"],
                          password=request.form["pass"],
                          fio=request.form["FIO"])

    return render_template("registration.html")




if __name__ == '__main__':
    app.run(debug=True)
