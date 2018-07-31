import os
from io import BytesIO
import unittest
from app import create_app, db, user_datastore
import json
from flask_security.utils import hash_password
import shutil


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
        if os.path.exists(self.app.config['UPLOAD_FOLDER']):
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'])

    def login_as_admin(self):
        user = user_datastore.create_user(email='test@example.com', name='test', password=hash_password('123456'))
        role = user_datastore.create_role(name='admin')
        user_datastore.add_role_to_user(user, role)
        db.session.commit()
        response = self.client.post(
            '/api/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com',
                    'password': '123456',
                }))
        json_response = json.loads(response.get_data(as_text=True))
        return json_response

    def upload_photo(self):
        json_response = self.login_as_admin()
        response = self.client.post(
            '/api/photos',
            headers={'Content-Type': 'multipart/form-data', 'Authorization': json_response['token']},
            data = dict(
                file=(BytesIO(b'my file contents'), "test.png"),
            )
        )
        return response, json_response

    def add_post(self):
        response, json_response = self.upload_photo()
        new_response = json.loads(response.get_data(as_text=True))
        img_id = new_response['id']
        response = self.client.post(
            '/api/posts',
            headers={'Content-Type': 'application/json', 'Authorization': json_response['token']},
            data=json.dumps({
                    'title': 'test',
                    'desc': 'hello',
                    'body': 'ni hao',
                    'category': 'python',
                    'img_id': img_id
                })
        )
        return response, json_response

    def test_register_success(self):
        response = self.client.post(
            '/api/users',
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
        user_datastore.create_user(email='test@example.com', name='test', password='123456')
        db.session.commit()
        response = self.client.post(
            '/api/users',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com',
                    'name': 'test',
                    'password': '123456'
                }))
        self.assertEqual(response.status_code, 409)

    def test_login_success(self):
        user_datastore.create_user(email='test@example.com', name='test', password=hash_password('123456'))
        db.session.commit()
        response = self.client.post(
            '/api/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com',
                    'password': '123456',
                }))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['name'], 'test')

    def test_login_fail(self):
        user_datastore.create_user(email='test@example.com', name='test', password=hash_password('123456'))
        db.session.commit()
        response = self.client.post(
            '/api/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com',
                    'password': '1',
                }))
        self.assertEqual(response.status_code, 411)
        response = self.client.post(
            '/api/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@edmple.com',
                    'password': '123456',
                }))
        self.assertEqual(response.status_code, 410)

    def test_logout(self):
        user_datastore.create_user(email='test@example.com', name='test', password=hash_password('123456'))
        db.session.commit()
        response = self.client.post(
            '/api/sessions',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                    'email': 'test@example.com',
                    'password': '123456',
                }))
        json_response = json.loads(response.get_data(as_text=True))

        response = self.client.delete(
            '/api/sessions',
            headers={'Content-Type': 'application/json', 'Authorization': json_response['token']},
        )
        self.assertEqual(response.status_code, 204)

    def test_add_article(self):
        response, _ = self.add_post()
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['title'], 'test')

    def test_modify_article(self):
        new_response, json_response = self.add_post()
        response = self.client.put(
            '/api/posts/{}'.format(json.loads(new_response.get_data(as_text=True))['id']),
            headers={'Content-Type': 'application/json', 'Authorization': json_response['token']},
            data=json.dumps({
                    'title': 'test2',
                    'desc': 'hello',
                    'body': 'ni hao',
                    'category': 'python',
                    'img_id': json.loads(new_response.get_data(as_text=True))['id']
                })
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['title'], 'test2')

    def test_get_article(self):
        new_response, json_response = self.add_post()
        response = self.client.get(
            '/api/posts/{}'.format(json.loads(new_response.get_data(as_text=True))['id']),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['title'], 'test')

        response = self.client.get(
            '/api/posts/454353',
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 410)

    def test_delete_article(self):
        new_response, json_response = self.add_post()
        response = self.client.delete(
            '/api/posts/{}'.format(json.loads(new_response.get_data(as_text=True))['id']),
            headers={'Content-Type': 'application/json', 'Authorization': json_response['token']}
        )
        self.assertEqual(response.status_code, 204)
        img = json.loads(new_response.get_data(as_text=True))['img']
        path = os.path.join(self.app.config['UPLOAD_FOLDER'], img['filename'])
        self.assertFalse(os.path.exists(path))

    def test_add_comment(self):
        new_response, json_response = self.add_post()
        response = self.client.post(
            '/api/comments/{}'.format(json.loads(new_response.get_data(as_text=True))['id']),
            headers={'Content-Type': 'application/json', 'Authorization': json_response['token']},
            data=json.dumps({
                    'body': 'ni hao',
                })
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['body'], 'ni hao')

    def test_upload_file(self):
        response, _ = self.upload_photo()
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['url'], '/api/photos/test.png')
        response = self.client.get(
            '/api/photos/test.png',
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_photo(self):
        response, json_response = self.upload_photo()
        new_response = json.loads(response.get_data(as_text=True))
        response = self.client.delete(
            '/api/photos/{}'.format(new_response['filename']),
            headers={'Content-Type': 'application/json', 'Authorization': json_response['token']},
        )
        self.assertEqual(response.status_code, 201)
