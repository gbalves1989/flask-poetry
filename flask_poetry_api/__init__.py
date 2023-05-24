from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_openapi3 import APIBlueprint, HTTPBearer, Info, OpenAPI
from flask_sqlalchemy import SQLAlchemy

info = Info(
    title='Flask Poetry API',
    version='1.0.0',
    termsOfService='http://example.com/terms/',
    contact={
        'name': 'API Support',
        'url': 'http://www.example.com/support',
        'email': 'support@example.com',
    },
    license={
        'name': 'Apache 2.0',
        'url': 'https://www.apache.org/licenses/LICENSE-2.0.html',
    },
)

security_schemes = {'jwt': HTTPBearer(bearerFormat='JWT')}
security = [{'jwt': []}]

app = OpenAPI(
    __name__,
    info=info,
    servers=[{'url': 'http://localhost:5000'}],
    security_schemes=security_schemes,
)
app.config.from_object('config')

CORS(
    app,
    origins=['http://127.0.0.1:5000'],
)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

api = APIBlueprint('flask-poetry', __name__)
jwt = JWTManager(app)

from flask_poetry_api.routes import course_route, user_route

app.register_api(api)
