from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

#set path to db
file_path = os.path.abspath(os.getcwd())+"\\test.db"

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

#create a class to use as a model for our db
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        print('db has successfully been created')
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']

        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'Error occurred adding your task to the list'

    else:
        all_tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=all_tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error occurred while deleting task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Error occurred while updating task'
    else:
        return render_template('update.html', task=task_to_update)
        

if __name__ == "__main__":
    app.run(debug=True)
