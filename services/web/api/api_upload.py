import os
from flask import (
  Flask,
  Blueprint,
  request,
  jsonify
)
from werkzeug import (
  secure_filename
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
api_upload = Blueprint('upload_api', __name__)

@api_upload.route('/upload', methods=['POST'])
def api_post_upload():
  