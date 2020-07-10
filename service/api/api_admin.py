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
from api.db_admin import (
  select_admin_posts,
  select_admin_reports,
  select_admin_bans,
  update_admin_report,
  insert_admin_ban
)

# init flask blueprint
api_admin = Blueprint('admin_api', __name__, url_prefix='/admin')

@api_admin.route('/posts', methods=['GET'])
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

@api_admin.route('/reports', methods=['GET'])
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

@api_admin.route('/reports/<int:report_id>', methods=['PUT'])
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

@api_admin.route('/bans', methods=['GET'])
def api_admin_get_bans():
  """Returns a list of bans filtered by various parameters"""

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
  result = select_admin_bans(arg_limit, arg_offset)

  return jsonify(result), result['status']

@api_admin.route('/bans', methods=['POST'])
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
