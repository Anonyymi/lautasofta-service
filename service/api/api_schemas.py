from common.config import (
  config
)

api_schema_thread = {
  'message': {
    'type': 'string',
    'nullable': False,
    'minlen': 1,
    'maxlen': 4096
  },
  'extension': {
    'type': 'string',
    'nullable': False,
    'values': config['MEDIA_CONTENT_TYPES']
  }
}

api_schema_post = {
  'message': {
    'type': 'string',
    'nullable': False,
    'minlen': 1,
    'maxlen': 4096
  },
  'extension': {
    'type': 'string',
    'nullable': True,
    'values': config['MEDIA_CONTENT_TYPES']
  }
}

api_schema_report = {
  'post_id': {
    'type': 'number',
    'nullable': False,
    'min': 1
  },
  'reason': {
    'type': 'string',
    'nullable': False,
    'minlen': 1,
    'maxlen': 1024
  }
}
