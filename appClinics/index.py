from flask import render_template, request
from appClinics import app, dao


@app.route("/")
def index():
    # categories = dao.load_categories()
    # products = dao.load_products(category_id=request.args.get('category_id'))
    categories = 3
    products = 4
    return render_template('index.html', categories=categories, products=products)


@app.route("/appointment")
def appointment():
    user_atb = dao.load_user_attributes()
    return render_template('appointment.html', user_atb=user_atb)


if __name__ == '__main__':
    app.run(debug=True)
