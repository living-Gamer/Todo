from datetime import date, datetime
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.Date, default=date)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db.session.add(Todo(title=request.form['title'], desc=request.form['desc']))
        db.session.commit()
    return render_template('index.html', alltodo=Todo.query.all())

@app.route('/delete/<int:sno>')
def delete(sno):
    allTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    reqTodo = Todo.query.filter_by(sno=sno).first()
    if request.method == "GET": 
        return render_template('update.html', reqTodo=reqTodo)
    elif request.method == "POST":
        reqTodo.title = request.form['title']
        reqTodo.desc = request.form['desc']
        reqTodo.date_created = datetime.strptime(request.form['date_created'], '%Y-%m-%d')
        db.session.commit()
        return redirect('/')
if __name__ == '__main__':
    app.run(debug=True)