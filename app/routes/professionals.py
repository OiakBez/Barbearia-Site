from flask import Blueprint, render_template


professionals = Blueprint(
    "professionals",
    __name__,
    url_prefix="/profissionais"
)

@professionals.route("/")
def index():
    return render_template("professionals.html")