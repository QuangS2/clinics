import datetime

from appClinics.models import Medicine, User, Staff, GenderRole, Appointment, UserRole
from appClinics import db
from flask_login import current_user, utils
from sqlalchemy import func, or_
import hashlib
import json

emp_path = "data/medicine.json"


def load_medicine():
    return Medicine.query.all()


# user
def load_user_attributes():
    return {
        "name": "Họ và tên",
        "gender": "Giới tính",
        "birthday": "Ngày sinh",
        "address": "Địa chỉ",
        "CCCD": "CMND/CCCD",
        "phone": "Số điện thoại"
    }


def add_data_user(data_user):
    u = User(name=data_user['name'], gender=GenderRole[data_user['gender']], birthday=data_user['birthday'], \
             address=data_user['address'], \
             CCCD=data_user['CCCD'], phone=data_user['phone'])
    db.session.add(u)
    return db.session.commit()


def auth_user(username, password):

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    staff = Staff.query.filter(Staff.username.__eq__(username.strip()),
                               Staff.password.__eq__(password)).first()

    if staff:
        user_success = True
        return User.query.get(staff.user_id)

    return staff


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_contain(kw):
    return User.query.filter(User.name.like('%' + kw + '%')).all()


def reverse_legit_user(user_id):
    user = get_user_by_id(user_id);
    user.legit = not user.legit
    db.session.add(user)
    return db.session.commit()


# apm
def get_apm_user(kw):
    apms = load_list_apm(datetime.date.today())
    patients = []
    if kw == "ALL": kw = ""
    if kw.isdigit():
        apm = Appointment.query.filter(Appointment.id.__eq__(int(kw))).first();
        patients.append(get_user_by_id(apm.patient_id))

    else:
        for apm in apms:
            u = get_user_by_id(apm.patient_id)
            if kw.lower() in u.name.lower():
                patients.append(u)
    return patients


def get_apm_legit():
    apms_legit = []
    list_apm = load_list_apm(None)
    for apm in list_apm:
        u = get_user_by_id(apm.patient_id)
        if u.legit == True:
            apms_legit.append(apm)
    return apms_legit


def get_apm_date(user_id, date):
    return Appointment.query.filter(Appointment.patient_id.__eq__(int(user_id)),
                                    Appointment.date.__eq__(date)).first()


def set_apm(date, amount):
    apms = get_apm_legit()
    for idx in range(amount):
        apms[idx].date = date
        apms[idx].nurse_id = current_user.id
        db.session.add(apms[idx])
    return db.session.commit()


def load_list_apm(date):
    return Appointment.query.filter(Appointment.date.__eq__(date)).all()


def get_apm_by_id(id):
    return


def register_appointment(data_user):
    u = User.query.filter(User.CCCD.__eq__(data_user['CCCD'])).first()
    apm = Appointment(patient_id=u.id)
    db.session.add(apm)
    return db.session.commit()


# medicine
def get_medicine_by_kw(kw):
    if kw == "ALL": kw = ""
    return Medicine.query.filter(or_(Medicine.name.like('%' + kw + '%'),
                                     Medicine.content.like('%' + kw + '%')
                                     )).all()


if __name__ == '__main__':
    # fileme = []
    from appClinics import app

    with app.app_context():
        load_medicine()
        # data = {
        #     "gender":"MALE"
        # }
        # print(GenderRole[data['gender']].name)
        # listapm = load_list_apm()
        # for item in listapm:
        #     print(item.patient_id)
        # dis_legit_user(9)
        # u = get_user_by_id(8)
        # print(u.legit)
        # print(u.birthday.year)
        # datetime.date.year
        # print(load_user_attributes().items())
        # print(get_apm_legit())
        # print(get_apm_user("2"))
        # print(get_apm_date("5",datetime.date.today()))
        # print(datetime.date.today())

        print(get_medicine_by_kw("ALL"))
