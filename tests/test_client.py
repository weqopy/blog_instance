import unittest
import re
from flask import url_for
from app import create_app, db
from app.models import User, Role


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        data = response.get_data(as_text=True)
        self.assertTrue('Stranger' in data)

    def test_register_and_login(self):
        response = self.client.post(url_for('auth.register'), data={
            'email': 'john@example.com',
            'username': 'john123',
            'password': 'catcat',
            'confirm_pw': 'catcat'
        })
        self.assertTrue(response.status_code == 302)

        response = self.client.post(url_for('auth.login'), data={
            'username': 'john123',
            'password': 'catcat'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('john123', data))
        self.assertTrue('请查收邮件确认账户信息。' in data)

        user = User.query.filter_by(username='john123').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('账户已确认' in data)

        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('Stranger' in data)
