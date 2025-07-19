# Clinic Management System

A modern, professional, doctor-only clinic management web application built with Flask, SQLite, SQLAlchemy, WTForms, and Bootstrap.

## Features
- **Doctor Login** (single doctor, secure session)
- **Patient Registration** (name, father's name, age, sex, contact)
- **Patient Search** (by name)
- **Edit/Delete Patients**
- **Record Clinical Visits**
  - Select patient
  - Enter symptoms (multi-select, with custom option)
  - Select diagnosis (dropdown, with custom option)
  - Add dynamic prescriptions (medicine, dosage, duration, with custom option)
- **View Visit History** (for each patient)
- **Printable Visit Summary** (professional format)
- **Dashboard Layout** (sidebar, topbar, responsive, minimal UI)
- **Demo Data** (doctor, patients, diagnoses, medications)

## Tech Stack
- **Backend:** Python, Flask, SQLAlchemy, SQLite
- **Frontend:** Bootstrap 5, custom CSS, Jinja2 templates
- **Forms:** WTForms

## Setup Instructions
1. **Clone the repository**
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Seed the database with demo data**
   ```bash
   python seed.py
   ```
5. **Run the app**
   ```bash
   python app.py
   ```
6. **Open in your browser:**
   - Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Default Doctor Credentials
- **Username:** `doctor`
- **Password:** `password`

## Database Structure
- **Doctor**: id, username, password_hash
- **Patient**: id, name, father_name, age, sex, contact
- **Diagnosis**: id, name
- **Medication**: id, name
- **Visit**: id, patient_id, doctor_id, diagnosis_id, symptoms, date
- **Prescription**: id, visit_id, medication_id, dosage, duration

## Demo Data
- 1 doctor account (see credentials above)
- 3 demo patients
- 6 common psychiatric diagnoses
- 6 example medications

## Usage Notes
- **Add unlimited patients** via the "Register Patient" page.
- **Edit or delete any patient** from the "Patients" page.
- **Record unlimited visits** for any patient. Each visit can have multiple symptoms, a diagnosis, and any number of prescriptions.
- **Visit history** is shown for each patient when recording a new visit.
- **All data is stored in `clinic.db` (SQLite)**. You can view/edit this with any SQLite browser.
- **Print visit summaries** for professional records.

## Customization
- All UI is minimal, professional, and responsive.
- To change branding, edit the `CLINIC_BRAND` dictionary in `app.py`.
- To add more demo data, edit `seed.py` and re-run it (this will reset the database).

## License
This project is for educational and demonstration purposes. 