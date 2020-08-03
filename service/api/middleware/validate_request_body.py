from functools import wraps
from flask import (
  request,
  jsonify
)

def validate_request_body(schema=None):
  """Validates request body against input schema"""
  def decorator(f):
    @wraps(f)
    def middleware(*args, **kwargs):
      # get api schema and request body
      api_schema = schema
      body_req = request.json

      # nothing to validate: pass
      if api_schema is None:
        return f(*args, **kwargs)
      
      if body_req is None:
        return validate_request_body_response(400, 'invalid body: None')
      elif len(body_req) == 0:
        return validate_request_body_response(400, 'invalid body: len(keys) == 0')
      elif len(body_req) > 128:
        return validate_request_body_response(400, 'invalid body: len(keys) > 128')
      
      # validate request body against api schema
      result = do_request_body_validation(api_schema, body_req, 0)

      # schema is invalid: fail
      if result is not None:
        return validate_request_body_response(400, f'invalid body: {result}')
      
      # schema is valid: pass
      return f(*args, **kwargs)
    return middleware
  return decorator

def do_request_body_validation(schema: dict, body: dict, n=0):
  if n > 8:
    return f'body nested object depth limit of \'8\' reached'
  
  for key, sch in schema.items():
    # get schema object props
    sch_type = sch['type']
    sch_nullable = sch['nullable']

    if body.get(key) is not None:
      # get body object props
      obj = body[key]
      obj_type = type(obj).__name__

      # execute validation rules
      if sch_type == 'string':
        if obj_type != 'str':
          return f'key \'{key}\' value type is not \'{sch_type}\''
        elif 'values' in sch and obj not in sch['values']:
          return f'key \'{key}\' value is not allowed'
        elif 'minlen' in sch and len(obj) < sch['minlen']:
          return f'key \'{key}\' value is shorter than allowed \'{sch["minlen"]}\''
        elif 'maxlen' in sch and len(obj) > sch['maxlen']:
          return f'key \'{key}\' value is longer than allowed \'{sch["maxlen"]}\''
      elif sch_type == 'number':
        if obj_type not in ['int', 'float']:
          return f'key \'{key}\' value type is not \'{sch_type}\''
        elif 'min' in sch and obj < sch['min']:
          return f'key \'{key}\' value is smaller than allowed \'{sch["min"]}\''
        elif 'max' in sch and obj > sch['max']:
          return f'key \'{key}\' value is larger than allowed \'{sch["max"]}\''
      elif sch_type == 'object':
        if obj_type != 'dict':
          return f'key \'{key}\' value type is not \'{sch_type}\''
        return do_request_body_validation(sch, obj, n+1)
    elif not sch_nullable:
      return f'key \'{key}\' is missing from body and is not nullable'

def validate_request_body_response(status=400, message='invalid body: ??'):
  return jsonify({
    'status': status,
    'data': {
      'message': message
    }
  }), status
