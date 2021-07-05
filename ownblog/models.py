from ownblog import db
from flask_login import UserMixin
from ownblog import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model , UserMixin):
    id=db.Column(db.Integer , primary_key=True)
    username= db.Column(db.String , nullable=False)
    password= db.Column(db.String , nullable= False)
    karma = db.Column(db.Integer , nullable= False , default=0)
    posts= db.relationship('Post' , backref='author')
    comment = db.relationship('Comment' , backref='comment_author')

class Post(db.Model, UserMixin):
    id= db.Column(db.Integer , primary_key=True)
    title= db.Column(db.String , nullable=False)
    content = db.Column(db.Text , nullable=False)
    upvotes = db.Column(db.Integer , nullable=False , default=0)
    downvotes= db.Column(db.Integer , nullable=False , default=0)
    author_id = db.Column(db.Integer , db.ForeignKey('user.id'))

class Comment(db.Model , UserMixin):
    id= db.Column(db.Integer , primary_key=True)
    upvotes = db.Column(db.Integer , nullable=False , default=0)
    downvotes= db.Column(db.Integer , nullable=False , default=0)
    content = db.Column(db.Text , nullable=False)
    author_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer , db.ForeignKey('post.id'))
    
