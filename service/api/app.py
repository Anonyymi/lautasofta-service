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
from api.db_boards import (
  select_boards
)
from api.db_threads import (
  select_threads,
  insert_thread
)
from api.db_posts import (
  select_posts,
  insert_post
)

# init flask app
app = Flask(__name__)
CORS(app, resources={
  r'/*': {
    'origins': '*'
  }
})

@app.route('/config', methods=['GET'])
def api_get_config():
  """Returns a configuration object for the requesting client"""
  result = {
    'S3_MEDIA_BUCKET_URL': os.getenv('S3_ENDPOINT_URL') + '/' + os.getenv('MEDIA_BUCKET')
  }
  return jsonify(status=200, data=result)

@app.route('/boards', methods=['GET'])
def api_get_boards():
  """Returns a list of accessible boards"""
  # get results from db
  result = select_boards()
  return jsonify(result)

@app.route('/boards/<int:board_id>/threads', methods=['GET'])
def api_get_threads(board_id):
  """Returns a list of threads"""
  # parse args
  arg_limit = request.args.get('limit', default=128, type=int)
  arg_offset = request.args.get('offset', default=0, type=int)
  # validate args
  if arg_limit <= 0 or arg_limit > 128:
    arg_limit = 128
  if arg_offset < 0:
    arg_offset = 0
  # get results from db
  result = select_threads(board_id, arg_limit, arg_offset)
  return jsonify(result)

@app.route('/boards/<int:board_id>/threads', methods=['POST'])
def api_post_thread(board_id):
  """Creates a new thread"""
  # insert content to db
  result = insert_thread(board_id, request.json)
  return jsonify(result)

@app.route('/boards/<int:board_id>/threads/<int:thread_id>/posts', methods=['GET'])
def api_get_posts(board_id, thread_id):
  """Returns a list of posts"""
  # parse args
  arg_limit = request.args.get('limit', default=128, type=int)
  arg_offset = request.args.get('offset', default=0, type=int)
  # validate args
  if arg_limit <= 0 or arg_limit > 128:
    arg_limit = 128
  if arg_offset < 0:
    arg_offset = 0
  # get results from db
  result = select_posts(board_id, thread_id, arg_limit, arg_offset)
  return jsonify(result)

@app.route('/boards/<int:board_id>/threads/<int:thread_id>/posts', methods=['POST'])
def api_post_post(board_id, thread_id):
  """Creates a new post"""
  # insert content to db
  result = insert_post(board_id, thread_id, request.json)
  return jsonify(result)

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
