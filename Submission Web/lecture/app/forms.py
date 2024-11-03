from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Regexp


# This is the form class

class UserForm(FlaskForm):
    assesement_title= StringField('Assesment Title', validators=[DataRequired()])
    module_code = StringField('Module Code', validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z]{4}\d{4}$', message="Module code must be 4 letters followed by 4 numbers (e.g., COMP1000).")
    ])
    # the validator above checks that the module code is in the format of 4 letters followed by 4 numbers as specific in the rubric. This allows us to validate the input from the user.
    
    deadline = StringField('Deadline', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    completed = BooleanField('Completed ? : (Tick for yes) (Blank for no)') # This is a checkbox field
    submit = SubmitField('Submit')