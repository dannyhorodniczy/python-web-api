from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from waitress import serve

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default = datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Task {self.id}>'
    
# with app.app_context():
#     db.create_all()

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form['content'] # id of the input we want the contents of
        todo = Todo(content=task_content)

        try:
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'ohhh naoooo, db add no worky'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks) # this must line up with the index.html
    
# this should be a post but we're hacking it as a get :/
@app.route('/delete/<int:id>', methods=["GET"])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'ohhh naoooo, db delete no worky'
    

@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == "POST":
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "fuckl off"
    else:
        return render_template('update.html', task=task_to_update)


if __name__ == '__main__':
    app.run(debug=True)
    # serve(app, host='0.0.0.0', port=8687, threads=1)