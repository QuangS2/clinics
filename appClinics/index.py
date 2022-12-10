from flask import render_template, request, redirect, url_for
from appClinics import app, dao, login
from flask_login import login_user, logout_user
from appClinics.decorator import annonynous_user, nurse_user

@app.route("/")
def index():
    # categories = dao.load_categories()
    # products = dao.load_products(category_id=request.args.get('category_id'))
    categories = 3
    products = 4
    return render_template('index.html', categories=categories, products=products)


@app.route("/appointment")
def appointment():
    u = request.args.get('success')         #xử lý đúng
    u2 =  request.args.get('fail')          #xử lý sai
    print("bien trang thai", u)


    user_atb = dao.load_user_attributes()
    return render_template('appointment.html', user_atb=user_atb, success = u, fail = u2)
@app.route("/listapm")
@nurse_user
def list_apm():
    list = dao.load_list_apm()
    users =[]
    user_atb = dao.load_user_attributes()
    for item in list:
        users.append(dao.get_user_by_id(item.patient_id))
    return render_template('listapm.html', list = list, users = users, user_atb=user_atb)




@app.route("/login")
@annonynous_user
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['post'])
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get('next')
            return redirect(n if n else '/')

    return render_template('login.html')
@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')
@app.route('/appointment', methods=['post'])
def register_appointment():
    if request.method == 'POST':
        try:
            success = None          #xử lý đúng
            fail = None             #xử lý sai
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
        except Exception as ex:
            print(ex)
            fail = False        #xử lý sai
            return redirect(url_for('appointment', fail=fail))      #xử lý sai

    return redirect( url_for('appointment', success = success))     #xử lý đúng




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
