import json

def gen_apigw_event(resource, method, body=None, query={}, ipv4_addr='127.0.0.1'):
  """Generates an API Gateway event"""

  return {
    "httpMethod": method,
    "body": json.dumps(body),
    "resource": "/{proxy+}",
    "requestContext": {
      "resourceId": "123456",
      "apiId": "1234567890",
      "resourcePath": "/{proxy+}",
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
        "sourceIp": ipv4_addr,
        "accountId": "",
      },
      "stage": "prod",
      "path": "/{proxy+}"
    },
    "queryStringParameters": query,
    "multiValueQueryStringParameters": {x: [x] for x in query},
    "headers": {
      "Content-Type": "application/json",
      "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
      "Accept-Language": "en-US,en;q=0.8",
      "CloudFront-Is-Desktop-Viewer": "true",
      "CloudFront-Is-SmartTV-Viewer": "false",
      "CloudFront-Is-Mobile-Viewer": "false",
      "X-Forwarded-For": ipv4_addr,
      "CloudFront-Viewer-Country": "US",
      "Accept": "*/*",
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
    "stageVariables": None,
    "path": '/' + resource,
  }
