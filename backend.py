from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SQLite Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pediatric_care.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Patient Model
class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    chronic_condition = db.Column(db.String(255), nullable=False)
    medical_history = db.Column(db.Text)  # Store as JSON string
    appointments = db.Column(db.Text)  # Store as JSON string
    medication_schedule = db.Column(db.Text)  # Store as JSON string
    emergency_contact = db.Column(db.Text)  # Store as JSON string

# Initialize the database
with app.app_context():
    db.create_all()

# Routes

# Get all patients
@app.route('/api/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{
        'patient_id': p.patient_id,
        'name': p.name,
        'age': p.age,
        'chronic_condition': p.chronic_condition,
        'medical_history': p.medical_history,
        'appointments': p.appointments,
        'medication_schedule': p.medication_schedule,
        'emergency_contact': p.emergency_contact
    } for p in patients])

# Add a new patient
@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    new_patient = Patient(
        name=data['name'],
        age=data['age'],
        chronic_condition=data['chronic_condition'],
        medical_history=data['medical_history'],
        appointments=data['appointments'],
        medication_schedule=data['medication_schedule'],
        emergency_contact=data['emergency_contact']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'Patient added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
