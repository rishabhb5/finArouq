from flask import session
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    RadioField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from flask_app.models import User


class PostTypeForm(FlaskForm):
    post_type = RadioField(
        "Is it a Youtube Video or Text?",
        validators=[DataRequired()],
        choices=[("video", "YouTube Video Link"), ("text", "Text Post")],
    )

    submit = SubmitField("Next →")


class CreatePostForm(FlaskForm):
    title = StringField("What name shall your post have?", validators=[DataRequired(), Length(min=5, max=100)])

    text = TextAreaField("Now write what is on your mind:")
    video_id = StringField("Please type in all the rubbish at the end of the share url")

    submit = SubmitField("Submit →")

    def validate_video_id(self, video_id):
        if session["post_type"] == "video":
            if len(video_id.data.strip()) != 11:
                raise ValidationError("The YouTube video ID must be 11 characters long")


class CommentForm(FlaskForm):
    text = TextAreaField("Comment:", validators=[Length(min=1)])

    submit = SubmitField("Submit Comment")
