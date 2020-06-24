import json
import awsgi
from flask import (
  Flask,
  jsonify
)
from api.dbmodels import DbModels

# init flask app
app = Flask(__name__)

# init db schema
db_models = DbModels()

@app.route('/boards')
def api_get_boards():
  """Returns a list of accessible boards"""

  return jsonify({
    'status': 200,
    'message': [
      'board1',
      'board2'
    ]
  })

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
