import sqlite3
import query
from datetime import datetime
from uuid import uuid4

database__name = 'api.db'


def connect():
    connection = sqlite3.connect(database__name)
    connection.row_factory = sqlite3.Row
    return connection


def objectify(row):
    obj = dict(row)
    if 'roc_ys' in obj:
        obj['roc_ys'] = list(map(float, obj['roc_ys'].split(',')))
        
    if 'roc_xs' in obj:
        obj['roc_xs'] = list(map(float, obj['roc_xs'].split(',')))
    return obj


def execute(query, parameter=None):
    connection = connect()
    rows = [objectify(row) for row in (connection.execute(query) if parameter is None else connection.execute(query, parameter))]
    connection.commit()
    connection.close()
    return rows


def execute_script(filepath):
    with open(filepath, 'r') as script:
        connection = connect()
        connection.executescript(script.read())
        connection.close()
    return


def get(offset, limit):
    parameter = {}
    parameter['limit'] = limit
    parameter['offset'] = offset
    return execute(query.get, parameter)

def get_all():
    return execute(query.get_all)

def get_by_id(uuid):
    parameter = {'id': uuid}
    rows = execute(query.get_by_id, parameter)
    return rows[0] if rows else None


def post(parameter):
    new_id = str(uuid4() if parameter['id'] is None else parameter['id'])
    parameter['id'] = new_id
    parameter['roc_ys'] = ','.join(map(str, parameter['roc_ys']))
    parameter['roc_xs'] = ','.join(map(str, parameter['roc_xs']))
    parameter['datetime'] = datetime.now() if parameter['datetime'] is None else parameter['datetime']
    execute(query.post, parameter)
    return [new_id]


def delete_by_id(uuid):
    parameter = {'id': uuid}
    return execute(query.delete_by_id, parameter)
