from flask import Flask, render_template, request, redirect, url_for, flash, jsonify    
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
# app.app_context()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(00), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # with app.app_context():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        # print(request.form['title'])

    allTodo = Todo.query.all()

    return render_template('index.html', allTodo=allTodo)
    # return 'Hello, World!'

@app.route('/products')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    # return render_template('index.html')
    return 'Hello, Here comes the products'

@app.route('/delete/<int:sno>')
def delete(sno):

    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.description=description
        db.session.add(todo)
        db.session.commit()

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)