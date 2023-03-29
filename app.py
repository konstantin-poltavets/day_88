from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/add')
def index():
    return render_template('index.html')

class Task(db.Model):
        
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.task}>'

with app.app_context():
     db.create_all()
     
     
@app.route('/add_todo', methods=['POST'])
def add_todo():
    new_task = Task(
            task=request.form["task"],
            complete=False
        )    
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')


@app.route('/')
def todo_list():
    todo = Task.query.all()
    return render_template('todo_list.html', todos=todo)


@app.route('/todo/<int:todo_id>/edit', methods=['GET', 'POST'])
def todo_edit(todo_id):
    new_var = todo_id
    todo = Task.query.get_or_404(new_var)
    if request.method == 'POST':
        check_done = request.form.get('check_done')
        todo.task = request.form['task']
        try:
            if check_done == 'on':
                todo.complete = True
            else:
                todo.complete = False
        except:
            todo.complete = False
        db.session.commit()

        return redirect(url_for('todo_list'))
    return render_template('todo_edit.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)