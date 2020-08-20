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
  api_schema_admin_report,
  api_schema_admin_ban
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
    return jsonify({'status': 403, 'data': None}), 403

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
    return jsonify({'status': 403, 'data': None}), 403

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
@validate_request_body(schema=api_schema_admin_report)
def api_put_report(report_id):
  """Updates a report"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # return 403 forbidden if requester is not an admin
  if ipv4_addr not in os.getenv('ADMIN_IPS'):
    return jsonify({'status': 403, 'data': None}), 403
  
  # insert content to db
  result = update_admin_report(report_id, request.json, ipv4_addr)

  return jsonify(result), result['status']

@api_admin.route('/bans', methods=['GET'])
def api_admin_get_bans():
  """Returns a list of bans filtered by various parameters"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # return 403 forbidden if requester is not an admin
  if ipv4_addr not in os.getenv('ADMIN_IPS'):
    return jsonify({'status': 403, 'data': None}), 403

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
@validate_request_body(schema=api_schema_admin_ban)
def api_post_ban():
  """Creates a new ban"""

  # parse request env
  ipv4_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)

  # return 403 forbidden if requester is not an admin
  if ipv4_addr not in os.getenv('ADMIN_IPS'):
    return jsonify({'status': 403, 'data': None}), 403
  
  # insert content to db
  result = insert_admin_ban(request.json, ipv4_addr)

  return jsonify(result), result['status']
