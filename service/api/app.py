import os

# init os.environ from file if not initialized
if os.getenv('DB_HOST') is None:
  import common.set_env

import json
import awsgi
from flask import (
  Flask,
  request,
  jsonify
)
from flask_cors import (
  CORS
)
from werkzeug.middleware.proxy_fix import (
  ProxyFix
)
from common.config import (
  config,
  get_client_config
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
from api.db_admin import (
  select_admin_posts,
  select_admin_reports,
  select_admin_bans,
  update_admin_report,
  insert_admin_ban
)

# init flask app
app = Flask(__name__)
CORS(app, resources={
  r'/*': {
    'origins': '*'
  }
})
ProxyFix(app.wsgi_app, 1)

#######################
# NORMAL ROUTES BELOW #
#######################

@app.route('/config', methods=['GET'])
def api_get_config():
  """Returns a configuration object for the requesting client"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  return jsonify(status=200, data=get_client_config(ipv4_addr))

@app.route('/boards', methods=['GET'])
def api_get_boards():
  """Returns a list of accessible boards"""

  # get results from db
  result = select_boards()

  return jsonify(result), result['status']

@app.route('/boards/<int:board_id>/threads', methods=['GET'])
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

@app.route('/boards/<int:board_id>/threads', methods=['POST'])
def api_post_thread(board_id):
  """Creates a new thread"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # validate body
  body = request.json
  if not body['message'] or len(body['message'].strip(' \t\n\r')) == 0:
    return jsonify({'statusCode': 400, 'body': None}), 400
  
  if not body['extension'] or body['extension'] not in config['MEDIA_CONTENT_TYPES']:
    return jsonify({'statusCode': 400, 'body': None}), 400
  
  # insert content to db
  result = insert_thread(board_id, body, ipv4_addr)

  return jsonify(result), result['status']

@app.route('/posts/<int:post_id>', methods=['GET'])
def api_get_post(post_id):
  """Returns a single post"""
  
  # get result from db
  result = select_post(post_id)

  return jsonify(result), result['status']

@app.route('/boards/<int:board_id>/threads/<int:thread_id>/posts', methods=['GET'])
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

@app.route('/boards/<int:board_id>/threads/<int:thread_id>/posts', methods=['POST'])
def api_post_post(board_id, thread_id):
  """Creates a new post"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # validate body
  body = request.json
  if not body['message'] or len(body['message'].strip(' \t\n\r')) == 0:
    return jsonify({'statusCode': 400, 'body': None}), 400
  
  if body['extension'] and body['extension'] not in config['MEDIA_CONTENT_TYPES']:
    body['extension'] = None
  
  # insert content to db
  result = insert_post(board_id, thread_id, body, ipv4_addr)

  return jsonify(result), result['status']

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def api_delete_post(post_id):
  """Deletes a post (thread or post)"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # delete content from db
  result = delete_post(post_id, ipv4_addr)

  return jsonify(result), result['status']

@app.route('/reports', methods=['POST'])
def api_post_report():
  """Creates a new report"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # validate body
  body = request.json
  if not body['reason'] or len(body['reason'].strip(' \t\n\r')) == 0:
    return jsonify({'statusCode': 400, 'body': None}), 400
  
  # insert content to db
  result = insert_report(body, ipv4_addr)

  return jsonify(result), result['status']

#######################
# ADMIN ROUTES BELOW  #
#######################

@app.route('/admin/posts', methods=['GET'])
def api_admin_get_posts():
  """Returns a list of posts (threads & posts) filtered by various parameters"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # return 403 forbidden if requester is not an admin
  if ipv4_addr not in os.getenv('ADMIN_IPS'):
    return jsonify(status=403, data={'statusCode': 403, 'body': None})

  # parse args
  arg_limit = request.args.get('limit', default=100, type=int)
  arg_offset = request.args.get('offset', default=0, type=int)
  arg_deleted = request.args.get('deleted', default=1, type=int)

  # validate args
  if arg_limit <= 0 or arg_limit > config['MAX_POSTS_PER_PAGE']:
    arg_limit = config['MAX_POSTS_PER_PAGE']
  
  if arg_offset < 0:
    arg_offset = 0

  # get results from db
  result = select_admin_posts(arg_deleted, arg_limit, arg_offset)

  return jsonify(result), result['status']

@app.route('/admin/reports', methods=['GET'])
def api_admin_get_reports():
  """Returns a list of reports filtered by various parameters"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # return 403 forbidden if requester is not an admin
  if ipv4_addr not in os.getenv('ADMIN_IPS'):
    return jsonify(status=403, data={'statusCode': 403, 'body': None})

  # parse args
  arg_limit = request.args.get('limit', default=100, type=int)
  arg_offset = request.args.get('offset', default=0, type=int)

  # validate args
  if arg_limit <= 0 or arg_limit > config['MAX_POSTS_PER_PAGE']:
    arg_limit = config['MAX_POSTS_PER_PAGE']
  
  if arg_offset < 0:
    arg_offset = 0

  # get results from db
  result = select_admin_reports(arg_limit, arg_offset)

  return jsonify(result), result['status']

@app.route('/admin/reports/<int:report_id>', methods=['PUT'])
def api_put_report(report_id):
  """Updates a report"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # return 403 forbidden if requester is not an admin
  if ipv4_addr not in os.getenv('ADMIN_IPS'):
    return jsonify(status=403, data={'statusCode': 403, 'body': None})

  # validate body
  body = request.json
  if body['processed'] is None:
    return jsonify({'statusCode': 400, 'body': None}), 400
  
  if not body['admin_notes'] or len(body['admin_notes'].strip(' \t\n\r')) == 0:
    return jsonify({'statusCode': 400, 'body': None}), 400
  
  # insert content to db
  result = update_admin_report(report_id, body, ipv4_addr)

  return jsonify(result), result['status']

@app.route('/admin/bans', methods=['POST'])
def api_post_ban():
  """Creates a new ban"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # return 403 forbidden if requester is not an admin
  if ipv4_addr not in os.getenv('ADMIN_IPS'):
    return jsonify(status=403, data={'statusCode': 403, 'body': None})

  # validate body
  body = request.json
  if body['report_id'] is None and body['post_id'] is None:
    return jsonify({'statusCode': 400, 'body': None}), 400
  
  if not body['reason'] or len(body['reason'].strip(' \t\n\r')) == 0:
    return jsonify({'statusCode': 400, 'body': None}), 400
  
  # insert content to db
  result = insert_admin_ban(body, ipv4_addr)

  return jsonify(result), result['status']

def lambda_handler(evt, ctx):
  """AWS Lambda entrypoint"""

  try:
    return awsgi.response(app, evt, ctx)
  except Exception as err:
    print(f'{err}')

    return {
      'statusCode': 500,
      'body': json.dumps({
        'message': 'internal server error',
      })
    }
