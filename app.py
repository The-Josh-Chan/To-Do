from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #Tell app where database is located
db = SQLAlchemy(app) #initializing databse

# Create a class for each item in todo list (Template for each todo list item)
class todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    notes = db.Column(db.String(500), nullable = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id

@app.route('/', methods=['POST', 'GET'])
# methods Post will allow to send data to database
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_notes = request.form['notes']
        new_task = todo(content=task_content, notes=task_notes)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your task"

    else:
        #Return all data in database ordered by date created
        tasks = todo.query.order_by(todo.date_created).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = todo.query.get_or_404(id) #Get task by id
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.notes = request.form['notes']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error updating task'
    else:
        return render_template('update.html', task = task)

if __name__ == '__main__':
    app.run(debug=True)
