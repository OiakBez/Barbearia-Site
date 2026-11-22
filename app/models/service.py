from datetime import datetime, timezone

from app.extensions import db

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(
        db.integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    appointments = db.relationship(
        "Appointment",
        back_populates="service"
    )

    def __repr__(self):
        return f"<Service {self.name}>"