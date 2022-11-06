import sys
from random import randint
from database import execute_script, post

algorithm = ['detectron2_db_test', 'openpose_db_test', 'megadetector_db_test']


def init():
    execute_script('initialiser.sql')


def populate():
    for i in range(12**3):
        parameter = {}
        parameter['id'] = None
        parameter['algorithm'] = gen_algorithm()
        parameter['dataset'] = None
        parameter['roc_ys'] = gen_ys()
        parameter['actual_0'] = gen_positive()
        parameter['actual_1'] = gen_positive()
        parameter['predicted_0'] = gen_positive()
        parameter['predicted_1'] = gen_positive()
        parameter['f1_score'] = gen_fraction()
        parameter['datetime'] = None
        post(parameter)


def gen_algorithm():
    return algorithm[randint(0, len(algorithm) - 1)]


def gen_bit():
    return randint(0, 1)


def gen_positive(limit=2**63 - 1):
    return randint(0, limit)


def gen_fraction(resolution=12**7):
    return randint(0, resolution) / resolution


def gen_ys(minimum=12, maximum=144):
    return [gen_fraction() for _ in range(randint(minimum, maximum))]


if __name__ == '__main__':
    '''
        args:
         - init: run initialiser.sql and add one row from initialiser.sql
         - populate: add multiple row entries randomly generated
    '''
    if len(sys.argv) < 2:
        raise Exception('Please provide at least 1 argument')
    expected = ['init', 'populate']
    callback = sys.argv[1]
    if callback not in expected:
        raise Exception(f'Argument {callback} not in expected {expected}')
    eval(f'{callback}()')
