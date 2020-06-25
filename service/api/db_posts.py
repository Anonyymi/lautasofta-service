from api.dbinstance import DbInstance

def select_posts(board_id, thread_id, limit, offset):
  # prepare result
  result = {
    'status': 404,
    'data': None
  }
  # fetch rows from db
  with DbInstance().instance.cursor() as cursor:
    cursor.execute("""
      SELECT
        p.id AS id,
        p.board_id AS board_id,
        p.thread_id AS thread_id,
        p.data_message AS data_message,
        p.data_filepath AS data_filepath,
        p.datetime_created AS datetime_created,
        p.timestamp_edited AS timestamp_edited
      FROM posts AS p
      WHERE p.board_id = %s AND p.thread_id = %s OR p.id = %s
      ORDER BY p.datetime_created ASC
      LIMIT %s OFFSET %s
    """, (board_id, thread_id, thread_id, limit, offset,))
    result['data'] = cursor.fetchall()
  # update result
  if result['data']:
    result['status'] = 200
  return result

def insert_post(board_id, thread_id, post):
  # prepare result
  result = {
    'status': 400,
    'data': None
  }
  # insert row to db
  with DbInstance().instance.cursor() as cursor:
    rows = cursor.execute("""
      INSERT INTO posts (board_id, thread_id, data_message, data_filepath)
      VALUES (%s, %s, %s, %s)
    """, (board_id, thread_id, post['data_message'], None,))
    if rows == 1:
      cursor.connection.commit()
      result['data'] = cursor.lastrowid
  # update result
  if result['data']:
    result['status'] = 200
  return result
