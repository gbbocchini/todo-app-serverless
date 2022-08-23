import mock

from ..db import get_db


@mock.patch('chalicelib.db.os')
@mock.patch('chalicelib.db.boto3')
def test_get_db(mocked_boto, mocked_os):
    mocked_os.environ = {'APP_TABLE_NAME': 'test table'}
    result = get_db()
    mocked_boto.assert_has_calls([
        mock.call.resource('dynamodb'),
        mock.call.resource('dynamodb').Table('test table')
    ])
    assert result == mocked_boto.resource().Table.return_value
