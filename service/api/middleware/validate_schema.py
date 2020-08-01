from functools import wraps
from flask import (
  request,
  jsonify
)

def validate_schema(schema=None):
  """Validates request schema against input schema"""
  def decorator(f):
    @wraps(f)
    def middleware(*args, **kwargs):
      ctx = f(*args, **kwargs)

      # get api schema and request body
      api_schema = schema
      body_req = request.json
      
      print(f'api_schema: {api_schema}, body_req: {body_req}')

      # nothing to validate: pass
      if api_schema is None:
        return ctx
      
      if body_req is None:
        return validate_schema_response(400, 'invalid body: None')
      
      # validate request body against api schema
      for key, val in body_req.items():
        if key in api_schema:
          result = validate_schema_obj(key, val, api_schema)
          
          # schema is invalid: fail
          if result is not None:
            return validate_schema_response(400, f'invalid body: {result}')

      # schema is valid: pass
      return ctx
    return middleware
  return decorator

def validate_schema_obj(key, val, api_schema, n=0):
  if n > 8:
    return f'input object nested depth limit of \'8\' reached'
  
  schema = api_schema[key]
  print(f'key: {key}, val: {val}, schema: {schema}')

  val_type = type(val).__name__
  sch_type = schema['type']
  if sch_type == 'string':
    if val_type != 'str':
      return f'key \'{key}\' value type is not \'{sch_type}\''
    elif 'values' in schema and val not in schema['values']:
      return f'key \'{key}\' value is not allowed'
    elif 'minlen' in schema and len(val) < schema['minlen']:
      return f'key \'{key}\' value is shorter than allowed \'{schema["minlen"]}\''
    elif 'maxlen' in schema and len(val) > schema['maxlen']:
      return f'key \'{key}\' value is longer than allowed \'{schema["maxlen"]}\''
  elif sch_type == 'number':
    if val_type not in ['int', 'float']:
      return f'key \'{key}\' value type is not \'{sch_type}\''
    elif 'min' in schema and val < schema['min']:
      return f'key \'{key}\' value is smaller than allowed \'{schema["min"]}\''
    elif 'max' in schema and val > schema['max']:
      return f'key \'{key}\' value is larger than allowed \'{schema["max"]}\''
  elif sch_type == 'object':
    if val_type != 'dict':
      return f'key \'{key}\' value type is not \'{sch_type}\''
    elif not val:
      return f'key \'{key}\' value must not be empty'
    for key_n, val_n in val.items():
      return validate_schema_obj(key_n, val_n, schema[key_n], n+1)
  
  return None

def validate_schema_response(status=400, message='invalid body: ??'):
  return jsonify({
    'status': status,
    'data': {
      'message': message
    }
  }), status
