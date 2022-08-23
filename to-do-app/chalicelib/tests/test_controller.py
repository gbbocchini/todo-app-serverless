from collections import OrderedDict

import mock
import pytest
from marshmallow import ValidationError

from ..controller import ToDoController


@mock.patch('chalicelib.controller.ToDoCreateValidator')
@mock.patch('chalicelib.controller.ToDoDao')
def test_add_todo_success(mocked_dao, mocked_validator):
    mocked_validator().load.return_value = 'validated'
    result = ToDoController().add_todo('this is arg')
    mocked_validator().load.assert_called_once_with('this is arg')
    mocked_dao().add_one.assert_called_once_with('validated')
    assert result == mocked_dao().add_one.return_value


@mock.patch('chalicelib.controller.ToDoCreateValidator')
@mock.patch('chalicelib.controller.ToDoDao')
def test_add_todo_fail(mocked_dao, mocked_validator):
    mocked_validator().load.side_effect = ValidationError('this is error')

    with pytest.raises(ValidationError, match='this is error'):
        result = ToDoController().add_todo('this is arg')
        mocked_validator().load.assert_called_once_with('this is arg')
        mocked_dao().add_one.assert_not_called()
        assert not result


@mock.patch('chalicelib.controller.ToDoController._make_ordered_dicts')
@mock.patch('chalicelib.controller.ToDoDao')
def test_list_all(mocked_dao, mocked_make_dicts):
    result = ToDoController().list_all()
    mocked_dao().list_all.assert_called_once()
    mocked_make_dicts.assert_called_once_with(
        mocked_dao().list_all.return_value
    )
    assert result == mocked_make_dicts.return_value


@mock.patch('chalicelib.controller.ToDoController._make_ordered_dicts')
@mock.patch('chalicelib.controller.ToDoDao')
def test_get_one(mocked_dao, mocked_make_dicts):
    result = ToDoController().get_one(_id='this is id')
    mocked_dao().get_one.assert_called_once_with('this is id')
    mocked_make_dicts.assert_called_once_with(
        [mocked_dao().get_one.return_value]
    )
    assert result == mocked_make_dicts.return_value[0]


@mock.patch('chalicelib.controller.ToDoDao')
def test_delete_one(mocked_dao):
    result = ToDoController().delete_one(_id='this is id')
    mocked_dao().delete_one.assert_called_once_with('this is id')
    assert result == mocked_dao().delete_one.return_value


@mock.patch('chalicelib.controller.ToDoDao')
def test_update_one_success(mocked_dao):
    mocked_data = {'title': 'test title', 'description': 'test desc'}
    result = ToDoController().update_one('this is id', mocked_data)
    mocked_dao().update_one.assert_called_once_with('this is id', mocked_data)
    assert result == mocked_dao().update_one.return_value


@mock.patch('chalicelib.controller.ToDoDao')
def test_update_one_fail_1(mocked_dao):
    mocked_data = {}

    with pytest.raises(ValidationError, match='data argument is mandatory for update.'):
        result = ToDoController().update_one('this is id', mocked_data)
        mocked_dao().update_one.assert_not_called()
        assert not result


@mock.patch('chalicelib.controller.ToDoDao')
def test_make_ordered_dicts(mocked_dao):
    mocked_data = [
        {
            'title': 'test',
            'id': '12',
            'description': 'test desc'
        },
        {
            'description': 'test',
            'title': 'title',
            'id': '1'
        }
    ]
    result = ToDoController()._make_ordered_dicts(mocked_data)
    assert result == [
        OrderedDict([
            ('id', '12'),
            ('title', 'test'),
            ('description', 'test desc')
        ]),
        OrderedDict([
            ('id', '1'),
            ('title', 'title'),
            ('description', 'test')
        ])
    ]

