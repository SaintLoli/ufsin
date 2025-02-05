from flask import Flask, render_template


app = Flask(__name__, template_folder="layout")

@app.route('/')
def login():
    return render_template("login.html")


@app.route("/registration")
def register():
    return render_template("registration.html")


def rtest():
    return "1231231232132123123213"


if __name__ == '__main__':
    app.run(debug=True)
