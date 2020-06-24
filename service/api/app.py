import json
import awsgi
from flask import (
  Flask,
  jsonify
)
from api.api_boards import (
  select_boards
)

# init flask app
app = Flask(__name__)

@app.route('/boards')
def api_get_boards():
  """Returns a list of accessible boards"""

  result = select_boards()

  return jsonify(status=result['status'], message=result['data'])

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
