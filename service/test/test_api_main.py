import json
import time
import pytest

import common.setenv
from api import app
from test.utils import (
  gen_apigw_event
)

def test_api_get_config_user():
  evt = gen_apigw_event('config', 'GET', None, None, '127.0.0.2')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['MEDIA_BUCKET_URL'] is not None
  assert bdy['data']['USER_ROLE'] == 'USER'

def test_api_get_config_administrator():
  evt = gen_apigw_event('config', 'GET', None, None, '127.0.0.1')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['MEDIA_BUCKET_URL'] is not None
  assert bdy['data']['USER_ROLE'] == 'ADMINISTRATOR'

def test_api_get_boards():
  evt = gen_apigw_event('/boards', 'GET')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data'][0] is not None

def test_api_post_thread_png():
  evt = gen_apigw_event('boards/1/threads', 'POST', {
    'message': 'test msg',
    'extension': 'png'
  }, None, '127.0.0.1')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '201'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['id'] is not None

  time.sleep(1.0)

def test_api_post_post_webp():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', {
    'message': 'test msg',
    'extension': 'webp'
  }, None, '127.0.0.2')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '201' 
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['id'] is not None

  time.sleep(1.0)

def test_api_post_post_noimg():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', {
    'message': 'test msg'
  }, None, '127.0.0.3')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '201'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['id'] is not None

  time.sleep(1.0)

def test_api_post_report():
  evt = gen_apigw_event('reports', 'POST', {
    'post_id': 2,
    'reason': 'test report'
  }, None, '127.0.0.2')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '201'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['id'] is not None

  time.sleep(1.0)

def test_api_delete_post():
  evt = gen_apigw_event('posts/2', 'DELETE', None, None, '127.0.0.2')
  res = app.lambda_handler(evt, '')

  assert res['statusCode'] == '200'

def test_api_post_thread_err_empty_body():
  evt = gen_apigw_event('boards/1/threads', 'POST', {}, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_thread_err_invalid_body_1():
  evt = gen_apigw_event('boards/1/threads', 'POST', {
    'message': '',
  }, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_thread_err_invalid_body_2():
  evt = gen_apigw_event('boards/1/threads', 'POST', {
    'extension': ''
  }, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_thread_err_invalid_body_3():
  evt = gen_apigw_event('boards/1/threads', 'POST', {
    'extension': 'not_a_valid_extension'
  }, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_post_err_empty_body():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', {}, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_post_err_invalid_body_1():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', {
    'message': ''
  }, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_post_err_invalid_body_2():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', {
    'extension': 'not_a_valid_extension'
  }, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_report_err_empty_body():
  evt = gen_apigw_event('reports', 'POST', {}, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_report_err_invalid_body_1():
  evt = gen_apigw_event('reports', 'POST', {
    'post_id': 0,
    'reason': 'valid test reason'
  }, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_report_err_invalid_body_2():
  evt = gen_apigw_event('reports', 'POST', {
    'post_id': 12491258
  }, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_report_err_invalid_body_3():
  evt = gen_apigw_event('reports', 'POST', {
    'reason': 'valid_test_reason'
  }, None, '127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None
