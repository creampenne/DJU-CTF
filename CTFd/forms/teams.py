from wtforms import BooleanField, PasswordField, SelectField, StringField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import InputRequired

from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.models import TeamFieldEntries, TeamFields
from CTFd.utils.countries import SELECT_COUNTRIES_LIST
from CTFd.utils.user import get_current_team


def build_custom_team_fields(
    form_cls,
    include_entries=False,
    fields_kwargs=None,
    field_entries_kwargs=None,
    blacklisted_items=("affiliation", "website"),
):
    if fields_kwargs is None:
        fields_kwargs = {}
    if field_entries_kwargs is None:
        field_entries_kwargs = {}

    fields = []
    new_fields = TeamFields.query.filter_by(**fields_kwargs).all()
    user_fields = {}

    # Only include preexisting values if asked
    if include_entries is True:
        for f in TeamFieldEntries.query.filter_by(**field_entries_kwargs).all():
            user_fields[f.field_id] = f.value

    for field in new_fields:
        if field.name.lower() in blacklisted_items:
            continue

        form_field = getattr(form_cls, f"fields[{field.id}]")

        # Add the field_type to the field so we know how to render it
        form_field.field_type = field.field_type

        # Only include preexisting values if asked
        if include_entries is True:
            initial = user_fields.get(field.id, "")
            form_field.data = initial
            if form_field.render_kw:
                form_field.render_kw["data-initial"] = initial
            else:
                form_field.render_kw = {"data-initial": initial}

        fields.append(form_field)
    return fields


def attach_custom_team_fields(form_cls, **kwargs):
    new_fields = TeamFields.query.filter_by(**kwargs).all()
    for field in new_fields:
        validators = []
        if field.required:
            validators.append(InputRequired())

        if field.field_type == "text":
            input_field = StringField(
                field.name, description=field.description, validators=validators
            )
        elif field.field_type == "boolean":
            input_field = BooleanField(
                field.name, description=field.description, validators=validators
            )

        setattr(form_cls, f"fields[{field.id}]", input_field)


class TeamJoinForm(BaseForm):
    name = StringField("팀명", validators=[InputRequired()])
    password = PasswordField("팀 비밀번호", validators=[InputRequired()])
    submit = SubmitField("가입")


def TeamRegisterForm(*args, **kwargs):
    class _TeamRegisterForm(BaseForm):
        name = StringField("팀명", validators=[InputRequired()])
        password = PasswordField("팀 비밀번호", validators=[InputRequired()])
        submit = SubmitField("생성")

        @property
        def extra(self):
            return build_custom_team_fields(
                self, include_entries=False, blacklisted_items=()
            )

    attach_custom_team_fields(_TeamRegisterForm)
    return _TeamRegisterForm(*args, **kwargs)


def TeamSettingsForm(*args, **kwargs):
    class _TeamSettingsForm(BaseForm):
        name = StringField(
            "팀명",
            description="다른 참가자에게 공개할 팀명을 입력하세요.",
        )
        password = PasswordField(
            "새로운 팀 비밀번호", description="새로운 팀 비밀번호를 입력하세요."
        )
        confirm = PasswordField(
            "비밀번호 확인",
            description="새로운 팀 비밀번호를 다시 한번 입력하세요.",
        )
        affiliation = StringField(
            "학과",
            description="다른 참가자에게 공개할 학과명을 입력하세요.",
        )
        website = URLField(
            "웹사이트",
            description="다른 참가자에게 공개할 팀 웹사이트를 작성하세요.(없을시 빈칸)",
        )
        country = SelectField(
            "국가",
            choices=SELECT_COUNTRIES_LIST,
            description="다른 참가자에게 공개할 국가를 선택하세요.",
        )
        submit = SubmitField("확인")

        @property
        def extra(self):
            fields_kwargs = _TeamSettingsForm.get_field_kwargs()
            return build_custom_team_fields(
                self,
                include_entries=True,
                fields_kwargs=fields_kwargs,
                field_entries_kwargs={"team_id": self.obj.id},
            )

        def get_field_kwargs():
            team = get_current_team()
            field_kwargs = {"editable": True}
            if team.filled_all_required_fields is False:
                # Show all fields
                field_kwargs = {}
            return field_kwargs

        def __init__(self, *args, **kwargs):
            """
            Custom init to persist the obj parameter to the rest of the form
            """
            super().__init__(*args, **kwargs)
            obj = kwargs.get("obj")
            if obj:
                self.obj = obj

    field_kwargs = _TeamSettingsForm.get_field_kwargs()
    attach_custom_team_fields(_TeamSettingsForm, **field_kwargs)

    return _TeamSettingsForm(*args, **kwargs)


class TeamCaptainForm(BaseForm):
    # Choices are populated dynamically at form creation time
    captain_id = SelectField("팀장", choices=[], validators=[InputRequired()])
    submit = SubmitField("확인")


class TeamSearchForm(BaseForm):
    field = SelectField(
        "Search Field",
        choices=[
            ("name", "Name"),
            ("id", "ID"),
            ("affiliation", "Affiliation"),
            ("website", "Website"),
        ],
        default="name",
        validators=[InputRequired()],
    )
    q = StringField("Parameter", validators=[InputRequired()])
    submit = SubmitField("Search")


class PublicTeamSearchForm(BaseForm):
    field = SelectField(
        "Search Field",
        choices=[
            ("name", "팀명"),
            ("affiliation", "학과명"),
            ("website", "웹사이트"),
        ],
        default="name",
        validators=[InputRequired()],
    )
    q = StringField("Parameter", validators=[InputRequired()])
    submit = SubmitField("Search")


class TeamBaseForm(BaseForm):
    name = StringField("Team Name", validators=[InputRequired()])
    email = EmailField("Email")
    password = PasswordField("Password")
    website = URLField("Website")
    affiliation = StringField("Affiliation")
    country = SelectField("Country", choices=SELECT_COUNTRIES_LIST)
    hidden = BooleanField("Hidden")
    banned = BooleanField("Banned")
    submit = SubmitField("Submit")


def TeamCreateForm(*args, **kwargs):
    class _TeamCreateForm(TeamBaseForm):
        pass

        @property
        def extra(self):
            return build_custom_team_fields(self, include_entries=False)

    attach_custom_team_fields(_TeamCreateForm)

    return _TeamCreateForm(*args, **kwargs)


def TeamEditForm(*args, **kwargs):
    class _TeamEditForm(TeamBaseForm):
        pass

        @property
        def extra(self):
            return build_custom_team_fields(
                self,
                include_entries=True,
                fields_kwargs=None,
                field_entries_kwargs={"team_id": self.obj.id},
            )

        def __init__(self, *args, **kwargs):
            """
            Custom init to persist the obj parameter to the rest of the form
            """
            super().__init__(*args, **kwargs)
            obj = kwargs.get("obj")
            if obj:
                self.obj = obj

    attach_custom_team_fields(_TeamEditForm)

    return _TeamEditForm(*args, **kwargs)


class TeamInviteForm(BaseForm):
    link = URLField("초대 링크")


class TeamInviteJoinForm(BaseForm):
    submit = SubmitField("가입")
