from appClinics import app, dao, login, controllers

app.add_url_rule('/', 'index', controllers.index)
# login logout
app.add_url_rule('/login', 'login', controllers.login_page)
app.add_url_rule('/login', 'login-user', controllers.login_my_user, methods=['post'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/login-admin', 'login-admin', controllers.login_admin, methods=['post'])
# appoinment dk kham
app.add_url_rule('/appointment', 'register-appointment', controllers.register_appointment, methods=['post'])
app.add_url_rule('/appointment', 'appointment', controllers.appointment)

# apms
app.add_url_rule('/apms', 'apms', controllers.apms)
app.add_url_rule('/apms', 'update-apms', controllers.update_legit, methods=['post'])
app.add_url_rule('/apms/create', 'creat-apms', controllers.set_date_apm, methods=['post'])

# doctor
app.add_url_rule('/medicalrp', 'medicalrp', controllers.medicalrp)
# medicalrp

app.add_url_rule('/medicine', 'medicine', controllers.medicine)

app.add_url_rule('/api/patient/<string:kw>', 'get-patients', controllers.get_patients)
app.add_url_rule('//api/user/<int:id>', 'get-user', controllers.get_user)

# medicine
app.add_url_rule('/api/medicines/<string:kw>', 'get_medicine_kw', controllers.get_medicines_by_kw)

app.add_url_rule('/api/medicine/<int:id>', 'get_medicine_id', controllers.get_medicine_by_id)

# rp
app.add_url_rule('/api/report/<int:apm_id>', 'get-report', controllers.getRp, methods=['put'])
app.add_url_rule('/api/report/add_medicine', 'add-medicine', controllers.addMedicine, methods=['post'])
app.add_url_rule('/api/report/<int:rp_id>', 'complete-report', controllers.completeRp, methods=['post'])

# prescribe
app.add_url_rule('/api/prescribe/<int:pres_id>', 'del-Prescribe', controllers.deletePrescribe, methods=['delete'])

app.add_url_rule('/price', 'price', controllers.price)

app.add_url_rule('/bill', 'bill', controllers.billCas)
app.add_url_rule('/generalExamination', 'generalExamination', controllers.generalExamination)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
