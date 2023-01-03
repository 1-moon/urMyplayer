from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    DateField,
    SelectField,
    IntegerField,
    RadioField,
    FloatField,
    validators
) 

from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from .. import models
from flask_wtf.file import FileRequired, FileField

# =========================Authentication Form===================================
class LoginForm(FlaskForm):
    email = StringField(label=('Email'), validators=[DataRequired('plase enter your email'), 
                                                     Length(1,64), Email('This is not email type')]) 
    
    password = PasswordField(label=('Password:'), validators=[DataRequired()])
    remember_me = BooleanField(label=('Login status maintain:'))
    submit = SubmitField(label=('Login'))

class SignupForm(FlaskForm):
    email = StringField(label=('Email'), validators=[DataRequired('please enter your Email'), 
                                                     Length(1,64), Email('This is not email type')]) 
    # member = RadioField(label=('Member'), choices=[('Supporter'),('Owner')])
    username = StringField(label=('Club name:'), validators=[DataRequired('please enter your ID'),
                                                      Length(1,64), Regexp('^\w+$',
                                                                           message='Id should be made of letter')])
    password = PasswordField(label=('Password:'), validators=[DataRequired('please enter your password'),
                                                              EqualTo('password2', message='password is incorrect.')])
    password2 = PasswordField(label=('Password confirmation:'), validators=[DataRequired('please enter your password')])
    submit = SubmitField(label=('Register'))

# ============================= Editing Form =====================================
class EditProfileForm(FlaskForm):
    league = SelectField(label=('League: '), choices=models.League.fetch_names)
    stadium = StringField(label=('Stadium name:'), validators=[DataRequired('plase enter name of stadium')])
    capacity = SelectField(label=('Stadium Capacity'), choices=models.Capacity.fetch_names)
    address= StringField(label=('Address:'), validators=[DataRequired('please enter where stadium is located')])
    manager= StringField(label=('Manager name:'), validators=[DataRequired('plase enter who is manager')])
    founded= DateField(label=('Founded:'), validators=[DataRequired()])
    telephone=StringField(label=('Contact :'), validators=[DataRequired()])
    emblem = FileField(label=('Profile Pic'), validators=[FileRequired(message='please add an image')])
    submit = SubmitField(label=('Submit'))

    def validate_phone(self, telephone):
        try:
            p = phonenumbers.parse(telephone)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid contact number')

class EditProfileAdminForm(FlaskForm):
    email = StringField(label=('Email'), validators=[DataRequired('please enter your Email'), 
                                                     Length(1,64), Email('This is not email type')]) 
    username = StringField(label=('Club name:'), validators=[DataRequired('please enter your ID'),
                                                      Length(1,64), Regexp('^\w+$',
                                                                           message='Id should be made of letter')])
    role = SelectField('Role', coerce=int)

    league = SelectField(label=('League: '), choices=models.League.fetch_names)
    stadium = StringField(label=('Stadium name:'), validators=[DataRequired('plase enter name of stadium')])
    capacity = SelectField(label=('Stadium Capacity'), choices=models.Capacity.fetch_names)
    address= StringField(label=('Address:'), validators=[DataRequired('please enter where stadium is located')])
    manager= StringField(label=('Manager name:'), validators=[DataRequired('plase enter who is manager')])
    founded= DateField(label=('Founded:'), validators=[DataRequired()])
    telephone=StringField(label=('Contact :'), validators=[DataRequired()])
    emblem = FileField(label=('Profile Pic'), validators=[FileRequired(message='please add an image')])
    submit = SubmitField(label=('Submit'))

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.user = user
        
    def validate_phone(self, telephone):
        try:
            p = phonenumbers.parse(telephone)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid contact number')

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('This email already used')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('This team name already used.')