import os

# init os.environ from file if not initialized
if os.getenv('DB_HOST') is None:
  import common.setenv

import json
import awsgi
from flask import Flask
from flask_cors import (
  CORS
)
from werkzeug.middleware.proxy_fix import (
  ProxyFix
)
from api.api_main import api_main
from api.api_admin import api_admin

# init flask app
app = Flask(__name__)
CORS(app, resources={
  r'/*': {
    'origins': '*'
  }
})
ProxyFix(app.wsgi_app, 1)
app.register_blueprint(api_main)
app.register_blueprint(api_admin)

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
