from flask import Blueprint,request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, Department, Appointment, Doctor, Patient, Treatment, Availability

doctor_bp = Blueprint('doctor', __name__)

def is_doctor():
    claims=get_jwt()
    return claims.get('role')=='doctor'

@doctor_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    user_id = get_jwt_identity()
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    if not doctor:
        return {"message": "Doctor not found"}, 404

    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()

    result = []
    for a in appointments:
        patient = Patient.query.get(a.patient_id)

        result.append({
            "id": a.id,
            "patient_id":a.patient_id,
            "patient_name": patient.name,
            "date": a.date,
            "time": a.time,
            "status": a.status
        })

    return result

@doctor_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_doctor_profile():
    if not is_doctor():
        return {"message": "Unauthorized"}, 403

    user_id = get_jwt_identity()

    doctor = Doctor.query.filter_by(user_id=user_id).first()

    return {
        "name": doctor.name
    }


@doctor_bp.route('/patients', methods=['GET'])
@jwt_required()
def get_patients():
    if not is_doctor():
        return {"message": "Unauthorized"}, 403

    user_id = get_jwt_identity()
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patient_ids = list(set([a.patient_id for a in appointments]))
    patients = Patient.query.filter(Patient.id.in_(patient_ids)).all()

    return [{"id": p.id, "name": p.name} for p in patients]


@doctor_bp.route('/appointment/<int:id>', methods=['GET'])
@jwt_required()
def get_appointment(id):
    claims = get_jwt()
    role = claims.get('role')

    if role not in ['doctor', 'admin']:
        return {"message": "Unauthorized"}, 403

    a = Appointment.query.get(id)
    patient = Patient.query.get(a.patient_id)

    return {
        "patient_name": patient.name
    }


@doctor_bp.route('/treatment/<int:id>', methods=['GET'])
@jwt_required()
def get_treatment(id):
    claims = get_jwt()
    role = claims.get('role')

    if role not in ['doctor', 'admin']:
        return {"message": "Unauthorized"}, 403

    treatment = Treatment.query.filter_by(appointment_id=id).first()

    if not treatment:
        return {}, 200

    return {
        "visit_type": treatment.visit_type,
        "tests": treatment.tests_done,
        "diagnosis": treatment.diagnosis,
        "prescription": treatment.prescription,
        "medicines": treatment.medicines
    }


@doctor_bp.route('/treatment/<int:id>', methods=['POST'])
@jwt_required()
def add_or_update_treatment(id):
    if not is_doctor():
        return {"message": "Unauthorized"}, 403

    data = request.get_json()

    treatment = Treatment.query.filter_by(appointment_id=id).first()

    if treatment:
        treatment.visit_type = data.get('visit_type')
        treatment.tests_done = data.get('tests')
        treatment.diagnosis = data.get('diagnosis')
        treatment.prescription = data.get('prescription')
        treatment.medicines = data.get('medicines')

    else:
        treatment = Treatment(
            appointment_id=id,
            visit_type=data.get('visit_type'),
            tests_done=data.get('tests'),
            diagnosis=data.get('diagnosis'),
            prescription=data.get('prescription'),
            medicines=data.get('medicines')
        )
        db.session.add(treatment)

    appointment = Appointment.query.get(id)
    appointment.status = "Completed"

    db.session.commit()

    return {"message": "Saved"}


@doctor_bp.route('/patient-history/<int:id>', methods=['GET'])
@jwt_required()
def get_patient_history(id):
    claims = get_jwt()
    role = claims.get('role')

    if role not in ['doctor', 'admin']:
        return {"message": "Unauthorized"}, 403

    patient = Patient.query.get(id)

    appointments = Appointment.query.filter(Appointment.patient_id==id).all()

    result = []

    for a in appointments:
        treatment = Treatment.query.filter_by(appointment_id=a.id).first()

        if treatment:
            doctor = Doctor.query.get(a.doctor_id)
            dept = Department.query.get(doctor.department_id)

            result.append({
                "id": treatment.id,
                "date": a.date,
                "diagnosis": treatment.diagnosis,
                "prescription": treatment.prescription,
                "tests": treatment.tests_done,
                "medicines": treatment.medicines,
                "doctor_name": doctor.name,   
                "department": dept.name if dept else ""
            })

    return {
        "patient_name": patient.name,   
        "history": result
    }


@doctor_bp.route('/availability', methods=['GET'])
@jwt_required()
def get_availability():
    if not is_doctor():
        return {"message": "Unauthorized"}, 403

    user_id = get_jwt_identity()
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    records = Availability.query.filter_by(doctor_id=doctor.id).all()

    return [
        {
            "date": r.date,
            "morning": r.morning_slot,
            "evening": r.evening_slot
        } for r in records
    ]


@doctor_bp.route('/availability', methods=['POST'])
@jwt_required()
def save_availability():
    if not is_doctor():
        return {"message": "Unauthorized"}, 403

    user_id = get_jwt_identity()
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    data = request.get_json()

    Availability.query.filter_by(doctor_id=doctor.id).delete()

    for day in data:
        record = Availability(
            doctor_id=doctor.id,
            date=day['date'],
            morning_slot=day['morning'],
            evening_slot=day['evening']
        )
        db.session.add(record)

    db.session.commit()

    return {"message": "Saved"}


@doctor_bp.route('/appointment/<int:id>/complete', methods=['PUT'])
@jwt_required()
def complete_appointment(id):
    a = Appointment.query.get(id)
    a.status = "Completed"
    db.session.commit()
    return {"message": "Completed"}


@doctor_bp.route('/appointment/<int:id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_appointment(id):
    a = Appointment.query.get(id)
    a.status = "Cancelled"
    db.session.commit()
    return {"message": "Cancelled"}