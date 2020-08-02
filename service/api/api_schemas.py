from common.config import (
  config
)

api_schema_thread = {
  'message': {
    'type': 'string',
    'minlen': 1,
    'maxlen': 4096
  },
  'extension': {
    'type': 'string',
    'values': config['MEDIA_CONTENT_TYPES']
  }
}

api_schema_post = {
  'message': {
    'type': 'string',
    'minlen': 1,
    'maxlen': 4096
  },
  'extension': {
    'type': 'string',
    'values': config['MEDIA_CONTENT_TYPES'],
    'nullable': True
  }
}

api_schema_report = {
  'post_id': {
    'type': 'number',
    'min': 1,
    'nullable': False
  },
  'reason': {
    'type': 'string',
    'minlen': 1,
    'maxlen': 1024
  }
}
