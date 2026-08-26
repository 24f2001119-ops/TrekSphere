from flask import render_template, redirect, url_for, flash
from . import staff_bp

from app.decorators import staff_required
from app.models import Trek, Booking
from app.forms import TrekForm
from app import db
from app.forms import StaffTrekUpdateForm
from app.forms import StaffProfileForm

from flask_login import current_user

@staff_bp.route("/dashboard")
@staff_required
def dashboard():

    assigned_treks = Trek.query.filter_by(
        staff_id=current_user.id
    ).all()

    return render_template(
        "staff/dashboard.html",
        assigned_treks=assigned_treks
    )

@staff_bp.route("/treks")
@staff_required
def assigned_treks():

    treks = Trek.query.filter_by(
        staff_id=current_user.id
    ).all()

    return render_template(
        "staff/assigned_treks.html",
        treks=treks
    )

@staff_bp.route("/treks/update/<int:trek_id>", methods=["GET", "POST"])
@staff_required
def update_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.staff_id != current_user.id:

        flash("Unauthorized", "danger")

        return redirect(url_for("staff.dashboard"))

    form = StaffTrekUpdateForm(obj=trek)

    if form.validate_on_submit():

        trek.available_slots = form.available_slots.data
        trek.status = form.status.data

        db.session.commit()

        flash("Trek Updated Successfully", "success")

        return redirect(url_for("staff.assigned_treks"))

    return render_template(
        "staff/update_trek.html",
        form=form
    )


@staff_bp.route("/participants/<int:trek_id>")
@staff_required
def participants(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.staff_id != current_user.id:

        flash("Unauthorized", "danger")

        return redirect(url_for("staff.dashboard"))

    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    return render_template(
        "staff/participants.html",
        trek=trek,
        bookings=bookings
    )

@staff_bp.route("/profile", methods=["GET", "POST"])
@staff_required
def profile():

    form = StaffProfileForm(obj=current_user)

    if form.validate_on_submit():

        current_user.name = form.name.data
        current_user.phone = form.phone.data

        db.session.commit()

        flash("Profile Updated Successfully", "success")

        return redirect(url_for("staff.profile"))

    return render_template(
        "staff/profile.html",
        form=form
    )