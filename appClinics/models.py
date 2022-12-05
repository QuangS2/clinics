from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum, DateTime, DATE
from sqlalchemy.orm import relationship, backref
from appClinics import db, app
from enum import Enum as BaseEnum
import json
from flask_login import UserMixin
from datetime import datetime


#
class UserRole(BaseEnum):
    PATIENT = 1
    NURSE = 2
    DOCTOR = 3
    CASHIER = 4
    ADMIN = 5


class GenderRole(BaseEnum):
    FEMALE = 0
    MALE = 1
    OTHER = 2


class ActionRole(BaseEnum):
    MEDICINE = 1
    REGULATIONS = 2


class ActionMedicineRole(BaseEnum):
    ADD = 1
    CHANGE = 2
    DELETE = 3
    FOUND = 4


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    __tablename__ = 'User'

    name = Column(String(50), nullable=False)
    gender = Column(Enum(GenderRole), default=GenderRole.MALE)
    birthday = Column(DATE, nullable=False)
    address = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PATIENT)
    CCCD = Column(String(12), nullable=False)
    phone = Column(String(12), nullable=False)
    avatar = Column(String(100), default="https://res.cloudinary.com/dpwzlm56r/image/upload/v1668053235/fqgebe03qujrypsdcni5.jpg")

    def __str__(self):
        return self.name


class Mail(BaseModel):
    __tablename__ = 'Mail'
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    content = Column(String(50), nullable=False)


class Staff(BaseModel):  # nhanvien
    __tablename__ = 'Staff'
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    salary = Column(Integer, nullable=False)


class Clinics(BaseModel):  # phongkham
    __tablename__ = 'Clinics'
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Appointment(BaseModel):  # lichkham
    __tablename__ = 'Appointment'
    patient_id = Column(Integer, ForeignKey(User.id), nullable=False)
    nurse_id = Column(Integer, ForeignKey(User.id), nullable=True)
    clinics_id = Column(Integer, ForeignKey(Clinics.id), default=1)
    date = Column(DateTime, nullable=True)


class MedicalReport(BaseModel):  # PhieuKham
    __tablename__ = 'MedicalReport'
    doctor_id = Column(Integer, ForeignKey(User.id), nullable=False)
    appointment_id = Column(Integer, ForeignKey(Appointment.id), nullable=False)
    symptom = Column(String(255), nullable=False)
    predict = Column(String(255), nullable=False)


class Medicine(BaseModel):  # thuoc
    __tablename__ = 'Medicine'
    name = Column(String(75), nullable=False)
    content = Column(String(255), nullable=False)
    unit = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Prescribe(BaseModel):  # donThuoc
    __tablename__ = 'Prescribe'
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    medicalReport_id = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)
    amount = Column(Integer, nullable=False)
    userManual = Column(String(255), nullable=False)


class Bill(BaseModel):  # hoaDon
    __tablename__ = 'Bill'
    medicalReport_id = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)
    cashier_id = Column(Integer, ForeignKey(User.id), nullable=False)
    medicalExpenses = Column(Integer, nullable=False)
    medicineExpenses = Column(Integer, nullable=False)


class Action(BaseModel):  # quantri
    __tablename__ = 'Action'
    admin_id = Column(Integer, ForeignKey(User.id), nullable=False)
    date = Column(DateTime, nullable=False)
    type = Column(Enum(ActionRole), nullable=False)


class ManageMedicine(BaseModel):  # quantriThuoc
    __tablename__ = 'ManageMedicine'
    action_id = Column(Integer, ForeignKey(Action.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    action = Column(Enum(ActionMedicineRole), nullable=False)


class Regulations(BaseModel):  # quyDinh
    __tablename__ = 'Regulations'
    patientAmount = Column(Integer, nullable=False)
    medicalExpenses = Column(Integer, nullable=False)


class ManageRegulation(BaseModel):  # quanLyQuyDinh
    __tablename__ = 'ManageRegulation'
    action_id = Column(Integer, ForeignKey(Action.id), nullable=False)
    regulation_id = Column(Integer, ForeignKey(Regulations.id), nullable=False)
    content = Column(String(255), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #
        import hashlib

        # u = User(name='Nhung', gender=GenderRole.OTHER, birthday="2002/9/6",address='DH babon', role=UserRole.CASHIER,\
        #          CCCD="123452789",phone="35012581")
        #
        # db.session.add(u)
        # db.session.commit()
        u = User.query.filter(User.CCCD.__eq__("123452789")).first()
        # print(u.id)
        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        staf = Staff(user_id=u.id, username="Nhung", password=password,salary = 3500001)
        db.session.add(staf)
        db.session.commit()

        # with open(f'data/medicine.json', encoding='utf-8') as f:
        #     # datas = json.load(f)['result']['items']
        #     datas = json.load(f)
        #     for item in datas:
        #         # if len(item['hoatChat']) < 255 and len(item['tenThuoc']) < 75 and len(item['donViTinh']) < 50:
        #         #     m = Medicine(name = item['tenThuoc'],
        #         #                  unit = item['donViTinh'],
        #         #                  price = item['giaBanBuon'],
        #         #                  content = item['hoatChat'])
        #         m = Medicine(name=item['name'],
        #                      unit=item['unit'],
        #                      price=item['price'],
        #                      content=item['content'])
        #         db.session.add(m)
        #         db.session.commit()
