from appClinics.models import Medicine,User
from appClinics import db
from flask_login import current_user
from sqlalchemy import func
import json

emp_path = "data/medicine.json"


def load_medicine():
    return Medicine.query.all()

def load_user_attributes():
    return ["Usename","Password","Name","Gender","Address","Role","CCCD","Phone","Avatar", "Email"]

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
    fileme = []
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

