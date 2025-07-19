from app import app, db
from models import Doctor, Patient, Diagnosis, Medication
from werkzeug.security import generate_password_hash

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Add doctor
        doctor = Doctor(username='doctor', password_hash=generate_password_hash('password'))
        db.session.add(doctor)

        # Add patients
        patients = [
            Patient(name='Ali Khan', father_name='Ahmed Khan', age=30, sex='Male', contact='03001234567'),
            Patient(name='Sara Ahmed', father_name='Imran Ahmed', age=25, sex='Female', contact='03007654321'),
            Patient(name='Bilal Raza', father_name='Rashid Raza', age=40, sex='Male', contact='03111234567'),
        ]
        db.session.add_all(patients)

        # Add diagnoses
        diagnoses = [
            Diagnosis(name='Depression'),
            Diagnosis(name='Anxiety'),
            Diagnosis(name='Bipolar Disorder'),
            Diagnosis(name='Schizophrenia'),
            Diagnosis(name='Obsessive Compulsive Disorder'),
            Diagnosis(name='PTSD'),
        ]
        db.session.add_all(diagnoses)

        # Add medications
        medications = [
            Medication(name='Sertraline'),
            Medication(name='Fluoxetine'),
            Medication(name='Olanzapine'),
            Medication(name='Risperidone'),
            Medication(name='Lithium'),
            Medication(name='Diazepam'),
        ]
        db.session.add_all(medications)

        db.session.commit()
        print('Database seeded successfully.')

if __name__ == '__main__':
    seed() 