from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db   


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    phone = db.Column(db.String(15))

    role = db.Column(db.String(20), nullable=False)
    

    approved = db.Column(db.Boolean, default=False)

    blacklisted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    

    assigned_treks = db.relationship(
        "Trek",
        backref="staff",
        lazy=True,
        foreign_keys="Trek.staff_id"
    )

    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True,
        cascade="all, delete"
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.name}>"


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    difficulty = db.Column(db.String(20), nullable=False)

    duration = db.Column(db.Integer, nullable=False)

    available_slots = db.Column(db.Integer, nullable=False)

    altitude=db.Column(db.Integer, nullable=False)

    start_date = db.Column(db.Date)

    end_date = db.Column(db.Date)

    description = db.Column(db.Text)

    status = db.Column(
        db.String(20),
        default="Open"
    )
    

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    bookings = db.relationship(
        "Booking",
        backref="trek",
        lazy=True,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Trek {self.name}>"



class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    booking_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        default="Booked"
    )
    

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    trek_id = db.Column(
        db.Integer,
        db.ForeignKey("treks.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Booking {self.id}>"



