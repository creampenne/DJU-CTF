from wtforms import PasswordField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.forms.users import (
    attach_custom_user_fields,
    attach_registration_code_field,
    build_custom_user_fields,
    build_registration_code_field,
)


def RegistrationForm(*args, **kwargs):
    class _RegistrationForm(BaseForm):
        name = StringField(
            "아이디", validators=[InputRequired()], render_kw={"autofocus": True}
        )
        email = EmailField("Email", validators=[InputRequired()])
        password = PasswordField("비밀번호", validators=[InputRequired()])
        submit = SubmitField("가입")

        @property
        def extra(self):
            return build_custom_user_fields(
                self, include_entries=False, blacklisted_items=()
            ) + build_registration_code_field(self)

    attach_custom_user_fields(_RegistrationForm)
    attach_registration_code_field(_RegistrationForm)

    return _RegistrationForm(*args, **kwargs)


class LoginForm(BaseForm):
    name = StringField(
        "아이디(Email)",
        validators=[InputRequired()],
        render_kw={"autofocus": True},
    )
    password = PasswordField("비밀번호", validators=[InputRequired()])
    submit = SubmitField("로그인")


class ConfirmForm(BaseForm):
    submit = SubmitField("Resend Confirmation Email")


class ResetPasswordRequestForm(BaseForm):
    email = EmailField(
        "Email", validators=[InputRequired()], render_kw={"autofocus": True}
    )
    submit = SubmitField("확인")


class ResetPasswordForm(BaseForm):
    password = PasswordField(
        "비밀번호", validators=[InputRequired()], render_kw={"autofocus": True}
    )
    submit = SubmitField("확인")
