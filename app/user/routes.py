from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user

from . import user_bp

from app.decorators import user_required
from app.models import Trek, Booking, User
from app import db
from app.forms import ProfileForm

@user_bp.route("/dashboard")
@user_required
def dashboard():

    available_treks = Trek.query.filter_by(status="Open").all()

    my_bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).count()

    return render_template(
        "user/dashboard.html",
        treks=available_treks,
        total_bookings=my_bookings
    )

@user_bp.route("/treks")
@user_required
def browse_treks():

    difficulty = request.args.get("difficulty")
    location = request.args.get("location")

    query = Trek.query.filter_by(status="Open")

    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    if location:
        query = query.filter(
            Trek.location.ilike(f"%{location}%")
        )

    treks = query.all()

    return render_template(
        "user/browse_treks.html",
        treks=treks
    )

@user_bp.route("/book/<int:trek_id>")
@user_required
def book_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.status != "Open":

        flash("This trek is not open for booking.", "danger")
        return redirect(url_for("user.browse_treks"))

    if trek.available_slots <= 0:

        flash("No slots available.", "danger")
        return redirect(url_for("user.browse_treks"))

    existing = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id,
        status="Booked"
    ).first()

    if existing:

        flash("You have already booked this trek.", "warning")
        return redirect(url_for("user.browse_treks"))

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id
    )

    trek.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    flash("Booking Successful", "success")

    return redirect(url_for("user.my_bookings"))

@user_bp.route("/bookings")
@user_required
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "user/my_bookings.html",
        bookings=bookings
    )


@user_bp.route("/cancel/<int:booking_id>")
@user_required
def cancel_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:

        flash("Unauthorized", "danger")
        return redirect(url_for("user.my_bookings"))

    if booking.status != "Booked":

        flash("Booking cannot be cancelled.", "warning")
        return redirect(url_for("user.my_bookings"))

    booking.status = "Cancelled"

    booking.trek.available_slots += 1

    db.session.commit()

    flash("Booking Cancelled", "success")

    return redirect(url_for("user.my_bookings"))

@user_bp.route("/history")
@user_required
def history():

    history = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "user/history.html",
        bookings=history
    )


@user_bp.route("/profile", methods=["GET", "POST"])
@user_required
def profile():

    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():

        current_user.name = form.name.data
        current_user.phone = form.phone.data

        db.session.commit()

        flash("Profile Updated", "success")

        return redirect(url_for("user.profile"))

    return render_template(
        "user/profile.html",
        form=form
    )

    
