from flask import Flask,request,url_for,redirect,render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(200), nullable = False)
    date = db.Column(db.DateTime, default = datetime.datetime.today().date())

    def __repr__(self):
        return "Task %r" % self.id

@app.route('/', methods = ["POST","GET"])
def home():
    if request.method == "POST":
        task_content = request.form['task_content']
        new_task = Todo(task = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There is a problem adding the task."
        
    else:
        tasks = Todo.query.all()
    return render_template('home.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There is a problem deleting the task."

@app.route("/update/<int:id>", methods = ["POST","GET"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.task = request.form['task_content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return ""
    else:
        return render_template('update.html',task = task)

if __name__ == "__main__":
    app.run(debug = True)