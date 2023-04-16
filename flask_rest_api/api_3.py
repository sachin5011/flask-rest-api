"""
implimentation of flask apiu using sqlite
"""

from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, reqparse, abort
# importing flask sqlalchemy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

# sqlalchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


# Post arguments
task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='Task is required', required=True)
task_post_args.add_argument('summary', type=str, help='Summary is required', required=True)

# put arguments
task_put_args = reqparse.RequestParser()
task_put_args.add_argument('task')
task_put_args.add_argument('summary')


# creating DB Model for out todo with fields as id, task and summary
class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(500))

# This will create atable in the database with following columns
# db.create_all()

# mimicing the databse to python dictonaries
resource_field = {
    'id' : fields.Integer,
    'task' : fields.String,
    'summary': fields.String
}

class AllToDos(Resource):
    @marshal_with(resource_field)
    def get(self):
        todo = ToDoModel.query.all()
        return todo

class ToDo(Resource):
    @marshal_with(resource_field)
    def get(self, todo_id):
        todo = ToDoModel.query.filter_by(id=todo_id)
        return todo
    
    @marshal_with(resource_field)
    def post(self,todo_id):
        args = task_post_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409, message='Task already exists')
        todo = ToDoModel(id=todo_id, task=args['task'],summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201
    
    @marshal_with(resource_field)
    def put(self, todo_id):
        args = task_put_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(409, message="Task does not exists")
        if args['task']:
            task.task = args['task']
        if args['summary']:
            task.summary = args['summary']
        db.session.commit()
        return task
    
    def delete(self, todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        db.session.commit()
        return 'Task deleted', 204

api.add_resource(AllToDos, "/alltodos")
api.add_resource(ToDo, '/todo/<int:todo_id>')
if __name__ == "__main__":
    app.run(debug=True)