from flask import request
from wtforms import Form,StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About me', validators=[Length(min=0,max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username,*args, **kwargs):
        super(EditProfileForm,self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username = self.username.data).first()
            if user is not None:
                raise ValidationError('Please use  a different username')

class EmptyForm(Form):
    submit = SubmitField('Submit')

class PostForm(Form):
    post = TextAreaField('Say something', validators=[DataRequired(),Length(min=1,max=140)])
    submit = SubmitField('Submit')

class SearchForm(Form):
    q = StringField(_('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args

        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False

        super(SearchForm, self).__init__(*args, **kwargs)