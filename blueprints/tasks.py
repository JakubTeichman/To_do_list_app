from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Task
from database import db
from forms import TaskForm
from decorator import role_required
from datetime import datetime

task_mg = Blueprint('task_mg', __name__)

@task_mg.route('/task/add', methods=['GET', 'POST'])
@login_required
@role_required("user")
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(title=form.title.data, description=form.description.data, deadline = form.deadline.data)
        new_task.user_id = current_user.id
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('task_mg.dashboard'))
    flash('Invalid data. Make sure you enter deadline!')
    return render_template('task.html', form=form)

@task_mg.route('/task/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required("user")
def edit_task(id):
    task = Task.query.filter_by(user_id=current_user.id).filter_by(id=id).first()
    if not task:
        flash('Task not found.')
        return redirect(url_for('task_mg.dashboard'))

    form = TaskForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        if form.deadline.data:
            task.deadline = datetime.combine(form.deadline.data, datetime.min.time())
        db.session.commit()
        flash('Task updated successfully.')
        return redirect(url_for('task_mg.dashboard'))
    
    if request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.deadline.data = task.deadline.date() if task.deadline else None

    return render_template('task.html', form=form)


@task_mg.route('/task/<int:id>/delete', methods=['GET', 'POST'])
@login_required
@role_required("user")
def delete_task(id):
    task = Task.query.filter_by(user_id=current_user.id).filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('task_mg.dashboard'))

@task_mg.route('/admin/dashboard')
@login_required
@role_required('admin')
def admin_view():
    tasks = Task.query.all()
    return render_template('dashboard.html', role = current_user.role, tasks = tasks)

@task_mg.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', role = current_user.role, tasks = current_user.tasks)