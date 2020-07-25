import json
import pytest

import common.setenv
from api import app
from test.utils import (
  gen_apigw_event
)

def test_api_get_config_user():
  evt = gen_apigw_event('/config', 'GET', None, None, '127.0.0.2')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['MEDIA_BUCKET_URL'] is not None
  assert bdy['data']['USER_ROLE'] == 'USER'

def test_api_get_config_administrator():
  evt = gen_apigw_event('/config', 'GET', None, None, '127.0.0.1')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['MEDIA_BUCKET_URL'] is not None
  assert bdy['data']['USER_ROLE'] == 'ADMINISTRATOR'

def test_api_get_boards():
  evt = gen_apigw_event('/boards', 'GET', None, None)
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data'][0] is not None

def test_api_post_thread_png():
  evt = gen_apigw_event('/boards/1/threads', 'POST', {
    'message': 'test msg',
    'extension': 'png'
  }, None)
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '201'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['id'] is not None
