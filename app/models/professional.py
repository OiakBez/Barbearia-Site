from app.extensions import db


class Professional(db.Model):

    __tablename__ = "professionals"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    specialty = db.Column(
        db.String(100),
        nullable=True
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    photo = db.Column(
        db.String(255),
        nullable=True
    )

    is_available = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    user = db.relationship(
        "User",
        back_populates="professional"
    )

    def __repr__(self):
        return f"<Professional user_id={self.user_id}>"