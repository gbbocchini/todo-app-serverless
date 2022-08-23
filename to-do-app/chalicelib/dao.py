import uuid

from .db import get_db


class ToDoDao:
    def __init__(self):
        self.db = get_db()

    def list_all(self):
        result = self.db.scan()['Items']
        return result

    def get_one(self, _id):
        result = self.db.get_item(Key={'id': _id})['Item']
        return result

    def add_one(self, data, is_update=False):
        if not is_update:
            new_id = str(uuid.uuid4())
        else:
            new_id = data.get('id')
        self.db.put_item(Item={
            'id': new_id,
            'title': data.get('title', ''),
            'description': data.get('description')
        })
        return new_id

    def delete_one(self, _id):
        result = self.db.delete_item(Key={'id': _id})
        return result

    def update_one(self, _id, data):
        item = self.get_one(_id)
        if item:
            if data.get('title', ''):
                item['title'] = data.get('title')
            if data.get('description', ''):
                item['description'] = data.get('description')
        return self.add_one(item, is_update=True)
