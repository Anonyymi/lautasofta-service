import os
import json

print(f'WARNING: loading environment variables from local_env.json...')

env = json.load(open('deployment/local/local_env.json'))

for key,val in env['Parameters'].items():
  os.environ[key] = val
