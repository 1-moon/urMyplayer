"""
A file that manage and define database 
"""
from . import db
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask.globals import request
from flask_login import UserMixin, AnonymousUserMixin
# from markdown import markdown
from datetime import datetime
# import bleach
import hashlib
import enum




# ========================== enum classes =====================


class PositionType(enum.Enum):
    GK  = "Goalkeeper"
    LB  = "Left-back"
    LWB = "Left-wingback"
    CB  = "Centre-back"
    RB  = "Right-back"
    RWB = "Right-wingback"
    DM  = "Defensive-midfilder"
    CM  = "centre-midfilder"
    LM  = "Left-midfilder"
    AM  = "Attacking-midfilder"
    RM  = "Right-midfilder"
    FW  = "Forward"
    @classmethod
    def fetch_names(PostionType):
        return [member.value for member in PositionType]
    
class Capacity(enum.Enum):
    TEN = "10,000~20,000"
    TWN = "20~000~30,000"
    THR = "30,000~40,000"
    FOR = "40,000~50,000"
    FIF = "50,000~60,000"
    SEV = "60,000~70,000"
    EIG = "70,000~80,000"
    NIN = "80,000~90,000"
    K = "over 100,000"
    @classmethod
    def fetch_names(Capacity):
        return [member.value for member in Capacity]

class League(enum.Enum):
    EPL = "English Premier League"
    EFL = "English Football League Championship"
    SLL = "Spanish La Liga"
    SA  = "Italian Serie A"
    BUN = "Genman Bundesliga"
    L1  = "French Ligue 1"
    PPL = "Portuguese Primeira Liga"
    KLC = "Korean K-league classic"
    @classmethod
    def fetch_names(League):
        return [member.value for member in League]
# ===================================================================
    
# Module would hand over db.Model
class Player(db.Model):

    #These will make table when db.create.all() called
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(15), index=True, nullable=False)
    birth       = db.Column(db.Date, nullable=False)
    height      = db.Column(db.Numeric(10,2), nullable=False)
    position    = db.Column(db.Enum(PositionType, values_callable=lambda x: [str(member.value) for member in PositionType]), nullable=False)
    foot        = db.Column(db.String, nullable=False)
    club        = db.Column(db.String(30))
    status      = db.Column(db.Boolean, default= False)
    profile_pic = db.Column(db.String, nullable=False)
    # Foreign Key to link users (refer to primary key of the user )
    user_id     =db.Column(db.Integer, db.ForeignKey("user.id")) # table name is usually stored in lowercase 
    #   backref - 
    bids        = db.relationship('Bid', backref='user')

# ============================ Transfer system ==================== 

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    club = db.Column(db.String(50))
    bid_amount  = db.Column(db.String(20), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    #FK
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_id   = db.Column(db.Integer, db.ForeignKey("player.id"))
    
    def __repr__(self):
        return "<Name: {}>".format(self.text)
    

# ========================== Authentication ==================



class Permission:
    FOLLOW = 1
    COMMENT = 2
    BID = 4
    CHECK = 6
    REGIST = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    # Many users can have same role
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Supporter': [Permission.FOLLOW, Permission.COMMENT],
            'Registerer': [Permission.FOLLOW, Permission.COMMENT,
                        Permission.REGIST, Permission.CHECK, Permission.BID],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                            Permission.REGIST, Permission.CHECK, Permission.BID,Permission.ADMIN],
        }

        default_role = 'Supporter'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()    

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0   

    # get a string representation of Role object 
    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(64), unique=True)
    email   = db.Column(db.String(64), unique=True, index=True)
    # Do some password stuff!
    password_hash = db.Column(db.String(128))
    # User can register many teams! Relationship reference in real table
    # ==backref== 
    # teams   = db.relationship('Team', backref ='owner')
    bids     = db.relationship('Bid', backref ='Bidder')
    players  = db.relationship('Player', backref ='Registerer')
    # ==User has a role==
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    # team profile
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    league      = db.Column(db.Enum(League, values_callable=lambda x: [str(member.value) for member in League]), nullable=True)
    stadium     = db.Column(db.String(50), nullable=True)
    capacity    = db.Column(db.Enum(Capacity, values_callable=lambda x: [str(member.value) for member in Capacity]), nullable=True)
    location    = db.Column(db.String(64))
    manager     = db.Column(db.String(20), nullable=True)
    founded     = db.Column(db.DateTime, nullable=True)
    telephone   = db.Column(db.Numeric(15), nullable=True)
    emblem      = db.Column(db.String, nullable=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['MYCSW_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    
    @property 
    def password(self):
        raise AttributeError('Password can not be read')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    
    # recent visit
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

# 로그인 여부 확인하지 않고도 can, is_administrator를 사용할 수 있음
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 



