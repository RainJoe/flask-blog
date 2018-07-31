# -*- coding:utf-8 -*-
"""
   app.api
   This module provide some api
"""

import os
from flask import request, url_for, send_from_directory, current_app
from flask_restful import Resource, Api, marshal_with, fields, reqparse, HTTPException
from flask_security.decorators import login_required, roles_required
from flask_security.core import current_user
from flask_security.utils import verify_password, logout_user, hash_password, login_user
from werkzeug.utils import secure_filename
from app.models import User, Post, Category, Comment, Image
from app import db, user_datastore
from . import api

errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username or email already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
    },
    'PasswordWrongError': {
        'message': "Password dose not match.",
        'status': 411,
    },
    'UpdateResourceError': {
        'message': "Updating resource failed.",
        'status': 412,
    },
}


class ResourceDoesNotExist(HTTPException):
    pass


class UserAlreadyExistsError(HTTPException):
    pass


class PasswordWrongError(HTTPException):
    pass


class UpdateResourceError(HTTPException):
    pass


resources = Api(api, errors=errors)

session_args = reqparse.RequestParser()
session_args.add_argument("email", type=str)
session_args.add_argument('password', type=str)

session_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'is_admin': fields.Boolean,
    'token': fields.String,
    'avatar': fields.String,
}


class Session(Resource):
    """
    This class is used to manage session state
    """

    @marshal_with(session_fields)
    def post(self):
        """
        This method is used to login
        """
        args = session_args.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if not user:
            raise ResourceDoesNotExist

        if not verify_password(args['password'], user.password):
            raise PasswordWrongError

        login_user(user)

        return {'id': user.id,
                'name': user.name,
                'is_admin': user.has_role('admin'),
                'token': user.get_auth_token(),
                'avatar': user.avatar(50)}

    @login_required
    def delete(self):
        logout_user()
        return "", 204


user_args = reqparse.RequestParser()
user_args.add_argument('name', fields.String)
user_args.add_argument('email', fields.String)
user_args.add_argument('password', fields.String)


user_fields = {
    'id': fields.String,
    'name': fields.String,
}


user_list_fields = {
    'users': fields.List(fields.Nested(user_fields)),
    'count': fields.Integer,
}


class UserList(Resource):

    @marshal_with(user_fields)
    def post(self):
        """
        register
        """
        args = user_args.parse_args()
        password_hash = hash_password(args['password'])
        try:
            user = user_datastore.create_user(name=args['name'], email=args['email'], password=password_hash)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise UserAlreadyExistsError

    @roles_required('admin')
    @marshal_with(user_list_fields)
    def get(self):
        users = User.query.all()
        count = User.query.count()
        return {'users': users, 'count': count}


article_args = reqparse.RequestParser()
article_args.add_argument('title', fields.String)
article_args.add_argument('desc', fields.String)
article_args.add_argument('img_id', fields.Integer)
article_args.add_argument('category', fields.String)
article_args.add_argument('body', fields.String)

img_fields = {
    'id': fields.Integer,
    'url': fields.String,
    'filename': fields.String,
}

article_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'category': fields.String,
    'desc': fields.String,
    'img': fields.Nested(img_fields),
    'created_time': fields.String,
    'author': fields.String,
    'author_avatar': fields.String
}

article_list_fields = {
    'count': fields.Integer,
    'posts': fields.List(fields.Nested(article_fields))
}


class Article(Resource):
    @marshal_with(article_fields)
    def get(self, post_id):
        """
        return a post
        @param: post_id
        """
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            raise ResourceDoesNotExist
        return post.to_dict()

    @roles_required('admin')
    @marshal_with(article_fields)
    def put(self, post_id):
        """
        modify post
        @param: post_id        
        """
        args = article_args.parse_args()
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            raise ResourceDoesNotExist

        post.title = args['title']
        img_id = args['img_id']
        category = Category.query.filter_by(name=args['category']).first()
        img = Image.query.filter_by(id=img_id).first()
        if not category:
            category = Category(name=args['category'])
        try:
            post.category = category
            post.img = img
            post.body = request.json['body']
            post.desc = request.json['desc']
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise UpdateResourceError
        return post.to_dict()

    @roles_required('admin')
    def delete(self, post_id):
        """
        delete post
        @param: post_id
        """
        post = Post.query.filter_by(id=post_id).first()
        img = post.img
        if img:
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], img.url.split('/')[-1])
            if os.path.exists(path):
                os.remove(path)
            db.session.delete(img)
        db.session.delete(post)
        db.session.commit()
        return "", 204


class ArticleList(Resource):
    @roles_required('admin')
    @marshal_with(article_fields)
    def post(self):
        """
        Add new post
        """
        args = article_args.parse_args()
        img = Image.query.filter_by(id=args['img_id']).first()
        category = Category.query.filter_by(name=args['category']).first()
        if not category:
            category = Category(name=args['category'])
        p = Post(title=args['title'], desc=args['desc'], category=category, body=args['body'], author=current_user, img=img)
        try:
            db.session.add(p)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise UpdateResourceError
        return p.to_dict()

    @marshal_with(article_list_fields)
    def get(self):
        posts = Post.query.all()
        count = Post.query.count()
        return {'count': count, 'posts': posts}


comment_args = reqparse.RequestParser()
comment_args.add_argument('body', fields.String)


comment_fields = {
    'id': fields.String,
    'body': fields.String,
    'created_time': fields.String,
    'author_name': fields.String,
    'post': fields.String,
    'author_avatar': fields.String
}


class CommentList(Resource):
    @login_required
    @marshal_with(comment_fields)
    def post(self, article_id):
        """
        Add new comment
        """
        args = comment_args.parse_args()
        user = current_user
        post = Post.query.filter_by(id=article_id).first()
        comment = Comment(body=args['body'], post=post, author=user)
        try:
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise UpdateResourceError
        return comment.to_dict()

    @marshal_with(comment_fields)
    def get(self, article_id):
        """
        return comment list by article id
        """
        post = Post.query.filter_by(id=article_id).first()
        comments = post.comments.all()
        return comments


class PhotoList(Resource):

    @staticmethod
    def allowed_file(filename):
        """
        allowed file type
        @parma: filename
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

    @roles_required('admin')
    @marshal_with(img_fields)
    def post(self):
        """
        add photo
        """
        file = request.files['file']
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            img_url = url_for('api.photo', filename=filename)
            img = Image(url=img_url)
            db.session.add(img)
            db.session.commit()
            return img.to_dict()
        else:
            raise UpdateResourceError


class Photo(Resource):

    def get(self, filename):
        return send_from_directory(
            current_app.config['UPLOAD_FOLDER'], filename)

    @roles_required('admin')
    def delete(self, filename):
        img_url = url_for('api.photo', filename=filename)
        img = Image.query.filter_by(url=img_url).first()
        if img:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            db.session.delete(img)
            db.session.commit()
            return '', 201
        else:
            raise ResourceDoesNotExist


resources.add_resource(Session, '/sessions')
resources.add_resource(UserList, '/users')
resources.add_resource(Article, '/posts/<post_id>')
resources.add_resource(ArticleList, '/posts')
resources.add_resource(CommentList, '/comments/<article_id>')
resources.add_resource(PhotoList, '/photos')
resources.add_resource(Photo, '/photos/<filename>')
