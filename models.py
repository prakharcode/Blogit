from app import db, login_manager, bcrypt
import datetime , re



@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))
def slugify(s):
    return re.sub('[^\w]+','-',s).lower()

entry_tags=db.Table('entry_tags',
           db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')),
           db.Column('entry_id',db.Integer,db.ForeignKey('entry.id'))
           )





class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(64))
    slug = db.Column (db.String(64),unique = True)
    active = db.Column(db.Boolean, default = True)
    admin = db.Column(db.Boolean, default = False)
    created_timestamp = db.Column(db.DateTime,default = datetime.datetime.now)


    entries = db.relationship('Entry', backref = 'author', lazy = 'dynamic')

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        return 'User: %s' %self.name

    def generate_slug(self):
        self.slug = slugify(self.name)
    def get_id(self):
        return unicode(self.id)
    def is_authenticated(self):
        return True
    def is_active(self):
        return self.active

    def is_admin(self):
        return self.admin


    def is_anonymous(self):
        return False

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash,raw_password)

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)


    @classmethod
    def create(cls, email, password, **kwargs):
        return User(
        email = email,
        password_hash = User.make_password(password),
        **kwargs
        )


    @staticmethod
    def authenticate(email, password):
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return False





class Entry(db.Model):
    public = 1
    draft = 0
    deleted = 2
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100),unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=public)
    created_timestamp = db.Column(db.DateTime ,default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime ,default=datetime.datetime.now,\
    onupdate=datetime.datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    tags = db.relationship('Tag', secondary=entry_tags, backref=db.backref('entries',lazy='dynamic'))

    def __init__(self,*args,**kwargs):
        super(Entry,self).__init__(*args,**kwargs) #call parent constructor as super is a keyword for parent constructor
        self.generator_slug()
    def generator_slug(self):
        self.slug=''
        if self.title:
            self.slug=slugify(self.title)
    def __repr__(self):
        return '<Entry: %s>'% self.title

    @property
    def tag_list(self):
        return ', '.join(tag.name for tag in self.tags)

    @property
    def tease(self):
        return self.body[:10]+'..'


class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)


    def __init__(self, *args,**kwargs):
        super(Tag, self).__init__(*args,**kwargs)
        self.slug = slugify(self.name)
    def __repr__(self):
        return '<Tag %s>' % self.name
