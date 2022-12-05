from appClinics.models import Medicine, User, Staff, GenderRole, Appointment
from appClinics import db
from flask_login import current_user
from sqlalchemy import func
import hashlib
import json


# emp_path = "data/medicine.json"


def load_medicine():
    return Medicine.query.all()


def load_user_attributes():
    return {
        "name":"Họ và tên",
        "gender" : "Giới tính",
        "birthday":"Ngày sinh",
        "address":"Địa chỉ",
        "CCCD" : "CMND/CCCD",
        "phone":"Số điện thoại"
    }
def add_data_user(data_user):

    u = User(name=data_user['name'], gender=GenderRole[data_user['gender']], birthday=data_user['birthday'],\
             address=data_user['address'], \
             CCCD=data_user['CCCD'], phone=data_user['phone'])
    db.session.add(u)
    return    db.session.commit()
def register_appointment(data_user):
    u = User.query.filter(User.CCCD.__eq__(data_user['CCCD'])).first()
    apm = Appointment(patient_id=u.id)
    db.session.add(apm)
    return db.session.commit()
def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    staff = Staff.query.filter(Staff.username.__eq__(username.strip()),
                               Staff.password.__eq__(password)).first()

    if staff:
        return User.query.get(staff.user_id)
    return staff


def get_user_by_id(user_id):
    return User.query.get(user_id)


# def load_f_json(file_path):
#     if file_path is not None:
#         with open(file_path, encoding="utf-8") as f:
#             return json.load(f)
#
#
# def save_f_json(json_list, file_path):
#     with open(file_path, encoding="utf-8", mode="w") as f:
#         json.dump(json_list, f, ensure_ascii=False, indent=True)
def load_list_apm():
    return Appointment.query.filter(Appointment.date.__eq__(None)).all()

if __name__ == '__main__':
    # fileme = []
    from appClinics import app

    with app.app_context():
        # load_medicine()
        # data = {
        #     "gender":"MALE"
        # }
        # print(GenderRole[data['gender']].name)
        listapm = load_list_apm()
        for item in listapm:
            print(item.patient_id)
        # print(load_user_attributes().items())
        # for m in load_categories():
        #     e = {
        #         "name": m.name,
        #         "content": m.content,
        #         "unit": m.unit,
        #         "price": m.price
        #     }
        #     fileme.append(e)
        #     save_f_json(fileme, emp_path)
