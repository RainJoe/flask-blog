from flask_restful import reqparse

# session args
session_args = reqparse.RequestParser()
session_args.add_argument("email", type=str)
session_args.add_argument('password', type=str)

# user args
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str)
user_args.add_argument('email', type=str)
user_args.add_argument('password', type=str)

# article args
article_args = reqparse.RequestParser()
article_args.add_argument('title', type=str)
article_args.add_argument('desc', type=str)
article_args.add_argument('img_id', type=str)
article_args.add_argument('category', type=str)
article_args.add_argument('body', type=str)

# comment args
comment_args = reqparse.RequestParser()
comment_args.add_argument('body', type=str)
