from flask import session
from wtforms import PasswordField, SelectField, StringField
from wtforms.fields.html5 import DateField, URLField

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.forms.users import attach_custom_user_fields, build_custom_user_fields
from CTFd.utils.countries import SELECT_COUNTRIES_LIST
from CTFd.utils.user import get_current_user


def SettingsForm(*args, **kwargs):
    class _SettingsForm(BaseForm):
        name = StringField("아이디")
        email = StringField("Email")
        password = PasswordField("변경할 비밀번호")
        confirm = PasswordField("현재 비밀번호")
        affiliation = StringField("학과")
        website = URLField("웹사이트")
        country = SelectField("국가", choices=SELECT_COUNTRIES_LIST)
        submit = SubmitField("수정")

        @property
        def extra(self):
            fields_kwargs = _SettingsForm.get_field_kwargs()
            return build_custom_user_fields(
                self,
                include_entries=True,
                fields_kwargs=fields_kwargs,
                field_entries_kwargs={"user_id": session["id"]},
            )

        @staticmethod
        def get_field_kwargs():
            user = get_current_user()
            field_kwargs = {"editable": True}
            if user.filled_all_required_fields is False:
                # Show all fields
                field_kwargs = {}
            return field_kwargs

    field_kwargs = _SettingsForm.get_field_kwargs()
    attach_custom_user_fields(_SettingsForm, **field_kwargs)

    return _SettingsForm(*args, **kwargs)


class TokensForm(BaseForm):
    expiration = DateField("만료일")
    submit = SubmitField("생성")
