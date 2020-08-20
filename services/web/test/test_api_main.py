import json
import time
import pytest

import common.setenv
from api import app
from test.utils import (
  gen_apigw_event
)

def test_api_get_config_user():
  evt = gen_apigw_event('config', 'GET', ipv4_addr='127.0.0.2')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['MEDIA_BUCKET_URL'] is not None
  assert bdy['data']['USER_ROLE'] == 'USER'

def test_api_get_config_administrator():
  evt = gen_apigw_event('config', 'GET', ipv4_addr='127.0.0.1')
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

def test_api_get_threads():
  evt = gen_apigw_event('boards/1/threads', 'GET', ipv4_addr='127.0.0.1')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data'][0] is not None

def test_api_post_thread_png():
  evt = gen_apigw_event('boards/1/threads', 'POST', body={
    'message': 'test msg',
    'extension': 'png'
  }, ipv4_addr='127.0.0.10')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '201'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['id'] is not None

  time.sleep(1.0)

def test_api_post_post_webp():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', body={
    'message': 'test msg',
    'extension': 'webp'
  }, ipv4_addr='127.0.0.11')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '201' 
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['id'] is not None

  time.sleep(1.0)

def test_api_post_post_noimg():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', body={
    'message': 'test msg'
  }, ipv4_addr='127.0.0.12')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '201'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['id'] is not None

  time.sleep(1.0)

def test_api_post_report():
  evt = gen_apigw_event('reports', 'POST', body={
    'post_id': 2,
    'reason': 'test report'
  }, ipv4_addr='127.0.0.13')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '201'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['id'] is not None

  time.sleep(1.0)

def test_api_delete_post():
  evt = gen_apigw_event('posts/2', 'DELETE', ipv4_addr='127.0.0.1')
  res = app.lambda_handler(evt, '')

  assert res['statusCode'] == '200'

def test_api_post_thread_err_empty_body():
  evt = gen_apigw_event('boards/1/threads', 'POST', ipv4_addr='127.0.0.14')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_thread_err_invalid_body_1():
  evt = gen_apigw_event('boards/1/threads', 'POST', body={
    'message': '',
  }, ipv4_addr='127.0.0.15')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_thread_err_invalid_body_2():
  evt = gen_apigw_event('boards/1/threads', 'POST', body={
    'extension': ''
  }, ipv4_addr='127.0.0.16')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_thread_err_invalid_body_3():
  evt = gen_apigw_event('boards/1/threads', 'POST', body={
    'extension': 'not_a_valid_extension'
  }, ipv4_addr='127.0.0.17')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_post_err_empty_body():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', ipv4_addr='127.0.0.18')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_post_err_invalid_body_1():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', body={
    'message': ''
  }, ipv4_addr='127.0.0.19')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_post_err_invalid_body_2():
  evt = gen_apigw_event('boards/1/threads/1/posts', 'POST', body={
    'extension': 'not_a_valid_extension'
  }, ipv4_addr='127.0.0.20')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_report_err_empty_body():
  evt = gen_apigw_event('reports', 'POST', ipv4_addr='127.0.0.21')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_report_err_invalid_body_1():
  evt = gen_apigw_event('reports', 'POST', body={
    'post_id': 0,
    'reason': 'valid test reason'
  }, ipv4_addr='127.0.0.22')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_report_err_invalid_body_2():
  evt = gen_apigw_event('reports', 'POST', body={
    'post_id': 12491258
  }, ipv4_addr='127.0.0.23')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None

def test_api_post_report_err_invalid_body_3():
  evt = gen_apigw_event('reports', 'POST', body={
    'reason': 'valid_test_reason'
  }, ipv4_addr='127.0.0.24')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '400'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data']['message'] is not None
