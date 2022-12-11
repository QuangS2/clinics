import datetime

from flask import render_template, request, redirect, url_for, jsonify

from appClinics import app, dao, login, utils
from flask_login import login_user, logout_user
from appClinics.decorator import annonynous_user, nurse_user, doctor_user

@app.route("/")
def index():
    # categories = dao.load_categories()
    # products = dao.load_products(category_id=request.args.get('category_id'))
    # if dao.current_user.is_authenticated:
    #     if dao.current_user.role == dao.UserRole.NURSE:
    #         return redirect('/nurse')
    return render_template('index.html')




#login logout
@app.route("/login")
@annonynous_user
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['post'])
def login_my_user():

    check = False
    if request.method == 'POST':


        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/',)

    return render_template('login.html', check = check)
@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


#appoinment dk kham



@app.route('/appointment', methods=['post'])
def register_appointment():
    if request.method == 'POST':
        try:
            # success = None          #xử lý đúng
            # fail = None             #xử lý sai
            user = {
                'name' : request.form['name'],
            'gender' : request.form['gender'],
            'birthday' : request.form['birthday'],
            'address' : request.form['address'],
            'CCCD' : request.form['CCCD'],
            'phone' : request.form['phone']
            }
            dao.add_data_user(user)
            dao.register_appointment(user)

            success = True      #xử lý đúng
            return redirect(url_for('appointment', success=success))  # xử lý đúng
        except Exception as ex:
            print(ex)
            fail = False        #xử lý sai
            return redirect(url_for('appointment', fail=fail))      #xử lý sai


@app.route("/appointment")
def appointment():
    u = request.args.get('success')         #xử lý đúng
    u2 =  request.args.get('fail')          #xử lý sai
    # print("bien trang thai", u)


    user_atb = dao.load_user_attributes()
    return render_template('appointment.html', user_atb=user_atb, success = u, fail = u2)


#apms
@app.route("/apms")
@nurse_user
def apms():
    list = dao.load_list_apm(None)
    users = []
    user_atb = dao.load_user_attributes()
    date = datetime.date.today()
    for item in list:
        users.append(dao.get_user_by_id(item.patient_id))
    return render_template('nurse.html', list=list, users=users, user_atb=user_atb, \
                           date=date, site = 'apms')


@app.route('/apms', methods=['post'])
def update_legit():
    for user_id in request.form.getlist('data_fake'):
        dao.reverse_legit_user(user_id)
    # print(request.form['data_fake'])
    return redirect("/apms")


@app.route('/apms/create', methods=['post'])
def set_date_apm():
    date = request.form.getlist('date_apm')
    amount = request.form.getlist('patient_amount')
    dao.set_apm(date,int(amount[0]))
    # print(date,int(amount[0]))
    return redirect("/apms")
#doctor
#medicalrp
@app.route("/medicalrp")
@doctor_user
def medicalrp():
    return render_template('doctor.html', site = 'medicalrp')
@app.route("/medicine")
@doctor_user
def medicine():
    return render_template('doctor.html', site = 'medicine')


@app.route("/api/patient/<string:kw>")
#js api to repl json
def get_patients(kw): # come to apm or user to  get user data
    patients = dao.get_apm_user(kw)
    # print(users)
    patientsJson =[]
    for p in patients:
        patientsJson.append({
            "user_id" : p.id,
            "apm_id": dao.get_apm_date(p.id,datetime.date.today()).id,
            "user_data": utils.jsonUser(dao.get_user_by_id(p.id))
        })

    return jsonify(patientsJson)
@app.route("/api/user/<int:id>")
def get_user(id):
    return jsonify(utils.jsonUser(dao.get_user_by_id(id)))

#medicine
@app.route("/api/medicine/<string:kw>")
def get_medicine_by_kw(kw):
    medicines = dao.get_medicine_by_kw(kw)
    rsJson = []
    for m in medicines:
        rsJson.append({
            "name" : m.name,
            "unit" : m.unit,
            "price": m.price
        })
    return jsonify(rsJson)
@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/generalExamination")
def generalExamination():
    return render_template('generalExamination.html')

@app.route("/price")
def price():
    return render_template('price.html')

if __name__ == '__main__':
    app.run(debug=True)
