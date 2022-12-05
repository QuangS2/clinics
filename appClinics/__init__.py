from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary


app = Flask(__name__)
app.secret_key = '4567890sdfghjklcvbnvb4567fg6yug'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/Clinicsdb?charset=utf8mb4' % quote('123456')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['CART_KEY'] = 'cart'

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(
  cloud_name = "dpwzlm56r",
  api_key = "126952895863789",
  api_secret = "NEAZeJjZq4dZDqAY_gp1f8YtfaY"
)
# babel = Babel(app=app)

#
# @babel.localeselector
# def load_locale():
#     return "vi"