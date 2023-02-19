from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class ToDo(db.Model):  # type: ignore
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allToDo = ToDo.query.all()
    return render_template("index.html", allToDo=allToDo)

def about():
    return render_template("about.html")

app.add_url_rule("/about.html", "about", about)

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    if not path.exists("./instace/todo.db"):
        app.app_context().push()
        db.create_all()
        # Creating database if it doesn't exist
    
    else:
        pass
        # Ignoring the query as database already exists

    # app.run(debug = False, host = '0.0.0.0')
    app.run(debug=False, host = '0.0.0.0', port=6969)
