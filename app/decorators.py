from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        if current_user.role != "admin":
            flash("Access Denied!", "danger")
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper


def staff_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        if current_user.role != "staff":
            flash("Access Denied!", "danger")
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper


def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        if current_user.role != "user":
            flash("Access Denied!", "danger")
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper