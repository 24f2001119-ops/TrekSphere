from flask import render_template, request
from flask_login import login_required,current_user

from . import admin_bp
from app.models import User,Trek,Booking

from flask import redirect,url_for,flash
from app.forms import TrekForm
from app import db

from app.decorators import admin_required

@admin_bp.route("/dashboard")
@admin_required
def dashboard():

    if current_user.role!="admin":
        return "Unauthorized"

    total_users=User.query.filter_by(role="user").count()

    total_staff=User.query.filter_by(role="staff").count()

    total_treks=Trek.query.count()

    total_bookings=Booking.query.count()

    open_treks = Trek.query.filter_by(status="Open").count()

    completed_treks = Trek.query.filter_by(status="Completed").count()

    return render_template(
    "admin/dashboard.html",
    total_users=total_users,
    total_staff=total_staff,
    total_treks=total_treks,
    total_bookings=total_bookings,
    open_treks=open_treks,
    completed_treks=completed_treks
    )



@admin_bp.route("/treks")
@admin_required
def manage_treks():

    treks=Trek.query.all()

    return render_template(
        "admin/manage_treks.html",
        treks=treks
    )


@admin_bp.route("/treks/add", methods=["GET", "POST"])
@admin_required
def add_trek():

    form = TrekForm()

    form.staff_id.choices = [(0, "Not Assigned")] + [
        (staff.id, staff.name)
        for staff in User.query.filter_by(role="staff", approved=True).all()
    ]

    if form.validate_on_submit():

        # Prevent assigning same staff to overlapping treks
        if form.staff_id.data != 0:

            existing_trek = Trek.query.filter(
                Trek.staff_id == form.staff_id.data,
                Trek.start_date <= form.end_date.data,
                Trek.end_date >= form.start_date.data
            ).first()

            if existing_trek:

                flash(
                    f"This staff is already assigned to '{existing_trek.name}' during the selected dates.",
                    "danger"
                )

                return render_template(
                    "admin/add_trek.html",
                    form=form
                )

        trek = Trek(
            name=form.name.data,
            location=form.location.data,
            difficulty=form.difficulty.data,
            duration=form.duration.data,
            available_slots=form.available_slots.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            altitude=form.altitude.data,
            staff_id=form.staff_id.data if form.staff_id.data != 0 else None,
            description=form.description.data,
            status=form.status.data
        )

        db.session.add(trek)
        db.session.commit()

        flash("Trek Added Successfully", "success")

        return redirect(url_for("admin.manage_treks"))

    return render_template(
        "admin/add_trek.html",
        form=form
    )

@admin_bp.route("/treks/edit/<int:trek_id>", methods=["GET", "POST"])
@admin_required
def edit_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    form = TrekForm(obj=trek)

    form.staff_id.choices = [(0, "Not Assigned")] + [
        (staff.id, staff.name)
        for staff in User.query.filter_by(role="staff", approved=True).all()
    ]

    if request.method == "GET":

        if trek.staff_id:
            form.staff_id.data = trek.staff_id
        else:
            form.staff_id.data = 0

    if form.validate_on_submit():

        # Prevent assigning same staff to overlapping treks
        if form.staff_id.data != 0:

            existing_trek = Trek.query.filter(
                Trek.staff_id == form.staff_id.data,
                Trek.id != trek.id,
                Trek.start_date <= form.end_date.data,
                Trek.end_date >= form.start_date.data
            ).first()

            if existing_trek:

                flash(
                    f"This staff is already assigned to '{existing_trek.name}' during the selected dates.",
                    "danger"
                )

                return render_template(
                    "admin/edit_trek.html",
                    form=form,
                    trek=trek
                )

        trek.name = form.name.data
        trek.location = form.location.data
        trek.difficulty = form.difficulty.data
        trek.duration = form.duration.data
        trek.available_slots = form.available_slots.data
        trek.start_date = form.start_date.data
        trek.end_date = form.end_date.data
        trek.description = form.description.data
        trek.altitude = form.altitude.data
        trek.status = form.status.data
        trek.staff_id = form.staff_id.data if form.staff_id.data != 0 else None

        db.session.commit()

        flash("Trek Updated Successfully", "success")

        return redirect(url_for("admin.manage_treks"))

    return render_template(
        "admin/edit_trek.html",
        form=form,
        trek=trek
    )


@admin_bp.route("/treks/delete/<int:trek_id>")
@admin_required
def delete_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)

    db.session.commit()

    flash("Trek Deleted Successfully", "success")

    return redirect(url_for("admin.manage_treks"))

@admin_bp.route("/staff")
@admin_required
def manage_staff():

    staff_members = User.query.filter_by(role="staff").all()

    return render_template(
        "admin/manage_staff.html",
        staff_members=staff_members
    )

@admin_bp.route("/staff/approve/<int:staff_id>")
@admin_required
def approve_staff(staff_id):

    staff = User.query.get_or_404(staff_id)

    staff.approved = True

    db.session.commit()

    flash("Staff Approved Successfully", "success")

    return redirect(url_for("admin.manage_staff"))

@admin_bp.route("/staff/toggle_blacklist/<int:staff_id>")
@admin_required
def toggle_staff_blacklist(staff_id):

    staff = User.query.get_or_404(staff_id)

    staff.blacklisted = not staff.blacklisted

    db.session.commit()

    if staff.blacklisted:
        flash("Staff Blacklisted", "warning")
    else:
        flash("Staff Unblacklisted", "success")

    return redirect(url_for("admin.manage_staff"))

@admin_bp.route("/users")
@admin_required
def manage_users():

    users = User.query.filter_by(role="user").all()

    return render_template(
        "admin/manage_users.html",
        users=users
    )

@admin_bp.route("/users/toggle_blacklist/<int:user_id>")
@admin_required
def toggle_user_blacklist(user_id):

    user = User.query.get_or_404(user_id)

    user.blacklisted = not user.blacklisted

    db.session.commit()

    if user.blacklisted:
        flash("User Blacklisted Successfully", "warning")
    else:
        flash("User Unblacklisted Successfully", "success")

    return redirect(url_for("admin.manage_users"))

@admin_bp.route("/users/search")
@admin_required
def search_users():

    query = request.args.get("query", "")

    users = User.query.filter(
        User.role == "user",
        (User.name.ilike(f"%{query}%")) |
        (User.email.ilike(f"%{query}%"))
    ).all()

    return render_template(
        "admin/manage_users.html",
        users=users,
        query=query
    )

@admin_bp.route("/users/<int:user_id>/bookings")
@admin_required
def user_bookings(user_id):

    user = User.query.get_or_404(user_id)

    bookings = Booking.query.filter_by(user_id=user.id).all()

    return render_template(
        "admin/user_bookings.html",
        user=user,
        bookings=bookings
    )


@admin_bp.route("/bookings")
@admin_required
def AllUserBooking():

    bookings = Booking.query.filter_by()

    return render_template(
        "admin/AllUserBooking.html",
        bookings=bookings
    )
