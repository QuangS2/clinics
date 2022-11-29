from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from appClinics import db, app
from enum import Enum as UserEnum
from enum import Enum as GenderEnum
from flask_login import UserMixin
from datetime import datetime


#
class UserRole(UserEnum):
    PATIENT = 1
    NURSE = 2
    DOCTOR = 3
    CASHIER = 4
    ADMIN = 5


class GenderRole(GenderEnum):
    FEMALE = 0
    MALE = 1


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel):
    __tablename__ = 'User'

    name = Column(String(50), nullable=False)
    gender = Column(Boolean(GenderEnum), default=GenderRole.MALE)
    address = Column(String(50), nullable=False)
    role = Column(Boolean(UserRole), default=UserRole.PATIENT)
    CCCD = Column(String(12), nullable=False)
    phone = Column(String(12), nullable=False)
    avatar = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class Mail(BaseModel):
    __tablename__ = 'Mail'
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    content = Column(String(50), nullable=False)


class Staff(BaseModel):
    __tablename__ = 'Staff'
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    salary = Column(Integer, nullable=False)


class Clinics(BaseModel):
    __tablename__ = 'Clinics'
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Appointment(BaseModel):
    __tablename__ = 'Appointment'
    patient_id = Column(Integer, ForeignKey(User.id), nullable=False)
    nurse_id = Column(Integer, ForeignKey(User.id), nullable=False)
    clinics_id = Column(Integer, ForeignKey(Clinics.id), nullable=False)
    date = Column(DateTime, nullable=True)


class MedicalReport(BaseModel):
    __tablename__ = 'MedicalReport'
    doctor_id = Column(Integer, ForeignKey(User.id), nullable=False)
    appointment_id = Column(Integer, ForeignKey(Appointment.id), nullable=False)
    symptom = Column(String(255), nullable=False)
    predict = Column(String(255), nullable=False)


class Medicine(BaseModel):
    __tablename__ = 'Medicine'
    name = Column(String(50), nullable=False)
    content = Column(String(50), nullable=False)
    unit = Column(String(20), nullable=False)
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Prescribe(BaseModel):
    __tablename__ = 'Prescribe'
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    medicalReport_id = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)
    amount = Column(Integer, nullable=False)
    userManual = Column(String(255), nullable=False)
# prod_tag = db.Table('prod_tag',
#                     Column('product_id', ForeignKey('product.id'), nullable=False, primary_key=True),
#                     Column('tag_id', ForeignKey('tag.id'), nullable=False, primary_key=True))
#
#
# class Product(BaseModel):
#     __tablename__ = 'product'
#
#     name = Column(String(50), nullable=False)
#     description = Column(Text)
#     price = Column(Float, default=0)
#     image = Column(String(100))
#     active = Column(Boolean, default=True)
#     # category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
#     tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
#                         backref=backref('products', lazy=True))
#     receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
#
#     def __str__(self):
#         return self.name
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

        # c1 = Category(name='Điện thoại')
        # c2 = Category(name='Máy tính bảng')
        # c3 = Category(name='Phụ kiện')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()

        # p1 = Product(name='Galaxy S22 Pro', description='Samsung, 128GB', price=25000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=1)
        # p2 = Product(name='Galaxy Fold 4', description='Samsung, 128GB', price=38000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg',
        #              category_id=1)
        # p3 = Product(name='Apple Watch S5', description='Apple, 32GB', price=18000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=3)
        # p4 = Product(name='Galaxy Tab S8', description='Samsung, 128GB', price=22000000,
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=2)
        # db.session.add_all([p1, p2, p3, p4])
        # db.session.commit()
