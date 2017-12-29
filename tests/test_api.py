import unittest
from app import create_app, db, user_datastore
from base64 import b64encode
import json
from app.models import User, Role, Post, Category, Comment
from flask_security.utils import hash_password, login_user


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_as_admin(self):
        user = user_datastore.create_user(email='test@example.com', name='test', password=hash_password('123456'))
        role = user_datastore.create_role(name='admin')
        user_datastore.add_role_to_user(user, role)
        db.session.commit()
        response = self.client.post(
            '/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com', 
                    'password': '123456',
                }))
        json_response = json.loads(response.get_data(as_text=True))
        return json_response

    def test_register_success(self):
        response = self.client.post(
            '/users',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com', 
                    'name': 'test',
                    'password': '123456'
                }))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['name'], 'test')
    
    def test_register_fail(self):
        user = user_datastore.create_user(email='test@example.com', name='test', password='123456')
        db.session.commit()
        response = self.client.post(
            '/users',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com', 
                    'name': 'test',
                    'password': '123456'
                }))
        self.assertEqual(response.status_code, 401)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['code'], 401.3)

    def test_login_success(self):
        user = user_datastore.create_user(email='test@example.com', name='test', password=hash_password('123456'))
        db.session.commit()
        response = self.client.post(
            '/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com', 
                    'password': '123456',
                }))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['name'], 'test')

    def test_login_fail(self):
        user = user_datastore.create_user(email='test@example.com', name='test', password=hash_password('123456'))
        db.session.commit()
        response = self.client.post(
            '/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com', 
                    'password': '1',
                }))
        self.assertEqual(response.status_code, 401)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['code'], 401.1)
        response = self.client.post(
            '/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@edmple.com', 
                    'password': '123456',
                }))
        self.assertEqual(response.status_code, 401)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['code'], 401.2)
    
    def test_logout(self):
        user = user_datastore.create_user(email='test@example.com', name='test', password=hash_password('123456'))
        db.session.commit()
        response = self.client.post(
            '/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com', 
                    'password': '123456',
                }))
        json_response = json.loads(response.get_data(as_text=True))
 
        response = self.client.delete(
            '/sessions',
            headers={'Content-Type': 'application/json', 'Authorization': json_response['key']},
        )
        self.assertEqual(response.status_code, 204)

    def test_add_article(self):
        json_response = self.login_as_admin()
        response = self.client.post(
            '/posts',
            headers={'Content-Type': 'application/json', 'Authorization': json_response['key']},
            data=json.dumps({
                    'title': 'test', 
                    'desc': 'hello',
                    'body': 'ni hao',
                    'category': 'python'
                })
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['title'], 'test')
    
    def test_modify_article(self):
        json_response = self.login_as_admin()
        new_response = self.client.post(
            '/posts',
            headers={'Content-Type': 'application/json', 'Authorization': json_response['key']},
            data=json.dumps({
                    'title': 'test', 
                    'desc': 'hello',
                    'body': 'ni hao',
                    'category': 'python'
                })
        )
        response = self.client.put(
            'posts/{}'.format(json.loads(new_response.get_data(as_text=True))['id']),
            headers={'Content-Type': 'application/json', 'Authorization': json_response['key']},
            data=json.dumps({
                    'title': 'test2', 
                    'desc': 'hello',
                    'body': 'ni hao',
                    'category': 'python'
                })
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['title'], 'test2')

    def test_get_article(self):
        json_response = self.login_as_admin()
        new_response = self.client.post(
            '/posts',
            headers={'Content-Type': 'application/json', 'Authorization': json_response['key']},
            data=json.dumps({
                    'title': 'test', 
                    'desc': 'hello',
                    'body': 'ni hao',
                    'category': 'python'
                })
        )
        response = self.client.get(
            'posts/{}'.format(json.loads(new_response.get_data(as_text=True))['id']),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['title'], 'test')

        response = self.client.get(
            'posts/454353',
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))

    def test_delete_article(self):
        json_response = self.login_as_admin()
        new_response = self.client.post(
            '/posts',
            headers={'Content-Type': 'application/json', 'Authorization': json_response['key']},
            data=json.dumps({
                    'title': 'test', 
                    'desc': 'hello',
                    'body': 'ni hao',
                    'category': 'python'
                })
        )
        response = self.client.delete(
            'posts/{}'.format(json.loads(new_response.get_data(as_text=True))['id']),
            headers={'Content-Type': 'application/json', 'Authorization': json_response['key']}
        )
        self.assertEqual(response.status_code, 204)

    def test_add_comment(self):
        json_response = self.login_as_admin()
        new_response = self.client.post(
            '/posts',
            headers={'Content-Type': 'application/json', 'Authorization': json_response['key']},
            data=json.dumps({
                    'title': 'test', 
                    'desc': 'hello',
                    'body': 'ni hao',
                    'category': 'python'
                })
        )
        response = self.client.post(
            '/comments/{}'.format(json.loads(new_response.get_data(as_text=True))['id']),
            headers={'Content-Type': 'application/json', 'Authorization': json_response['key']},
            data=json.dumps({
                    'body': 'ni hao',
                })
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['body'], 'ni hao')