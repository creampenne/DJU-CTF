from wtforms import (
    FileField,
    HiddenField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    TextAreaField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired

from CTFd.constants.themes import DEFAULT_THEME
from CTFd.forms import BaseForm
from CTFd.forms.fields import SubmitField
from CTFd.utils.config import get_themes


class SetupForm(BaseForm):
    ctf_name = StringField(
        "이벤트 이름", description="CTF 이름을 입력하세요."
    )
    ctf_description = TextAreaField(
        "이벤트 설명", description="CTF 설명을 입력하세요."
    )
    user_mode = RadioField(
        "모드 선택",
        choices=[("teams", "팀"), ("users", "개인")],
        default="teams",
        description="팀으로 참가할지, 개인으로 참가할지 선택합니다.",
        validators=[InputRequired()],
    )

    name = StringField(
        "관리자 이름",
        description="관리자 계정으로 사용할 이름을 입력하세요.",
        validators=[InputRequired()],
    )
    email = EmailField(
        "관리자 이메일",
        description="관리자 계정으로 사용할 Email을 입력하세요.",
        validators=[InputRequired()],
    )
    password = PasswordField(
        "관리자 비밀번호",
        description="관리자 계정으로 사용할 비밀번호를 입력하세요.",
        validators=[InputRequired()],
    )

    ctf_logo = FileField(
        "로고",
        description="CTF 이름 대신에 사용할 로고를 등록하세요. 홈페이지 버튼으로 사용됩니다.",
    )
    ctf_banner = FileField(
        "배너", description="홈페이지에 사용할 배너를 등록하세요."
    )
    ctf_small_icon = FileField(
        "아이콘",
        description="사용자 브라우저에서 사용할 favicon을 등록하세요. 32x32px의 PNG 파일만 등록 가능합니다.",
    )
    ctf_theme = SelectField(
        "테마",
        description="사용할 테마를 선택하세요. 추후에 변경 가능합니다.",
        choices=list(zip(get_themes(), get_themes())),
        default=DEFAULT_THEME,
        validators=[InputRequired()],
    )
    theme_color = HiddenField(
        "테마 색상",
        description="사용할 테마 컬러를 선택하세요. 테마의 지원이 필요합니다.",
    )

    start = StringField(
        "시작 시간", description="CTF 시작 시간을 설정하세요."
    )
    end = StringField(
        "종료 시간", description="CTF 종료 시간을 설정하세요."
    )
    submit = SubmitField("종료")
