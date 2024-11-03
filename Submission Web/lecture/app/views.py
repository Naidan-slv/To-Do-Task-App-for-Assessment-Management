from app import app, db
from flask import Flask, render_template, flash, redirect, url_for, request
from .models import Tasks
from .forms import UserForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

@app.route('/')
def home():
    return redirect(url_for('all_tasks'))

@app.route('/all_tasks')
def all_tasks():
    tasks = Tasks.query.order_by(Tasks.deadline).all()  
    return render_template('ViewAll.html', tasks=tasks) 


#route to view all uncompleted tasks by filtering the tasks by the completed column
@app.route('/uncompleted')
def uncompleted_tasks():
    tasks = Tasks.query.filter_by(completed=False).order_by(Tasks.deadline).all()
    return render_template('uncompleted.html', tasks=tasks)


# route to view all completed tasks by filtering the tasks by the completed column
@app.route('/completed')
def completed_tasks():
    tasks = Tasks.query.filter_by(completed=True).order_by(Tasks.deadline).all()
    return render_template('completed.html', tasks=tasks)

#adding a new task to the database with the form data
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        deadline_date = datetime.strptime(form.deadline.data, '%Y-%m-%d').date()

        task = Tasks(
            assesement_title=form.assesement_title.data,
            module_code=form.module_code.data,
            deadline=deadline_date,
            description=form.description.data,
            completed=False)
            
        db.session.add(task)
        db.session.commit()
        flash(f'"{task.assesement_title}" has been created   ')


        form.assesement_title.data = ''
        form.module_code.data = ''
        form.deadline.data = ''
        form.description.data = ''

        the_tasks = Tasks.query.order_by(Tasks.deadline)

    return render_template('add_user.html', form=form)

#route to delete a task from the database
@app.route('/delete/<int:id>', methods=['POST','GET'])
def delete(id):

    task = Tasks.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash(f'"{task.assesement_title}" has been deleted   ')
    return redirect(url_for('all_tasks'))

#route to edit a task in the database by grabbing the task by its id and then updating its values using the form
@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    task_to_edit = Tasks.query.get_or_404(id)
    form = UserForm(obj=task_to_edit)

    if request.method == 'POST' and form.validate_on_submit():
        try:
            task_to_edit.assesement_title = form.assesement_title.data
            task_to_edit.module_code = form.module_code.data
            task_to_edit.deadline = datetime.strptime(form.deadline.data, '%Y-%m-%d').date()
            task_to_edit.description = form.description.data
            task_to_edit.completed = 'completed' in request.form
            db.session.commit()
            flash(f'"{task_to_edit.assesement_title}" has been updated   ')
            return redirect(url_for('all_tasks'))
        except Exception as e:
            db.session.rollback()
            flash(f'there was an error updating the task: {e}')
            return render_template('update.html', form=form, task_to_edit=task_to_edit)
    else:
        return render_template('update.html', form=form, task_to_edit=task_to_edit)
