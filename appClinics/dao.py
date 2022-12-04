from appClinics.models import Medicine, User, Staff
from appClinics import db
from flask_login import current_user
from sqlalchemy import func
import hashlib
import json


# emp_path = "data/medicine.json"


def load_medicine():
    return Medicine.query.all()


def load_user_attributes():
    return ["Usename", "Password", "Name", "Gender", "Address", "Role", "CCCD", "Phone", "Avatar", "Email"]


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


if __name__ == '__main__':
    # fileme = []
    from appClinics import app

    with app.app_context():
        # load_medicine()
        print(load_user_attributes())
        # for m in load_categories():
        #     e = {
        #         "name": m.name,
        #         "content": m.content,
        #         "unit": m.unit,
        #         "price": m.price
        #     }
        #     fileme.append(e)
        #     save_f_json(fileme, emp_path)
