from flask import Flask, render_template, redirect, url_for, flash, session, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from werkzeug.security import check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Doctor, Patient, Diagnosis, Medication, Visit, Prescription
from forms import LoginForm, PatientForm, VisitForm, PatientSearchForm

db.init_app(app)
csrf = CSRFProtect(app)

# Professional symptom and diagnosis lists
SYMPTOM_LIST = [
    'Anxiety', 'Depression', 'Hallucinations', 'Delusions', 'Mania', 'Insomnia', 'Suicidal thoughts',
    'Obsessions', 'Compulsions', 'Paranoia', 'Memory loss', 'Disorganized speech', 'Social withdrawal',
    'Fatigue', 'Irritability', 'Panic attacks', 'Flashbacks', 'Appetite changes', 'Sleep disturbances',
    'Euphoria', 'Grandiosity', 'Hyperactivity', 'Self-harm', 'Substance abuse', 'Confusion', 'Mood swings',
    'Avoidance', 'Physical complaints', 'Disinhibition', 'Impulsivity', 'Guilt', 'Hopelessness', 'Anhedonia', 'Fear'
]

DIAGNOSIS_LIST = [
    'Major Depressive Disorder', 'Generalized Anxiety Disorder', 'Bipolar Disorder', 'Schizophrenia',
    'Obsessive-Compulsive Disorder', 'Panic Disorder', 'Post-Traumatic Stress Disorder', 'Social Anxiety Disorder',
    'Attention Deficit Hyperactivity Disorder', 'Autism Spectrum Disorder', 'Borderline Personality Disorder',
    'Dissociative Identity Disorder', 'Somatic Symptom Disorder', 'Delusional Disorder', 'Acute Psychosis',
    'Adjustment Disorder', 'Anorexia Nervosa', 'Bulimia Nervosa', 'Substance Use Disorder', 'Insomnia Disorder',
    'Hypomania', 'Cyclothymia', 'Schizoaffective Disorder', 'Paranoid Personality Disorder', 'Avoidant Personality Disorder',
    'Dependent Personality Disorder', 'Antisocial Personality Disorder', 'Histrionic Personality Disorder',
    'Narcissistic Personality Disorder', 'Specific Phobia', 'Agoraphobia', 'Seasonal Affective Disorder', 'PTSD', 'Other'
]

# Example prescription suggestions for some diagnoses
DIAGNOSIS_PRESCRIPTIONS = {
    'Major Depressive Disorder': ['Sertraline', 'Fluoxetine', 'Escitalopram', 'Mirtazapine'],
    'Generalized Anxiety Disorder': ['Escitalopram', 'Sertraline', 'Buspirone', 'Diazepam'],
    'Bipolar Disorder': ['Lithium', 'Valproate', 'Olanzapine', 'Quetiapine'],
    'Schizophrenia': ['Risperidone', 'Olanzapine', 'Haloperidol', 'Clozapine'],
    'Obsessive-Compulsive Disorder': ['Fluoxetine', 'Sertraline', 'Clomipramine'],
    'Panic Disorder': ['Paroxetine', 'Sertraline', 'Alprazolam'],
    'Post-Traumatic Stress Disorder': ['Sertraline', 'Paroxetine', 'Venlafaxine'],
    'Other': []
}

