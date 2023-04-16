from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Helloworld(Resource):
    def get(self):
        return {"data": "Hello World"}
    
class Helloname(Resource):
    def get(self, name):
        return {"Name" : "Hello {}".format(name)}
    
# for every single class we have to define its own end point
# for class Helloworld
api.add_resource(Helloworld, '/helloworld')
# for class Helloname
api.add_resource(Helloname, '/helloworld/<string:name>')



if __name__ == "__main__":
    app.run(debug=True)