from collections import OrderedDict

from marshmallow import ValidationError

from .dao import ToDoDao
from .validators import ToDoCreateValidator


class ToDoController:
    def __init__(self):
        self.dao = ToDoDao()

    def add_todo(self, data):
        validator = ToDoCreateValidator()
        try:
            validated_data = validator.load(data)
        except ValidationError as exc:
            raise exc
        return self.dao.add_one(validated_data)

    def list_all(self):
        return self._make_ordered_dicts(self.dao.list_all())

    def get_one(self, _id):
        return self._make_ordered_dicts([self.dao.get_one(_id)])[0]

    def delete_one(self, _id):
        return self.dao.delete_one(_id)

    def update_one(self, _id, data):
        if not data:
            raise ValidationError('data argument is mandatory for update.')

        return self.dao.update_one(_id, data)

    @staticmethod
    def _make_ordered_dicts(results):
        ordered_dicts = []
        for r in results:
            ordered_dicts.append(
                OrderedDict([
                    ('id', r.get('id')),
                    ('title', r.get('title')),
                    ('description', r.get('description'))
                ])
            )
        return ordered_dicts
