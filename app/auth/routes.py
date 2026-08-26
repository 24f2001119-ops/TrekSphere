from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from . import auth_bp

from app.forms import (
    LoginForm,
    RegisterForm
)

from app.models import User
from app import db


@auth_bp.route("/")
def home():
    if current_user.is_authenticated:
        logout_user()
    return render_template("index.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        elif current_user.role == "staff":
            return redirect(url_for("staff.dashboard"))

        else:
            return redirect(url_for("user.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and user.check_password(form.password.data):

            if user.blacklisted:
                flash(
                    "Your account has been blacklisted.",
                    "danger"
                )
                return redirect(url_for("auth.login"))

            if user.role == "staff" and not user.approved:
                flash(
                    "Your account is waiting for Admin approval.",
                    "warning"
                )
                return redirect(url_for("auth.login"))

            login_user(user)

            flash("Login Successful", "success")

            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))

            elif user.role == "staff":
                return redirect(url_for("staff.dashboard"))

            else:
                return redirect(url_for("user.dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template(
        "auth/login.html",
        form=form
    )


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing:
            flash("Email already exists", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            role=form.role.data
        )

        user.set_password(form.password.data)

        if user.role == "user":
            user.approved = True
        else:
            user.approved = False

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration Successful",
            "success"
        )

        if user.role == "staff":
            flash(
                "Wait for Admin approval.",
                "info"
            )

        return redirect(url_for("auth.login"))

    return render_template(
        "auth/register.html",
        form=form
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged Out Successfully",
        "success"
    )

    return redirect(url_for("auth.login"))