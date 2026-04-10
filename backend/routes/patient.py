from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Patient, Doctor, Appointment, Department, Availability, Treatment

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    patient = Patient.query.filter_by(user_id=user_id).first()

    return {
        "name": patient.name,
        "contact":patient.contact
    }


@patient_bp.route('/doctors', methods=['GET'])
@jwt_required()
def get_doctors():
    query = request.args.get('q')

    doctors = Doctor.query

    if query:
        doctors = doctors.filter(
            (Doctor.name.contains(query)) |
            (Doctor.specialization.contains(query))
        )

    doctors = doctors.all()

    return [
        {
            "id": d.id,
            "name": d.name,
            "specialization": d.specialization
        } for d in doctors
    ]


@patient_bp.route('/departments')
@jwt_required()
def get_departments():
    depts = Department.query.all()
    return [{"id": d.id, "name": d.name} for d in depts]


@patient_bp.route('/appointments')
@jwt_required()
def get_appointments():
    user_id = get_jwt_identity()

    patient = Patient.query.filter_by(user_id=user_id).first()

    appointments = Appointment.query.filter_by(patient_id=patient.id).all()

    data = []
    for a in appointments:
        doctor = Doctor.query.get(a.doctor_id)
        dept = Department.query.get(doctor.department_id)

        data.append({
            "id": a.id,
            "doctor_name": doctor.name,
            "department": dept.name,
            "date": a.date,
            "time": a.time,
            "status":a.status
        })

    return data


@patient_bp.route('/department/<int:id>')
@jwt_required()
def get_department(id):
    dept = Department.query.get(id)

    return {
        "id": dept.id,
        "name": dept.name,
        "description": dept.description
    }


@patient_bp.route('/department/<int:id>/doctors')
@jwt_required()
def get_doctors_by_department(id):
    doctors = Doctor.query.filter_by(department_id=id).all()

    data = []
    for d in doctors:
        data.append({
            "id": d.id,
            "name": d.name,
            "specialization":d.specialization
        })

    return data


@patient_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    patient = Patient.query.filter_by(user_id=user_id).first()

    data = request.get_json()

    patient.name = data.get('name', patient.name)
    patient.contact = data.get('contact', patient.contact)

    db.session.commit()

    return {"message": "Profile updated"}


@patient_bp.route('/doctor/<int:id>/availability')
@jwt_required()
def get_doctor_availability(id):
    records = Availability.query.filter_by(doctor_id=id).all()

    return [
        {
            "date": r.date,
            "morning": r.morning_slot,
            "evening": r.evening_slot
        } for r in records
    ]


@patient_bp.route('/appointment', methods=['POST'])
@jwt_required()
def book_appointment():
    user_id = get_jwt_identity()
    patient = Patient.query.filter_by(user_id=user_id).first()

    data = request.get_json()

    time = "08:00-12:00" if data['slot'] == 'morning' else "04:00-09:00"

    appointment = Appointment(
        doctor_id=data['doctor_id'],
        patient_id=patient.id,
        date=data['date'],
        time=time,
        status="Upcoming"
    )

    db.session.add(appointment)
    db.session.commit()

    return {"message": "Booked"}


@patient_bp.route('/appointment/<int:id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_appointment(id):
    appointment = Appointment.query.get(id)
    appointment.status = "Cancelled"
    db.session.commit()

    return {"message": "Cancelled"}


@patient_bp.route('/history')
@jwt_required()
def get_patient_history():
    user_id = get_jwt_identity()
    patient = Patient.query.filter_by(user_id=user_id).first()

    appointments = Appointment.query.filter_by(
        patient_id=patient.id,
        status="Completed" 
    ).all()

    data = []

    for a in appointments:
        doctor = Doctor.query.get(a.doctor_id)
        dept = Department.query.get(doctor.department_id)

        treatment = Treatment.query.filter_by(appointment_id=a.id).first()

        data.append({
            "date": a.date,
            "doctor": doctor.name,
            "department": dept.name,
            "visit_type": treatment.visit_type if treatment else "",
            "tests_done": treatment.tests_done if treatment else "",
            "diagnosis": treatment.diagnosis if treatment else "",
            "prescription": treatment.prescription if treatment else "",
            "medicines": treatment.medicines if treatment else ""
        })

    return data