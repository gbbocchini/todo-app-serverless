import boto3
import os


def get_db():
    db = boto3.resource('dynamodb').Table(os.environ.get('APP_TABLE_NAME'))
    return db
