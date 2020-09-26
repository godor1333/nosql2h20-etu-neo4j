from flask import Flask
from flask_restful import Api

from uemployees.db import init_db
from uemployees.views import GroupView


init_db()

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True

api = Api(app)


api.add_resource(GroupView, '/groups/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
