from flask import request
from . import api
from flask_restful import Resource, Api, reqparse, abort
from app.models import User, Post, Category, Comment
from flask_security.decorators import login_required, roles_required
from flask_security.core import AnonymousUser, current_user
from flask_security.utils import verify_password, logout_user, hash_password, login_user
from app import db, user_datastore

apis = Api(api)

class Session(Resource):
    def get(self):
        pass

    def post(self):
        email = request.json['email']
        password = request.json['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if verify_password(password, user.password):
                login_user(user)
                return {'id': user.id, 'name': user.name, 'admin': user.has_role('admin'), 'key': user.get_auth_token()}
            else:
                return {'code': 401.1, 'msg': 'incorrent password'}, 401
        else:
            return {'code': 401.2, 'msg': 'user not found'}, 401
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
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        password_hash = hash_password(password)
        try:
            user = user_datastore.create_user(name=name, email=email, password=password_hash)
            db.session.commit()
            return {'id': user.id, 'name': user.name, 'admin': user.has_role('admin')}
        except:
            return {'code': 401.3, 'msg': 'email is already registered'}, 401

    def get(self):
        pass


class Article(Resource):
    def get(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        if post:
            return post.to_json()
        else:
            abort(404, message="article {} doesn't exist".format(post_id))
    
    @roles_required('admin')
    def put(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        post.title = request.json['title']
        category = Category.query.filter_by(name=request.json['category']).first()
        if not category:
            category = Category(name=request.json['category'])
        post.category = category
        post.body = request.json['body']
        post.desc = request.json['desc']
        db.session.commit()
        return post.to_json()
    
    @roles_required('admin')
    def delete(self, post_id):
        post = Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return '', 204


class ArticleList(Resource):
    @roles_required('admin')
    def post(self):
        title = request.json['title']
        category = request.json['category']
        desc = request.json['desc']
        body = request.json['body']
        c = Category.query.filter_by(name=category).first()
        if not c:
            c = Category(name=category)
        p = Post(title=title, desc=desc, category=c, body=body, author=current_user)
        db.session.add(p)
        db.session.commit()
        return p.to_json()

    def get(self):
        return [p.to_json() for p in Post.query.all()]

class CommentList(Resource):
    @login_required
    def post(self, article_id):
        body = request.json['body']
        user = current_user
        post = Post.query.filter_by(id=article_id).first()
        comment = Comment(body=body, post=post, author=user)
        db.session.add(comment)
        db.session.commit()
        return comment.to_json()
    
    def get(self, article_id):
        post = Post.query.filter_by(id=article_id).first()
        return [comment.to_json() for comment in post.comments.all()]


apis.add_resource(Session, '/sessions')
apis.add_resource(UserResource, '/users/<user_id>')
apis.add_resource(UserList, '/users')
apis.add_resource(Article, '/posts/<post_id>')
apis.add_resource(ArticleList, '/posts')
apis.add_resource(CommentList, '/comments/<article_id>')