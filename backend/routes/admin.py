from flask import Blueprint, request, jsonify
from models import db, User, Doctor, Patient, Appointment, Department
from flask_jwt_extended import jwt_required, get_jwt

admin_bp = Blueprint('admin', __name__)


def is_admin():
    claims=get_jwt()
    return claims.get('role')=='admin'


@admin_bp.route('/doctor', methods=['POST'])
@jwt_required()
def add_doctor():
    if not is_admin():
        return {"message": "Unauthorized"}, 403

    data = request.get_json()

    user = User(
        username=data['username'],
        password=data['password'],
        role='doctor'
    )
    db.session.add(user)
    db.session.commit()

    doctor = Doctor(
        user_id=user.id,
        name=data['name'],
        department_id=data['department_id'],
        specialization=data['specialization'],
    )
    db.session.add(doctor)
    db.session.commit()

    return {"message": "Doctor created"}, 201


@admin_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    if not is_admin():
        return {"message": "Unauthorized"}, 403
    
    departments = Department.query.all()
    return [
        {
            "id": d.id,
            "name": d.name
        } for d in departments
    ]


@admin_bp.route('/doctor/<int:id>', methods=['GET'])
@jwt_required()
def get_doctor(id):
    if not is_admin():
        return {"message": "Unauthorized"}, 403
    
    doctor = Doctor.query.get(id)

    return {
        "id": doctor.id,
        "name": doctor.name,
        "specialization": doctor.specialization,
        "department_id": doctor.department_id,
    }


@admin_bp.route('/doctor/<int:id>', methods=['PUT'])
@jwt_required()
def update_doctor(id):
    if not is_admin():
        return {"message": "Unauthorized"}, 403
    
    doctor = Doctor.query.get(id)
    data = request.get_json()

    doctor.name = data.get('name', doctor.name)
    doctor.specialization = data.get('specialization', doctor.specialization)
    doctor.department_id = data.get('department_id', doctor.department_id)

    db.session.commit()

    return {"message": "Doctor updated"}


@admin_bp.route('/doctors/search', methods=['GET'])
@jwt_required()
def search_doctors():
    if not is_admin():
        return jsonify({'message': 'Unauthorized'}), 403

    query = request.args.get('q')

    doctors = Doctor.query
    if query:
        doctors=doctors.filter(
            (Doctor.name.contains(query)) |
            (Doctor.specialization.contains(query))
        )
    doctors=doctors.all()

    result = []
    for d in doctors:
        result.append({
            'id': d.id,
            'user_id':d.user_id,
            'name': d.name,
            'specialization': d.specialization,
            'is_blacklisted':d.user.is_blacklisted
        })

    return jsonify(result)


@admin_bp.route('/patients/search', methods=['GET'])
@jwt_required()
def search_patients():
    if not is_admin():
        return jsonify({'message': 'Unauthorized'}), 403

    query = request.args.get('q')

    patients = Patient.query
    if query:
        patients=patients.filter(
            (Patient.name.contains(query)) |
            (Patient.contact.contains(query))
        )
    patients=patients.all()

    result = []
    for p in patients:
        result.append({
            'id': p.id,
            'user_id':p.user_id,
            'name': p.name,
            'contact': p.contact,
            'is_blacklisted':p.user.is_blacklisted
        })

    return jsonify(result)


@admin_bp.route('/appointments', methods=['GET'])
@jwt_required()
def view_appointments():
    if not is_admin():
        return jsonify({'message': 'Unauthorized'}), 403

    appointments = Appointment.query.all()

    result = []
    for a in appointments:
        patient=Patient.query.get(a.patient_id)
        doctor=Doctor.query.get(a.doctor_id)
        result.append({
            'id': a.id,
            'doctor_id': a.doctor_id,
            'patient_id': a.patient_id,
            'patient_name':patient.name,
            'doctor_name':doctor.name,
            'date': a.date,
            'time': a.time,
            'status': a.status
        })

    return jsonify(result)


@admin_bp.route('/delete/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    if not is_admin():
        return {"message": "Unauthorized"}, 403
    
    user = User.query.get(id)

    if not user:
        return {"message": "User not found"}, 404

    doctor = Doctor.query.filter_by(user_id=id).first()
    patient = Patient.query.filter_by(user_id=id).first()

    if doctor:
        if Appointment.query.filter_by(doctor_id=doctor.id).first():
            return {"message": "Cannot delete doctor with appointments"}, 400

    if patient:
        if Appointment.query.filter_by(patient_id=patient.id).first():
            return {"message": "Cannot delete patient with appointments"}, 400

    if doctor:
        db.session.delete(doctor)
    
    if patient:
        db.session.delete(patient)

    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted"}


@admin_bp.route('/blacklist/user/<int:id>', methods=['PUT'])
@jwt_required()
def blacklist_user(id):
    if not is_admin():
        return {"message": "Unauthorized"}, 403
    
    user = User.query.get(id)

    if not user:
        return {"message": "User not found"}, 404

    user.is_blacklisted = True
    db.session.commit()

    return {"message": "User blacklisted"}


@admin_bp.route('/unblacklist/user/<int:id>', methods=['PUT'])
@jwt_required()
def unblacklist_user(id):
    if not is_admin():
        return {"message": "Unauthorized"}, 403
    
    user = User.query.get(id)

    if not user:
        return {"message": "User not found"}, 404

    user.is_blacklisted = False
    db.session.commit()

    return {"message": "User unblacklisted"}