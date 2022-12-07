from functools import wraps
from flask_login import current_user
from flask import redirect
from appClinics.models import User, UserRole


def annonynous_user(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')

        return f(*args, **kwargs)

    return decorated_func


def nurse_user(f):
    @wraps(f)
    def nurse_func(*args, **kwargs):
        if current_user.is_authenticated \
                and current_user.role == UserRole.NURSE:
            return f(*args, **kwargs)
        return redirect('/')
    return nurse_func
