from app import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime
from flask import Markup
from markdown import markdown
import hashlib

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def avatar(self, size):
        return 'https://www.gravatar.com/avatar/' + hashlib.md5(
            self.email.encode('utf-8')).hexdigest() + '?d=retro&s=' + str(size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    description = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    img = db.relationship('Image', uselist=False, backref='post')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': Markup(markdown(self.body, extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.toc'])),
            'category': self.category.name,
            'desc': self.description,
            'img': self.img.to_dict() if self.img else '',
            'created_time': str(self.created_time),
            'author': self.author.name,
            'author_avatar': self.author.avatar(50)
        }


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'posts': [p.to_json() for p in self.posts.all()]
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_time = db.Column(db.DateTime, index=True, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'created_time': str(self.created_time),
            'author_name': self.author.name,
            'post': self.post.title,
            'author_avatar': self.author.avatar(50)
        }


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'filename': self.url.split('/')[-1]
        }
