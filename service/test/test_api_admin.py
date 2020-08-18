import json
import time
import pytest

import common.setenv
from api import app
from test.utils import (
  gen_apigw_event
)

def test_api_get_posts_notadmin():
  evt = gen_apigw_event('admin/posts', 'GET', query={'deleted': '0'}, ipv4_addr='127.0.1.1')
  res = app.lambda_handler(evt, '')

  assert res['statusCode'] == '403'

def test_api_get_posts():
  evt = gen_apigw_event('admin/posts', 'GET', query={'deleted': '0'}, ipv4_addr='127.0.0.1')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data'][0] is not None

def test_api_get_reports_notadmin():
  evt = gen_apigw_event('admin/reports', 'GET', ipv4_addr='127.0.1.1')
  res = app.lambda_handler(evt, '')

  assert res['statusCode'] == '403'

def test_api_get_reports():
  evt = gen_apigw_event('admin/reports', 'GET', ipv4_addr='127.0.0.1')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data'][0] is not None

def test_api_get_bans_notadmin():
  evt = gen_apigw_event('admin/bans', 'GET', ipv4_addr='127.0.1.1')
  res = app.lambda_handler(evt, '')

  assert res['statusCode'] == '403'

def test_api_get_bans():
  evt = gen_apigw_event('admin/bans', 'GET', ipv4_addr='127.0.0.1')
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'data' in res['body']
  assert bdy['data'] is not None
  assert bdy['data'][0] is not None
