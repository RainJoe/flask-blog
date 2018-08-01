from flask_restful import fields

session_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'is_admin': fields.Boolean,
    'token': fields.String,
    'avatar': fields.String,
}

user_fields = {
    'id': fields.String,
    'name': fields.String,
}

user_list_fields = {
    'users': fields.List(fields.Nested(user_fields)),
    'count': fields.Integer,
}

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

comment_fields = {
    'id': fields.String,
    'body': fields.String,
    'created_time': fields.String,
    'author_name': fields.String,
    'post': fields.String,
    'author_avatar': fields.String
}