# Branding info
CLINIC_BRAND = {
    'doctor': 'Prof. Dr. Wajid Ali Akhunzada',
    'title': 'Professor Psychiatry',
    'clinic': 'Opposite lady Griffith school, near Dabgari Garden Road, Shuba Bazaar, Peshawar',
    'phone': '(091) 2568085'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'doctor_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_branding():
    return dict(CLINIC_BRAND=CLINIC_BRAND)

@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('patients'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(username=form.username.data).first()
        if doctor and check_password_hash(doctor.password_hash, form.password.data):
            session['doctor_id'] = doctor.id
            flash('Logged in successfully.', 'success')
            return redirect(url_for('patients'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/patients', methods=['GET', 'POST'])
@login_required
def patients():
    form = PatientSearchForm()
    query = Patient.query
    if form.validate_on_submit() and form.search.data:
        search_term = f"%{form.search.data.strip()}%"
        query = query.filter(Patient.name.ilike(search_term))
    patients = query.all()
    return render_template('patients.html', patients=patients, form=form)

@app.route('/register_patient', methods=['GET', 'POST'])
@login_required
def register_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            name=form.name.data,
            father_name=form.father_name.data,
            age=form.age.data,
            sex=form.sex.data,
            contact=form.contact.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient registered successfully.', 'success')
        return redirect(url_for('patients'))
    return render_template('register_patient.html', form=form)

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)
    if form.validate_on_submit():
        patient.name = form.name.data
        patient.father_name = form.father_name.data
        patient.age = form.age.data
        patient.sex = form.sex.data
        patient.contact = form.contact.data
        db.session.commit()
        flash('Patient updated successfully.', 'success')
        return redirect(url_for('patients'))
    return render_template('register_patient.html', form=form, edit_mode=True)

@app.route('/delete_patient/<int:patient_id>')
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    # Delete all visits and prescriptions for this patient
    for visit in patient.visits:
        Prescription.query.filter_by(visit_id=visit.id).delete()
        db.session.delete(visit)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient and all related visits deleted.', 'info')
    return redirect(url_for('patients'))

@app.route('/new_visit', methods=['GET', 'POST'])
@login_required
def new_visit():
    form = VisitForm()
    form.patient_id.choices = [(p.id, p.name) for p in Patient.query.all()]
    form.symptoms.choices = [(s, s) for s in SYMPTOM_LIST] + [('Other', 'Other')]
    form.diagnosis_id.choices = [(i+1, d) for i, d in enumerate(DIAGNOSIS_LIST)]
    medications = Medication.query.all()
    diagnosis_name = None
    suggested_prescriptions = []
    visit_history = []
    selected_patient = None
    if request.method == 'GET' and request.args.get('patient_id'):
        form.patient_id.data = int(request.args.get('patient_id'))
    if form.patient_id.data:
        selected_patient = Patient.query.get(form.patient_id.data)
        if selected_patient:
            visit_history = Visit.query.filter_by(patient_id=selected_patient.id).order_by(Visit.date.desc()).all()
    if form.validate_on_submit():
        selected_symptoms = form.symptoms.data
        if 'Other' in selected_symptoms and form.other_symptom.data:
            selected_symptoms = [s for s in selected_symptoms if s != 'Other'] + [form.other_symptom.data]
        symptoms_str = ", ".join(selected_symptoms)
        diagnosis_id = form.diagnosis_id.data
        diagnosis_name = DIAGNOSIS_LIST[diagnosis_id-1] if diagnosis_id and diagnosis_id <= len(DIAGNOSIS_LIST) else None
        if diagnosis_name == 'Other' and form.other_diagnosis.data:
            diagnosis_name = form.other_diagnosis.data
        diagnosis_obj = Diagnosis.query.filter_by(name=diagnosis_name).first()
        if not diagnosis_obj:
            diagnosis_obj = Diagnosis(name=diagnosis_name)
            db.session.add(diagnosis_obj)
            db.session.commit()
        visit = Visit(
            patient_id=form.patient_id.data,
            doctor_id=session['doctor_id'],
            diagnosis_id=diagnosis_obj.id,
            symptoms=symptoms_str
        )
        db.session.add(visit)
        db.session.flush()
        prescriptions = []
        idx = 0
        while True:
            med_id = request.form.get(f'medication_id_{idx}')
            dosage = request.form.get(f'dosage_{idx}')
            duration = request.form.get(f'duration_{idx}')
            custom_med = request.form.get(f'custom_medication_{idx}')
            if not med_id and not custom_med:
                break
            if med_id and med_id != 'Other':
                prescription = Prescription(
                    visit_id=visit.id,
                    medication_id=int(med_id),
                    dosage=dosage,
                    duration=duration
                )
            else:
                med_name = custom_med
                med_obj = Medication.query.filter_by(name=med_name).first()
                if not med_obj:
                    med_obj = Medication(name=med_name)
                    db.session.add(med_obj)
                    db.session.commit()
                prescription = Prescription(
                    visit_id=visit.id,
                    medication_id=med_obj.id,
                    dosage=dosage,
                    duration=duration
                )
            prescriptions.append(prescription)
            idx += 1
        db.session.add_all(prescriptions)
        db.session.commit()
        flash('Visit recorded successfully.', 'success')
        return redirect(url_for('visit_summary', visit_id=visit.id))
    if form.diagnosis_id.data:
        diagnosis_name = DIAGNOSIS_LIST[form.diagnosis_id.data-1]
        suggested_prescriptions = DIAGNOSIS_PRESCRIPTIONS.get(diagnosis_name, [])
    return render_template('new_visit.html', form=form, medications=[{'id': m.id, 'name': m.name} for m in medications],
                           symptom_list=SYMPTOM_LIST, diagnosis_list=DIAGNOSIS_LIST, suggested_prescriptions=suggested_prescriptions,
                           visit_history=visit_history, selected_patient=selected_patient)

@app.route('/visit/<int:visit_id>')
@login_required
def visit_summary(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    return render_template('visit_summary.html', visit=visit)

if __name__ == '__main__':
    app.run(debug=True) 