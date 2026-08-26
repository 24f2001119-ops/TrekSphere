@admin_bp.route("/treks/add",methods=["GET","POST"])
@admin_required
def add_trek():

    form=TrekForm()
    
    form.staff_id.choices = [(0, "Not Assigned")] + [
    (staff.id, staff.name)
    for staff in User.query.filter_by(role="staff", approved=True).all()
    ]

    if form.validate_on_submit():

        trek=Trek(
            name=form.name.data,
            location=form.location.data,
            difficulty=form.difficulty.data,
            duration=form.duration.data,
            available_slots=form.available_slots.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            staff_id=form.staff_id.data if form.staff_id.data != 0 else None,
            description=form.description.data,
            status=form.status.data
        )

        db.session.add(trek)
        db.session.commit()

        flash("Trek Added","success")

        return redirect(url_for("admin.manage_treks"))

    return render_template(
        "admin/add_trek.html",
        form=form
    )