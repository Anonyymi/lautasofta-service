from api.dbinstance import DbInstance

def select_boards():
  # prepare result
  result = {
    'status': 404,
    'data': None
  }
  # fetch rows from db
  with DbInstance().instance.cursor() as cursor:
    cursor.execute("""
      SELECT
        b.id AS id,
        b.path AS path,
        b.name AS name,
        b.description AS description,
        b.flag_hidden AS flag_hidden,
        b.flag_nsfw AS flag_nsfw
      FROM boards AS b
      ORDER BY b.id ASC
    """)
    result['data'] = cursor.fetchall()
  # update result
  if result['data']:
    result['status'] = 200
  return result
