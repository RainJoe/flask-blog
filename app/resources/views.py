# -*- coding:utf-8 -*-
"""
   app.api
   This module provide some api
"""


import os
from flask import request, url_for, send_from_directory, current_app
from flask_restful import Resource, Api, abort
from flask_security.decorators import login_required, roles_required
from flask_security.core import current_user
from flask_security.utils import verify_password, logout_user, hash_password, login_user
from werkzeug.utils import secure_filename
from app.models import User, Post, Category, Comment, Image
from app import db, user_datastore
from . import api


resources = Api(api)


class Session(Resource):
    """
    This class is used to manage session state
    """
    def get(self):
        pass

    def post(self):
        """
        This method is used to login
        """
        email = request.json['email']
        password = request.json['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if verify_password(password, user.password):
                login_user(user)
                return {'id': user.id,
                        'name': user.name,
                        'admin': user.has_role('admin'),
                        'key': user.get_auth_token(),
                        'avatar': user.avatar(50)}
            else:
                return {'code': 401.1, 'msg': 'incorrent password'}
        else:
            return {'code': 401.2, 'msg': 'user not found'}
    def put(self):
        pass

    @login_required
    def delete(self):
        logout_user()
        return '', 204


class UserResource(Resource):
    def get(self, user_id):
        pass

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass


class UserList(Resource):

    def post(self):
        """
        register
        """
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        password_hash = hash_password(password)
        try:
            user = user_datastore.create_user(name=name, email=email, password=password_hash)
            db.session.commit()
            return {'id': user.id, 'name': user.name, 'admin': user.has_role('admin')}
        except:
            db.session.rollback()
            return {'code': 401.3, 'msg': 'email is already registered'}, 401

    def get(self):
        nums = User.query.count()
        return {'amount': str(nums)}



class Article(Resource):
    def get(self, post_id):
        """
        return a post
        @param: post_id
        """
        post = Post.query.filter_by(id=post_id).first()
        if post:
            return post.to_json()
        else:
            abort(404, message="article {} doesn't exist".format(post_id))

    @roles_required('admin')
    def put(self, post_id):
        """
        modify post
        @param: post_id        
        """
        post = Post.query.filter_by(id=post_id).first()
        post.title = request.json['title']
        img_id = request.json['img_id']
        category = Category.query.filter_by(name=request.json['category']).first()
        img = Image.query.filter_by(id=img_id).first()
        if not category:
            category = Category(name=request.json['category'])
        post.category = category
        post.img = img
        post.body = request.json['body']
        post.desc = request.json['desc']
        db.session.commit()
        return post.to_json()

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
        return '', 204


class ArticleList(Resource):
    @roles_required('admin')
    def post(self):
        """
        Add new post
        """
        title = request.json['title']
        category = request.json['category']
        desc = request.json['desc']
        body = request.json['body']
        img_id = request.json['img_id']
        img = Image.query.filter_by(id=img_id).first()
        c = Category.query.filter_by(name=category).first()
        if not c:
            c = Category(name=category)
        p = Post(title=title, desc=desc, category=c, body=body, author=current_user, img=img)
        db.session.add(p)
        db.session.commit()
        return p.to_json()

    def get(self):
        nums = Post.query.count()
        return {'amount': str(nums), 'posts': [p.to_json() for p in Post.query.all()]}


class CommentList(Resource):
    @login_required
    def post(self, article_id):
        """
        Add new comment
        """
        body = request.json['body']
        user = current_user
        post = Post.query.filter_by(id=article_id).first()
        comment = Comment(body=body, post=post, author=user)
        db.session.add(comment)
        db.session.commit()
        return comment.to_json()

    def get(self, article_id):
        """
        return comment list by article id
        """
        post = Post.query.filter_by(id=article_id).first()
        return [comment.to_json() for comment in post.comments.all()]


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
            return {'id': img.id, 'url': img.url, 'filename': filename}
        else:
            return {'code': 401, 'msg': 'save file error'}


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
            return '', 204
        else:
            return '', 205

resources.add_resource(Session, '/sessions')
resources.add_resource(UserResource, '/users/<user_id>')
resources.add_resource(UserList, '/users')
resources.add_resource(Article, '/posts/<post_id>')
resources.add_resource(ArticleList, '/posts')
resources.add_resource(CommentList, '/comments/<article_id>')
resources.add_resource(PhotoList, '/photos')
resources.add_resource(Photo, '/photos/<filename>')
