import os
from flask import (
  Flask,
  Blueprint,
  request,
  jsonify
)
from common.config import (
  config,
  get_client_config
)
from api.middleware.validate_request_body import (
  validate_request_body
)
from api.api_schemas import (
  api_schema_thread,
  api_schema_post,
  api_schema_report
)
from api.db_boards import (
  select_boards
)
from api.db_threads import (
  select_threads,
  insert_thread
)
from api.db_posts import (
  select_post,
  select_posts,
  insert_post,
  delete_post
)
from api.db_reports import (
  insert_report
)

# init flask blueprint
api_main = Blueprint('main_api', __name__)

@api_main.route('/config', methods=['GET'])
def api_get_config():
  """Returns a configuration object for the requesting client"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  return jsonify(status=200, data=get_client_config(ipv4_addr))

@api_main.route('/boards', methods=['GET'])
def api_get_boards():
  """Returns a list of accessible boards"""

  # get results from db
  result = select_boards()

  return jsonify(result), result['status']

@api_main.route('/boards/<int:board_id>/threads', methods=['GET'])
def api_get_threads(board_id):
  """Returns a list of threads"""

  # parse args
  arg_limit = request.args.get('limit', default=10, type=int)
  arg_offset = request.args.get('offset', default=0, type=int)

  # validate args
  if arg_limit <= 0 or arg_limit > config['MAX_THREADS_PER_PAGE']:
    arg_limit = config['MAX_THREADS_PER_PAGE']
  
  if arg_offset < 0:
    arg_offset = 0

  # get results from db
  result = select_threads(board_id, arg_limit, arg_offset)

  return jsonify(result), result['status']

@api_main.route('/boards/<int:board_id>/threads', methods=['POST'])
@validate_request_body(schema=api_schema_thread)
def api_post_thread(board_id):
  """Creates a new thread"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)
  
  # insert content to db
  result = insert_thread(board_id, request.json, ipv4_addr)

  return jsonify(result), result['status']

@api_main.route('/posts/<int:post_id>', methods=['GET'])
def api_get_post(post_id):
  """Returns a single post"""
  
  # get result from db
  result = select_post(post_id)

  return jsonify(result), result['status']

@api_main.route('/boards/<int:board_id>/threads/<int:thread_id>/posts', methods=['GET'])
def api_get_posts(board_id, thread_id):
  """Returns a list of posts"""

  # parse args
  arg_limit = request.args.get('limit', default=100, type=int)
  arg_offset = request.args.get('offset', default=0, type=int)

  # validate args
  if arg_limit <= 0 or arg_limit > config['MAX_POSTS_PER_PAGE']:
    arg_limit = config['MAX_POSTS_PER_PAGE']
  
  if arg_offset < 0:
    arg_offset = 0
  
  # get results from db
  result = select_posts(board_id, thread_id, arg_limit, arg_offset)

  return jsonify(result), result['status']

@api_main.route('/boards/<int:board_id>/threads/<int:thread_id>/posts', methods=['POST'])
@validate_request_body(schema=api_schema_post)
def api_post_post(board_id, thread_id):
  """Creates a new post"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)
  
  # insert content to db
  result = insert_post(board_id, thread_id, request.json, ipv4_addr)

  return jsonify(result), result['status']

@api_main.route('/posts/<int:post_id>', methods=['DELETE'])
def api_delete_post(post_id):
  """Deletes a post (thread or post)"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # delete content from db
  result = delete_post(post_id, ipv4_addr)

  return jsonify(result), result['status']

@api_main.route('/reports', methods=['POST'])
@validate_request_body(schema=api_schema_report)
def api_post_report():
  """Creates a new report"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)
  
  # insert content to db
  result = insert_report(request.json, ipv4_addr)

  return jsonify(result), result['status']
