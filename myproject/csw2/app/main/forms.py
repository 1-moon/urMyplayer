from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
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
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError,NumberRange
# from flask_pagedown.fields import PageDownField
from flask_wtf.file import FileField,FileRequired
from wtforms import ValidationError
from ..models import Role, User,PositionType,League,Capacity
import phonenumbers



# =========================Registration Form===========================
class PlayerForm(FlaskForm):
    name = StringField(label=('Player name:'), validators=[DataRequired('plase enter player name'), 
                                                     Length(1,20)]) 
    nationality = StringField(label=('Nationality:'), validators=[DataRequired('plase enter player nationality')])
    birth = DateField(label=('Birth:'), validators=[DataRequired()])
    height = FloatField(label=('Height'), validators=[DataRequired()])
    position = SelectField(label=('Position'), choices=PositionType.fetch_names)
    foot = SelectField(label=('Foot'), choices=[('Left'),('Right'),('Both')])
    club = StringField(label=('Club'))
    profile_pic = FileField(label=('Profile Pic'))
    submit = SubmitField(label=('Submit'))
    
class TeamForm(FlaskForm):    
    name = StringField(label=('Club name:'), validators=[DataRequired('plase enter player name'),Length(1,20)]) 
    league = SelectField(label=('League: '), choices=League.fetch_names)
    stadium = StringField(label=('Stadium name:'), validators=[DataRequired('plase enter name of stadium')])
    capacity = SelectField(label=('Stadium Capacity'), choices=Capacity.fetch_names)
    address= StringField(label=('Address:'), validators=[DataRequired('please enter where stadium is located')])
    manager= StringField(label=('Manager name:'), validators=[DataRequired('plase enter who is manager')])
    founded= DateField(label=('Founded:'), validators=[DataRequired()])
    telephone=StringField(label=('Contact :'), validators=[DataRequired()])
    emblem = FileField(label=('Profile Pic'), validators=[FileRequired(message='please add an image')])
    submit = SubmitField(label=('Submit'))
    
    # def validate_phone(self, telephone):
    #     try:
    #         p = phonenumbers.parse(telephone)
    #         if not phonenumbers.is_valid_number(p):
    #             raise ValueError()
    #     except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
    #         raise ValidationError('Invalid contact number')
# ============================== search Form ====================================
# class PlayerSearchForm(FlaskForm):
#     name = StringField(label=('name:'), validators=[DataRequired()])
#     position = SelectField(label=('Position'), choices=models.PositionType.fetch_names)
#     submit = SubmitField(label=('Search'))

# ============================== bid Form  ======================================
class PlaceBidForm(FlaskForm):
    # the bid amount has to be more than current bid 
    # draw from Bid table, grab the highest 
    #SELECT * FROM BID WHERE team_id = <id>
    # min = highest_bid + 1
    # whom = StringField(label=('Club name:'), validators=[DataRequired('plase enter player name'),Length(1,20)]) 
    bid_amount = FloatField(label=('£ Pound sterling'))
    place = SubmitField('Place Bids')

# profile edit oneslef
class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(0, 64)])
    location = StringField('Address', validators=[Length(0, 64)])
    league = SelectField(label=('League: '), choices=League.fetch_names )
    stadium = StringField(label=('Stadium name:'), validators=[DataRequired('plase enter name of stadium')])
    capacity = SelectField(label=('Stadium Capacity'), choices=Capacity.fetch_names)
    manager= StringField(label=('Manager name:'), validators=[DataRequired('plase enter who is manager')])
    founded= DateField(label=('Founded:'), validators=[DataRequired()])
    telephone=StringField(label=('Contact :'), validators=[DataRequired()])
    emblem = FileField(label=('Emblem Pic'), validators=[FileRequired()])
    submit = SubmitField('save')

# profile edit by admin
class EditProfileAdminForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Teamname', validators=[
                DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                'please only be letter.')])
    role = SelectField('role', coerce=int)

    location = StringField('address', validators=[Length(0, 64)])
    submit = SubmitField('save')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('This email in use.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('This team name in use.')