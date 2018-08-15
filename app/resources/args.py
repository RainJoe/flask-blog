from flask_restful import reqparse

# session args
session_args = reqparse.RequestParser()
session_args.add_argument("email", type=str, required=True)
session_args.add_argument('password', type=str, required=True)

# user args
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str) 
user_args.add_argument('email', type=str, required=True)
user_args.add_argument('password', type=str, required=True)

# article args
article_args = reqparse.RequestParser()
article_args.add_argument('title', type=str, required=True)
article_args.add_argument('desc', type=str, required=True)
article_args.add_argument('img_id', type=int)
article_args.add_argument('category', type=str, required=True)
article_args.add_argument('body', type=str, required=True)

# comment args
comment_args = reqparse.RequestParser()
comment_args.add_argument('body', type=str, required=True)
