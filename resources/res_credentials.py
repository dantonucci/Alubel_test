from flask_restful import Resource, reqparse
from models.credentials import UserModel, InfluxDB
from flask import request, jsonify
import json
from models.JsonInflux import FromJson_to_Database

from flask_jwt import jwt_required


# USERNAME AND PASSWORD 
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201
    
 
 
# TIMESERIES DATABASE    
class DBInflux(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('host_DB',
                        type=str,
                        required=True,
                        help="Every item needs a store_id."
                        )
    parser.add_argument('port_DB',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
                        )
    parser.add_argument('username_DB',
                        type=str,
                        required=True,
                        help="Every item needs a store_id."
                        )
    parser.add_argument('password_DB',
                        type=str,
                        required=True,
                        help="Every item needs a store_id."
                        )
    parser.add_argument('database_DB',
                        type=str,
                        required=True,
                        help="Every item needs a store_id."
                        )

    @jwt_required()
    def get(self,Project_name):
        ''' 
        Check database onf INfluxdb credentials available
        '''
        item = InfluxDB.Get_DB_Info(Project_name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, Project_name):
        ''' 
        Save credentials of DB timseries.
        '''
        if InfluxDB.find_database(Project_name):
            return {'message': "An item with name '{}' already exists.".format(Project_name)}, 400

        data = DBInflux.parser.parse_args()

        item = InfluxDB(Project_name, **data)

        try:
            item.save_to_db()
        except:
            return ({"message": "An error occurred inserting the item."},
                    {'item': item.json(), 'data':data, "Project_name":Project_name}), 500
        # 
        return item.json(), 201

    @jwt_required()
    def delete(self, Project_name):
        ''' 
        Delete database credentials
        '''
        item = InfluxDB.find_database(Project_name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    # def put(self, Project_name):
    #     data = DBInflux.parser.parse_args()

    #     item = InfluxDB.find_database(Project_name)

    #     if item:
    #         item.price = data['price']
    #     else:
    #         item = InfluxDB(Project_name, **data)

    #     item.save_to_db()

    #     return item.json()

       
# POST JSON      
class DataFromSystem(Resource):  
    
    @jwt_required()
    def post(self,Project_name):
        
        Client = InfluxDB.db_connection(Project_name)
        content = request.get_json()
        Result = FromJson_to_Database(content,Client)
        
        return (json.dumps(Result))

    