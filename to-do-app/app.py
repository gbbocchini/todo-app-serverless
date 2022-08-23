from chalice import Chalice, BadRequestError
from chalicelib.controller import ToDoController
from chalicelib.validators import CrudSuccessMsgs, CrudErrorMsgs

app = Chalice(app_name='to-do-app')


@app.route('/v1/todo', methods=['PUT'], cors=True)
def add_todo():
    data = app.current_request.json_body
    try:
        ToDoController().add_todo(data)
        return CrudSuccessMsgs.CREATE
    except Exception:
        raise BadRequestError(CrudErrorMsgs.CREATE)


@app.route('/v1/todo', methods=['GET'], cors=True)
def list_todos():
    try:
        results = ToDoController().list_all()
        if not results:
            results = []
        return results
    except Exception:
        raise BadRequestError(CrudErrorMsgs.LIST)


@app.route('/v1/todo/{todo_id}', methods=['GET'], cors=True)
def get_todo(todo_id):
    try:
        result = ToDoController().get_one(todo_id)
        if not result:
            raise BadRequestError(CrudErrorMsgs.GET)
        return result
    except Exception:
        raise BadRequestError(CrudErrorMsgs.GET)


@app.route('/v1/todo/{todo_id}', methods=['DELETE'], cors=True)
def delete_todo(todo_id):
    try:
        ToDoController().delete_one(todo_id)
        return CrudSuccessMsgs.DELETE
    except Exception:
        raise BadRequestError(CrudErrorMsgs.DELETE)


@app.route('/v1/todo/{todo_id}', methods=['PUT'], cors=True)
def update_todo(todo_id):
    data = app.current_request.json_body
    try:
        ToDoController().update_one(todo_id, data)
        return CrudSuccessMsgs.UPDATE
    except Exception:
        raise BadRequestError(CrudErrorMsgs.UPDATE)
