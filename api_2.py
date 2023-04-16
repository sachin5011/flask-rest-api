"""
====== implimentation of api using python dictonaries =======
"""




from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)


todos = {
    1:{"task":"task 1", "summary":"summary 1"},
    2:{'task':"task 2", 'summary' : "summary 2"}
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help="Task is required.", required=True)
task_post_args.add_argument('summary', type=str, help='Summary is required.', required=True)

# this class will give us all the todos from our database
class Listalltodos(Resource):
    def get(self):
        return todos
    

class ToDo(Resource):
    def get(self, todo_id):
        return todos[todo_id]
    
    def post(self, todo_id):
        args = task_post_args.parse_args()
        if todo_id in todos:
            abort(409,'Task Id already exists...')
        else:
            todos[todo_id] = {"task": args['task'], 'summary':args['summary']}
        return todos[todo_id]
        
        

# adding end point for class Listalltodos
api.add_resource(Listalltodos, '/alltodos')
# adding end point for class todo
api.add_resource(ToDo, '/ToDo/<int:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)

"""
http://127.0.0.1:5000/alltodos
http://127.0.0.1:5000/ToDo/
"""