import json
import unittest

from flask import Response
from sqlalchemy import desc

from flask_poetry_api import app, db
from flask_poetry_api.models.course_model import CourseModel
from flask_poetry_api.models.user_model import UserModel
from flask_poetry_api.repositories.user_repository import UserRepository
from flask_poetry_api.services.course_service import CourseService


class AppTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_1_register(self):
        response: Response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(
                dict(
                    name='administrador',
                    email='admin@gmail.com',
                    password='administrador2023',
                )
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('application/json', response.content_type)

        result: object = json.loads(response.data)

        self.assertEqual(result.get('name'), 'administrador')
        self.assertEqual(result.get('email'), 'admin@gmail.com')

        with app.app_context():
            last_user: int = self.last_register_user()
            user_db: UserModel = UserRepository.find_by_id(last_user)

            self.assertEqual(user_db.id, last_user)

    def test_2_login(self):
        response: Response = self.client.post(
            '/api/v1/users/login/',
            data=json.dumps(
                dict(
                    email='admin@gmail.com',
                    password='administrador2023',
                )
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)

    def test_3_login_error_401(self):
        response: Response = self.client.post(
            '/api/v1/users/login/',
            data=json.dumps(
                dict(
                    email='test@gmail.com',
                    password='administrador2023',
                )
            ),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn('application/json', response.content_type)

    def test_4_refresh(self):
        response: object = self.get_token()

        response_refresh: Response = self.client.post(
            f"/api/v1/users/token/refresh?authorization={response.get('refresh_token')}/",
            data=json.dumps(
                dict(
                    email='admin@gmail.com',
                    password='administrador2023',
                )
            ),
            content_type='application/json',
        )

        self.assertEqual(response_refresh.status_code, 200)
        self.assertIn('application/json', response_refresh.content_type)

    def test_5_create_course(self):
        response: object = self.get_token()

        response_course: Response = self.client.post(
            '/api/v1/courses/',
            data=json.dumps(
                dict(
                    name='curso de python',
                    description='formação em python',
                )
            ),
            content_type='application/json',
            headers={
                'Authorization': f"Bearer {response.get('access_token')}"
            },
        )

        self.assertEqual(response_course.status_code, 201)
        self.assertIn('application/json', response_course.content_type)

        result_course: object = json.loads(response_course.data)

        self.assertEqual(result_course.get('name'), 'curso de python')
        self.assertEqual(
            result_course.get('description'), 'formação em python'
        )

    def test_6_all_course(self):
        response: object = self.get_token()

        response: Response = self.client.get(
            '/api/v1/courses/',
            content_type='application/json',
            headers={
                'Authorization': f"Bearer {response.get('access_token')}"
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)

        result: object = json.loads(response.data)
        count_courses: int = len(result)

        self.assertEqual(len(result), count_courses)

    def test_7_show_course(self):
        last_course: int = self.last_register_course()
        response: object = self.get_token()

        response_course: Response = self.client.get(
            f'/api/v1/courses/{last_course}/',
            content_type='application/json',
            headers={
                'Authorization': 'Bearer ' + response.get('access_token')
            },
        )

        self.assertEqual(response_course.status_code, 200)
        self.assertIn('application/json', response_course.content_type)

        result: object = json.loads(response_course.data)

        self.assertEqual(result.get('id'), last_course)

    def test_8_show_course_error_404(self):
        with app.app_context():
            data = json.dumps(
                dict(
                    name='curso de php',
                    description='formação em php',
                )
            )

            response_show: Response = CourseService.show_course(1000)
            self.assertEqual(response_show.status_code, 404)

            response_update: Response = CourseService.update_course(1000, data)
            self.assertEqual(response_update.status_code, 404)

            response_delete: Response = CourseService.delete_course(1000)
            self.assertEqual(response_delete.status_code, 404)

    def test_9_update_course(self):
        last_course: int = self.last_register_course()
        response: object = self.get_token()

        response_course: Response = self.client.put(
            f'/api/v1/courses/{last_course}/',
            data=json.dumps(
                dict(
                    name='curso de php',
                    description='formação em php',
                )
            ),
            content_type='application/json',
            headers={
                'Authorization': f"Bearer {response.get('access_token')}"
            },
        )

        self.assertEqual(response_course.status_code, 202)
        self.assertIn('application/json', response_course.content_type)

        result_course: object = json.loads(response_course.data)

        self.assertEqual(result_course.get('name'), 'curso de php')
        self.assertEqual(result_course.get('description'), 'formação em php')

    def test_10_delete_course(self):
        last_course: int = self.last_register_course()
        response: object = self.get_token()

        response_course: Response = self.client.delete(
            f'/api/v1/courses/{last_course}/',
            content_type='application/json',
            headers={
                'Authorization': f"Bearer {response.get('access_token')}"
            },
        )

        self.assertEqual(response_course.status_code, 204)
        self.assertIn('application/json', response_course.content_type)

    def get_token(self) -> object:
        response: Response = self.client.post(
            '/api/v1/users/login/',
            data=json.dumps(
                dict(
                    email='admin@gmail.com',
                    password='administrador2023',
                )
            ),
            content_type='application/json',
        )

        return json.loads(response.data)

    def last_register_user(self) -> int:
        with app.app_context():
            model_db: UserModel = (
                db.session.query(UserModel)
                .order_by(desc(UserModel.id))
                .first()
            )
            return model_db.id

    def last_register_course(self) -> int:
        with app.app_context():
            model_db: CourseModel = (
                db.session.query(CourseModel)
                .order_by(desc(CourseModel.id))
                .first()
            )
            return model_db.id
