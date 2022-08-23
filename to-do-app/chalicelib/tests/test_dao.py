import mock
from ..dao import ToDoDao


@mock.patch('chalicelib.dao.get_db')
def test_list_all(mocked_get_db):
    mocked_get_db().scan.return_value = {'Items': 'this is items'}
    result = ToDoDao().list_all()
    mocked_get_db().scan.assert_called_once()
    assert result == 'this is items'


@mock.patch('chalicelib.dao.get_db')
def test_get_one(mocked_get_db):
    mocked_get_db().get_item.return_value = {'Item': 'this is item'}
    result = ToDoDao().get_one(_id='test_id')
    mocked_get_db().get_item.assert_called_once_with(Key={'id': 'test_id'})
    assert result == 'this is item'


@mock.patch('chalicelib.dao.uuid')
@mock.patch('chalicelib.dao.get_db')
def test_add_one_is_update_false(mocked_get_db, mocked_uuid):
    mocked_uuid.uuid4.return_value = 'this is uuid'
    mocked_data = {
        'title': 'this is title',
        'description': 'this is desc'
    }
    result = ToDoDao().add_one(data=mocked_data)
    mocked_uuid.uuid4.assert_called_once()
    mocked_get_db().put_item.assert_called_once_with(
        Item={
            'id': 'this is uuid',
            'title': 'this is title',
            'description': 'this is desc'
        }
    )
    assert result == 'this is uuid'


@mock.patch('chalicelib.dao.uuid')
@mock.patch('chalicelib.dao.get_db')
def test_add_one_is_update_true(mocked_get_db, mocked_uuid):
    mocked_data = {
        'id': 'this is id',
        'title': 'this is title',
        'description': 'this is desc'
    }
    result = ToDoDao().add_one(data=mocked_data, is_update=True)
    mocked_uuid.uuid4.assert_not_called()
    mocked_get_db().put_item.assert_called_once_with(
        Item={
            'id': 'this is id',
            'title': 'this is title',
            'description': 'this is desc'
        }
    )
    assert result == 'this is id'


@mock.patch('chalicelib.dao.get_db')
def test_delete_one(mocked_get_db):
    mocked_get_db().delete_item.return_value = 'test return'
    result = ToDoDao().delete_one('this is id')
    mocked_get_db().delete_item.assert_called_once_with(Key={'id': 'this is id'})
    assert result == 'test return'


@mock.patch('chalicelib.dao.ToDoDao.add_one')
@mock.patch('chalicelib.dao.ToDoDao.get_one')
@mock.patch('chalicelib.dao.get_db')
def test_update_one(mocked_get_db, mocked_get_one, mocked_add_one):
    mocked_get_one.return_value = {
        'id': 'this is id',
        'title': 'this is title',
        'description': 'this is desc'
    }
    mocked_add_one.return_value = 'this is return'
    mocked_data = {
        'description': 'updated desc'
    }
    result = ToDoDao().update_one('this is id', mocked_data)
    mocked_get_one.assert_called_once_with('this is id')
    mocked_add_one.assert_called_once_with({
        'id': 'this is id',
        'title': 'this is title',
        'description': 'updated desc'
    }, is_update=True)
    assert result == 'this is return'
