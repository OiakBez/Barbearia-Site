from datetime import datetime, timezone

from app.extensions import db


class Appointment(db.Model):

    __tablename__ = "appointments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    professional_id = db.Column(
        db.Integer,
        db.ForeignKey("professionals.id"),
        nullable=False,
        index=True
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("services.id"),
        nullable=False
    )

    scheduled_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        index=True
    )

    price_at_booking = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    duration_at_booking = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="pending"
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    customer = db.relationship(
        "User",
        back_populates="appointments",
        foreign_keys=[customer_id]
    )

    professional = db.relationship(
        "Professional",
        back_populates="appointments"
    )

    service = db.relationship(
        "Service",
        back_populates="appointments"
    )

    def __repr__(self):
        return f"<Appointment id={self.id} status={self.status}>"