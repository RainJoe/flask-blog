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
    name = db.Column(db.String(80), unique=True)
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
        return 'http://www.gravatar.com/avatar/' + hashlib.md5(
            self.email.encode('utf-8')).hexdigest() + '?d=retro&s=' + str(size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    desc = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def to_json(self):
        json_post = {
            'id': self.id,
            'title': self.title,
            'body': Markup(markdown(self.body, extensions=[
                                        'markdown.extensions.fenced_code',
                                        'markdown.extensions.tables',
                                        'markdown.extensions.toc'])),
            'category': self.category.name,
            'desc': self.desc,
            'img_url': self.img_url,
            'created_time': str(self.created_time),
            'author': self.author.name
        }
        return json_post


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def to_json(self):
        json_category = {
            'id': self.id,
            'name': self.name,
            'posts': [p.to_json() for p in self.posts.all()]
        }
        return json_category


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created_time = db.Column(db.DateTime, index=True, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def to_json(self):
        json_comment = {
            'id': self.id,
            'body': self.body,
            'created_time': str(self.created_time),
            'author_name': self.author.name,
            'post': self.post.title,
            'author_avatar': self.author.avatar(5050505050)
        }
        return json_comment