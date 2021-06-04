import os
import re

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources import res_credentials

from security import authenticate, identity
from resources.res_credentials import UserRegister,DBInflux,DataFromSystem

app = Flask(__name__)

app.config['DEBUG'] = True

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(uri, 'sqlite:///data.db')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///User_DBcredentials.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'Alubel2021'
api = Api(app)

# CREATE TABLES DB USER AND DATABASES 
# @app.before_first_request
# def create_tables():
#     db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth

# ADD RESOURCES 
## USER 
api.add_resource(UserRegister, '/register')

## INFLUXDB Credentials
api.add_resource(DBInflux, '/DBTimeSeries/<string:Project_name>')

# QUERY
api.add_resource(DataFromSystem, '/PostJson/<string:Project_name>')
# api.add_resource(GetBuildingTypeClass, '/GetBuildingTypeClass')
# api.add_resource(GetSensorClass, '/GetSensorClass')
# api.add_resource(GetSensorSpace, '/GetSensorSpace')
# api.add_resource(GetSensorUID, '/GetSensorUIID')
# api.add_resource(GetSensorInfo, '/GetSensorInfo')
# api.add_resource(Get_RoomSensor, '/Get_RoomSensor')
# api.add_resource(GetTimeSeriesData, '/GetTimeSeriesData')
# api.add_resource(QueryTot, '/QueryTot')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
        
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
    
    app.run(port=5000, debug=True)
