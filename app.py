import cx_Oracle
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import uuid


# declare constants for flask app
HOST = '0.0.0.0'
PORT = 5000

# initialize flask application
app = Flask(__name__)
api = Api(app)

# automonous data warehouse connection constants
# update below with your db credentials
# add wallet files to wallet folder
DB = "orcl_high"
DB_USER = "admin"
DB_PASSWORD = "Citi21direct"


# api endpoint returning version of database from automonous data warehouse
@app.route('/api/version')
def version():
    conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB)
    return jsonify(status='success', db_version=conn.version)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Titanic"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###
    

class Passengers(Resource):
    def get(self):
        conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB)
        cursor = conn.cursor()
        statement = 'select * from titanic'
        cursor.execute(statement)
        res = cursor.fetchall()
        items = [dict(zip([key[0] for key in cursor.description], row)) for row in res]
        return jsonify(items)
        

class Passenger_UUID(Resource):
    def get(self, UUID):
        conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB)
        cursor = conn.cursor()
        statement = 'select * from titanic where UUID = :UUID' 
        cursor.execute(statement, {'UUID' :UUID})
        res = cursor.fetchall()
        items = [dict(zip([key[0] for key in cursor.description], row)) for row in res]
        return jsonify(items)



class PassengersPost(Resource):
    def post(self):
        conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB)
        cursor = conn.cursor()
        json_obj = request.get_json()
        survived = json_obj['survived']
        passengerClass = json_obj['passengerClass']
        name = json_obj['name']
        sex = json_obj['sex']
        age = json_obj['age']
        siblingsOrSpousesAboard = json_obj['siblingsOrSpousesAboard']
        parentsOrChildrenAboard = json_obj['parentsOrChildrenAboard']
        fare = json_obj['fare']
        UUID = uuid.uuid1()
        statement = 'insert into titanic values (:1, :2, :3, :4, :5, :6, :7, :8, :9)'
        cursor.execute(statement, (survived, passengerClass, name, sex, age, siblingsOrSpousesAboard, parentsOrChildrenAboard, fare, str(UUID)))
        cursor.close()
        conn.commit()
        conn.close()
        return jsonify(dict(request.json, uuid=UUID))
        

class PassengersPut(Resource):
    def put(self, UUID):
        conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB)
        cursor = conn.cursor()
        json_obj = request.get_json()
        survived = json_obj['survived']
        passengerClass = json_obj['passengerClass']
        name = json_obj['name']
        sex = json_obj['sex']
        age = json_obj['age']
        siblingsOrSpousesAboard = json_obj['siblingsOrSpousesAboard']
        parentsOrChildrenAboard = json_obj['parentsOrChildrenAboard']
        fare = json_obj['fare']
        statement = 'update titanic set survived=:1, Pclass=:2, name=:3, sex=:4, age=:5, siblingsOrSpousesAboard=:6, parentsOrChildrenAboard=:7, fare=:8 where UUID =:UUID' 
        cursor.execute(statement, (survived, passengerClass, name, sex, age, siblingsOrSpousesAboard, parentsOrChildrenAboard, fare, UUID))
        cursor.close()
        conn.commit()
        conn.close()



class PassengersDel(Resource):
    def delete(self, UUID):
        conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB)
        cursor = conn.cursor()
        statement = 'delete from titanic where UUID = :UUID'
        cursor.execute(statement, {'UUID' :UUID})
        cursor.close()
        conn.commit()
        conn.close()


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

api.add_resource(Passengers, '/people', methods = ['GET'])
api.add_resource(Passenger_UUID, '/people/<UUID>', methods = ['GET'])
api.add_resource(PassengersPost, '/people/', methods = ['POST'])
api.add_resource(PassengersPut, '/people/<UUID>', methods = ['PUT'])
api.add_resource(PassengersDel, '/people/<UUID>', methods = ['DELETE'])

if __name__ == '__main__':
    app.run(host=HOST, debug=True, port=PORT)
