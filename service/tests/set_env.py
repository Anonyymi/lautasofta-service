import os
import json

env = json.load(open('local_env.json'))

for key,val in env['Parameters'].items():
  os.environ[key] = val
