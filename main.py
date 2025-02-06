from flask import Flask, render_template, request


app = Flask(__name__, template_folder="layout")

@app.route('/')
def login():
    return render_template("login.html")


@app.route("/registration", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        FIO = request.form["FIO"]
        username = request.form['login']
        password = request.form['pass']

        print(FIO, username, password)
    return render_template("registration.html")




if __name__ == '__main__':
    app.run(debug=True)
