from flask_login import login_user, logout_user
from appClinics.decorator import annonynous_user, nurse_user, doctor_user, cashier_user
import datetime
from appClinics import app, dao, utils, admin
from flask import render_template, request, redirect, url_for, jsonify


def index():
    return render_template('index.html')


@annonynous_user
def login_page():
    return render_template('login.html')


def login_my_user():
    check = False
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/', )

    return render_template('login.html', check=check)


def logout_my_user():
    logout_user()
    return redirect('/login')


def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


def register_appointment():
    if request.method == 'POST':
        try:
            # success = None          #xử lý đúng
            # fail = None             #xử lý sai
            user = {
                'name': request.form['name'],
                'gender': request.form['gender'],
                'birthday': request.form['birthday'],
                'address': request.form['address'],
                'CCCD': request.form['CCCD'],
                'phone': request.form['phone']
            }

            dao.register_appointment(dao.add_data_user(user))
            success = True  # xử lý đúng
            return redirect(url_for('appointment', success=success))  # xử lý đúng
        except Exception as ex:
            print(ex)
            fail = False  # xử lý sai
            return redirect(url_for('appointment', fail=fail))  # xử lý sai


@app.route("/appointment")
def appointment():
    u = request.args.get('success')  # xử lý đúng
    u2 = request.args.get('fail')  # xử lý sai
    # print("bien trang thai", u)

    user_atb = dao.load_user_attributes()
    return render_template('appointment.html', user_atb=user_atb, success=u, fail=u2)


@nurse_user
def apms():
    apms = dao.load_list_apm(None)
    users = []
    user_atb = dao.load_user_attributes()
    date = datetime.date.today()
    for apm in apms:
        users.append(dao.get_user_by_id(apm.patient_id))
    return render_template('nurse.html', users=users, user_atb=user_atb, \
                           date=date, site='apms')


def update_legit():
    for user_id in request.form.getlist('data_fake'):
        dao.reverse_legit_user(user_id)
    # print(request.form['data_fake'])
    return redirect("/apms")


def set_date_apm():
    date = request.form.getlist('date_apm')
    amount = request.form.getlist('patient_amount')
    dao.set_apm(date, int(amount[0]))

    return redirect("/apms")


@doctor_user
def medicalrp():
    return render_template('doctor.html', site='medicalrp')


@doctor_user
def medicine():
    return render_template('doctor.html', site='medicine')


def get_patients(kw):  # come to apm or user to  get user data
    patients = dao.get_apm_user(kw)
    # print(users)
    patientsJson = []
    for p in patients:
        patientsJson.append({
            "user_id": p.id,
            "apm_id": dao.get_apm_date(p.id, datetime.date.today()).id,
            "user_data": utils.jsonUser(dao.get_user_by_id(p.id))
        })

    return jsonify(patientsJson)


def get_user(id):
    return jsonify(utils.jsonUser(dao.get_user_by_id(id)))


def get_medicines_by_kw(kw):
    medicines = dao.get_medicines_by_kw(kw)
    rsJson = []
    for m in medicines:
        rsJson.append({
            "id": m.id,
            "name": m.name,
            "unit": m.unit,
            "price": m.price
        })
    return jsonify(rsJson)


def get_medicine_by_id(id):
    m = dao.get_medicine_by_id(id)
    return jsonify({
        "id": m.id,
        "name": m.name,
        "unit": m.unit,
        "price": m.price
    })


def getRp(apm_id):
    apm = dao.get_apm_by_id(apm_id)
    user = dao.get_user_by_id(apm.patient_id)
    data = {
        "date": apm.date,
        "patient": utils.jsonUser(user),
        "doctor_id": dao.current_user.id,
        "appointment_id": apm_id,
        "symptom": "",
        "predict": "",
        "active": False
    }
    rp = dao.get_medicine_rp(apm_id)
    if rp == None:
        rp = dao.create_medicine_rp(data)
    else:
        data['doctor_id'] = rp.doctor_id
        data['symptom'] = rp.symptom
        data['predict'] = rp.predict
        data['active'] = rp.active
    data['id'] = rp.id
    prescribes = dao.get_prescribe(rp.id);
    jsPress = []
    for pr in prescribes:
        medicine = dao.get_medicine_by_id(pr.medicine_id)
        rs = utils.Prescribe(pr);
        rs['medicine'] = utils.Medicine(medicine)
        jsPress.append(rs)
    data['prescribes'] = jsPress
    return jsonify(data)


def addMedicine():
    data = request.json
    medicine = dao.get_medicine_by_id(data['medicine_id'])
    pr = dao.create_prescribe(data['rp_id'], data['medicine_id'])
    rs = utils.Prescribe(pr);
    rs['medicine'] = utils.Medicine(medicine)
    return jsonify(rs)


def completeRp(rp_id):
    rs = dao.completeRp(rp_id)

    return jsonify({
        "result": rs
    })


def deletePrescribe(pres_id):
    rs = dao.delete_prescribe(pres_id)
    return jsonify({
        "result": "success"
    })


def price():
    return render_template('price.html')


@cashier_user
def billCas():
    return render_template('cashier.html', site='bill')


def generalExamination():
    return render_template('generalExamination.html')
