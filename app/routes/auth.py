from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

from app.extensions import db
from app.models import User


auth = Blueprint("auth", __name__, url_prefix="/auth")


class RegisterForm(FlaskForm):
    name = StringField(
        "Nome",
        validators=[DataRequired(), Length(min=2, max=120)]
    )

    email = StringField(
        "E-mail",
        validators=[DataRequired(), Length(max=150)]
    )

    password = PasswordField(
        "Senha",
        validators=[DataRequired(), Length(min=8)]
    )

    confirm_password = PasswordField(
        "Confirmar senha",
        validators=[DataRequired(), EqualTo("password", message="As senhas não coincidem.")]
    )

    submit = SubmitField("Criar conta")

class LoginForm(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[DataRequired(), Length(max=150)]
    )

    password = PasswordField(
        "Senha",
        validators=[DataRequired()]
    )

    submit = SubmitField("Entrar")


@auth.route("/cadastro", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip().lower()

        if "@" not in email or "." not in email.split("@")[-1]:
            flash("Digite um endereço de e-mail válido.", "error")
            return render_template("auth/register.html", form=form)

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Este e-mail já está cadastrado.", "error")
            return render_template("auth/register.html", form=form)

        user = User(
            name=name,
            email=email,
            role="customer"
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash("Conta criada com sucesso.", "success")

        return redirect(url_for("main.index"))

    return render_template("auth/register.html", form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()

        user = User.query.filter_by(email=email).first()

        if user and user.is_active and user.check_password(form.password.data):
            login_user(user)

            flash("Login realizado com sucesso!", "success")
            next_page = request.args.get("next")

            if next_page and next_page.startswith("/") and not next_page.startswith("//"):
                return redirect(next_page)

            return redirect(url_for("main.index"))

        flash("E-mail ou senha incorretos.", "error")

    return render_template("auth/login.html", form=form)

@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    flash("Você saiu da sua conta.", "success")

    return redirect(url_for("main.index"))


