from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from appClinics import db, app
from enum import Enum as BaseEnum
import json
# from enum import Enum as GenderEnum
# from enum import Enum as ActionEnum
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


class User(BaseModel):
    __tablename__ = 'User'

    name = Column(String(50), nullable=False)
    gender = Column(Enum(GenderRole), default=GenderRole.MALE)
    address = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    CCCD = Column(String(12), nullable=False)
    phone = Column(String(12), nullable=False)
    avatar = Column(String(100), nullable=False)

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
    nurse_id = Column(Integer, ForeignKey(User.id), nullable=False)
    clinics_id = Column(Integer, ForeignKey(Clinics.id), nullable=False)
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
    price = Column(Integer,nullable=False)
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


# prod_tag = db.Table('prod_tag',
#                     Column('product_id', ForeignKey('product.id'), nullable=False, primary_key=True),
#                     Column('tag_id', ForeignKey('tag.id'), nullable=False, primary_key=True))
#
#

#
#
# class Tag(BaseModel):
#     name = Column(String(50), nullable=False, unique=True)
#
#     def __str__(self):
#         return self.name
#
#
# class User (BaseModel, UserMixin):
#     name = Column(String(50), nullable=False)
#     username = Column(String(50), nullable=False, unique=True)
#     password = Column(String(50), nullable=False)
#     avatar = Column(String(100), nullable=False)
#     active = Column(Boolean, default=True)
#     user_role = Column(Enum(UserRole), default=UserRole.USER)
#     receipts = relationship('Receipt', backref='user', lazy=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Receipt(BaseModel):
#     created_date = Column(DateTime, default=datetime.now())
#     user_id = Column(Integer, ForeignKey(User.id), nullable=False)
#     details = relationship('ReceiptDetails', backref='receipt', lazy=True)
#
#
# class ReceiptDetails(BaseModel):
#     quantity = Column(Integer, default=0)
#     price = Column(Float, default=0)
#     product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
#     receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # import hashlib
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u = User(name='Thanh', username='admin', password=password, user_role=UserRole.ADMIN,
        #          avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # db.session.add(u)
        # db.session.commit()


        # with open(f'data/medicine.json', encoding='utf-8') as f:
        # #     datas = json.load(f)['result']['items']
        #     datas = json.load(f)
        #     for item in datas:
        #         # if len(item['hoatChat']) < 255 and len(item['tenThuoc']) < 75 and len(item['donViTinh']) < 50:
        #         #     m = Medicine(name = item['tenThuoc'],
        #         #                  unit = item['donViTinh'],
        #         #                  price = item['giaBanBuon'],
        #         #                  content = item['hoatChat'])
        #         m = Medicine(name=item['name'],
        #          unit=item['unit'],
        #          price=item['price'],
        #          content=item['content'])
        #         db.session.add(m)
        #         db.session.commit()



