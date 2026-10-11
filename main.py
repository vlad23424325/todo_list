from flask import Flask, render_template, request, redirect, url_for
from config import db
from models import Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    tasks = Task.query.all()
    total = len(tasks)
    completed = len([t for t in tasks if t.is_completed])
    return render_template("index.html", tasks=tasks, total=total, completed=completed)

@app.route("/add", methods=["POST"])
def add_task():
    content = request.form.get("content")
    if content and content.strip():
        new_task = Task(content=content.strip())
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_completed = not task.is_completed
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    new_content = request.form.get("content")
    if new_content and new_content.strip():
        task.content = new_content.strip()
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/clear_all")
def clear_all():
    Task.query.delete()
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)