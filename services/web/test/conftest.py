import pytest

import common.setenv
from api import app
from api import (
  db_threads,
  db_posts,
  db_reports,
  db_admin
)

def pytest_sessionstart(session):
  print('pytest::start')
  # threads
  threads = []
  threads.append(db_threads.insert_thread(1, {
    'message': 'test thread 1',
    'extension': 'png'
  }, '127.0.0.1')['data'])
  threads.append(db_threads.insert_thread(1, {
    'message': 'test thread 2',
    'extension': 'png'
  }, '127.0.1.1')['data'])
  threads.append(db_threads.insert_thread(1, {
    'message': 'test thread 3',
    'extension': 'png'
  }, '127.0.1.2')['data'])
  threads.append(db_threads.insert_thread(2, {
    'message': 'test thread 4',
    'extension': 'png'
  }, '127.0.1.3')['data'])
  threads.append(db_threads.insert_thread(2, {
    'message': 'test thread 5',
    'extension': 'png'
  }, '127.0.1.4')['data'])
  # reports
  reports = []
  reports.append(db_reports.insert_report({
    'post_id': threads[0]['id'],
    'reason': 'test report 1'
  }, '127.0.1.4')['data'])
  reports.append(db_reports.insert_report({
    'post_id': threads[1]['id'],
    'reason': 'test report 2'
  }, '127.0.1.3')['data'])
  # bans
  db_admin.insert_admin_ban({
    'post_id': threads[1]['id'],
    'reason': 'test ban 1',
    'datetime_ends': None
  }, '127.0.0.1')

def pytest_sessionfinish(session, exitstatus):
  print('pytest::finish')
