from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email, ValidationError
from ..models import User


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 30),
                                                   Regexp(r"^[A-Za-z][A-Za-z0-9_-]*$",
                                                          message="Username must start with a letter and contain only letters, numbers, underscores or hyphens.")])
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField("Save Changes")

    def __init__(self, original_username, original_email, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, field: StringField) -> None:
        if field.data != self.original_username:
            user = User.query.filter_by(username=field.data).first()

            if user:
                raise ValidationError("Username already in use.")

    def validate_email(self, field: StringField) -> None:
        if field.data != self.original_email:
            user = User.query.filter_by(email=field.data).first()

            if user:
                raise ValidationError("Email already registered.")
