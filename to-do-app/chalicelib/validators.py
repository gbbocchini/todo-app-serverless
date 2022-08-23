from marshmallow import Schema, fields


class ToDoCreateValidator(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)


class CrudErrorMsgs:
    LIST = 'There was an error loading the To-Do objects.'
    CREATE = 'There was an error while creating the To-Do object.'
    GET = 'There was an error loading the To-Do object.'
    UPDATE = 'There was an error while updating a To-Do object.'
    DELETE = 'There has been an error while deleting the To-Do object.'


class CrudSuccessMsgs:
    CREATE = {'message': 'To-Do object created successfully.'}
    UPDATE = {'message': 'To-Do object updated successfully.'}
    DELETE = {'message': 'To-Do object deleted successfully.'}
