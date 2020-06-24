import json
import pytest

import tests.set_env
from api import app

def gen_apigw_event(resource, method, body, query):
  """Generates an API Gateway event"""

  return {
    "body": json.dumps(body),
    "resource": resource,
    "requestContext": {
      "resourceId": "123456",
      "apiId": "1234567890",
      "resourcePath": resource,
      "httpMethod": method,
      "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
      "accountId": "123456789012",
      "identity": {
        "apiKey": "",
        "userArn": "",
        "cognitoAuthenticationType": "",
        "caller": "",
        "userAgent": "Custom User Agent String",
        "user": "",
        "cognitoIdentityPoolId": "",
        "cognitoIdentityId": "",
        "cognitoAuthenticationProvider": "",
        "sourceIp": "127.0.0.1",
        "accountId": "",
      },
      "stage": "prod",
    },
    "queryStringParameters": query,
    "headers": {
      "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
      "Accept-Language": "en-US,en;q=0.8",
      "CloudFront-Is-Desktop-Viewer": "true",
      "CloudFront-Is-SmartTV-Viewer": "false",
      "CloudFront-Is-Mobile-Viewer": "false",
      "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
      "CloudFront-Viewer-Country": "US",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Upgrade-Insecure-Requests": "1",
      "X-Forwarded-Port": "443",
      "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
      "X-Forwarded-Proto": "https",
      "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
      "CloudFront-Is-Tablet-Viewer": "false",
      "Cache-Control": "max-age=0",
      "User-Agent": "Custom User Agent String",
      "CloudFront-Forwarded-Proto": "https",
      "Accept-Encoding": "gzip, deflate, sdch",
    },
    "pathParameters": {"proxy": resource},
    "httpMethod": method,
    "stageVariables": {"baz": "qux"},
    "path": resource,
  }

def test_api_get_boards():
  evt = gen_apigw_event('/boards', 'GET', None, None)
  res = app.lambda_handler(evt, '')
  bdy = json.loads(res['body'])

  assert res['statusCode'] == '200'
  assert 'message' in res['body']
  assert bdy['message'] is not None
  assert bdy['message'][0]['path'] == 'b'
  assert bdy['message'][1]['path'] == 'a'
