from api.dbinstance import DbInstance

def select_boards():
  result = {
    'status': 404,
    'data': None
  }

  with DbInstance().instance.cursor() as cursor:
    query = """
      SELECT
        b.id AS id,
        b.path AS path,
        b.name AS name,
        b.description AS description,
        b.flag_hidden AS flag_hidden,
        b.flag_nsfw AS flag_nsfw
      FROM boards AS b
      ORDER BY b.id ASC
    """
    cursor.execute(query)
    result['data'] = cursor.fetchall()
  
  if result['data']:
    result['status'] = 200
  
  return result
