from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    father_name = StringField("Father's Name", validators=[DataRequired(), Length(max=120)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=120)])
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Register Patient')

class PatientSearchForm(FlaskForm):
    search = StringField('Search by Name', validators=[Optional(), Length(max=120)])
    submit = SubmitField('Search')

class VisitForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    symptoms = SelectMultipleField('Symptoms', coerce=str, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    other_symptom = StringField('Other Symptom', validators=[Optional(), Length(max=120)])
    diagnosis_id = SelectField('Diagnosis', coerce=int, validators=[Optional()])
    other_diagnosis = StringField('Other Diagnosis', validators=[Optional(), Length(max=120)])
    submit = SubmitField('Save Visit') 