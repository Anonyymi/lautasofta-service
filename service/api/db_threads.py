import os
import uuid
from common.dbinstance import DbInstance
from common.s3client import S3Client

def select_threads(board_id, limit, offset):
  # prepare result
  result = {
    'status': 404,
    'data': []
  }
  # fetch rows from db
  with DbInstance().get_instance().cursor() as cursor:
    cursor.execute("""
      SELECT
        t.id AS id,
        t.board_id AS board_id,
        t.thread_id AS thread_id,
        t.data_message AS data_message,
        t.data_filepath AS data_filepath,
        DATE_FORMAT(t.datetime_created, '%%m/%%d/%%y(%%a)%%T') AS datetime_created,
        DATE_FORMAT(t.timestamp_edited, '%%m/%%d/%%y(%%a)%%T') AS timestamp_edited
      FROM posts AS t
      WHERE (t.board_id = %s AND t.thread_id IS NULL) AND t.deleted = false
      ORDER BY t.timestamp_bumped DESC
      LIMIT %s OFFSET %s
    """, (board_id, limit, offset,))
    result['data'] = cursor.fetchall()
    if result['data']:
      for item in result['data']:
        cursor.execute("""
          SELECT
            p.id AS id,
            p.board_id AS board_id,
            p.thread_id AS thread_id,
            p.data_message AS data_message,
            p.data_filepath AS data_filepath,
            DATE_FORMAT(p.datetime_created, '%%m/%%d/%%y(%%a)%%T')  AS datetime_created,
            DATE_FORMAT(p.timestamp_edited, '%%m/%%d/%%y(%%a)%%T') AS timestamp_edited
          FROM posts AS p
          WHERE (p.board_id = %s AND p.thread_id = %s) AND p.deleted = false
          ORDER BY p.datetime_created DESC
          LIMIT 3 OFFSET 0
        """, (board_id, item['id']))
        item['posts'] = sorted(cursor.fetchall(), key=lambda p: p['id'])
  # update result
  if result['data']:
    result['status'] = 200
  return result

def insert_thread(board_id, thread, ipv4_addr):
  # prepare result
  result = {
    'status': 400,
    'data': None
  }
  # if requested, generate presigned s3 POST url for the file
  file_upload_info = {
    'url': None,
    'fields': {
      'key': None
    },
  }
  if thread['extension'] is not None:
    file_upload_info = S3Client().instance.generate_presigned_post(
      os.getenv('MEDIA_BUCKET'),
      str(uuid.uuid4()) + '.' + thread['extension'],
      Fields={
        'acl': 'public-read'
      },
      Conditions=[
        ['acl', 'public-read'],
        ['content-type', thread['extension']],
        ['content-length-range', 128, 4096000]
      ],
      ExpiresIn=60
    )
  # insert row to db
  with DbInstance().get_instance().cursor() as cursor:
    # insert/update ipv4_addr row
    rows_anon = cursor.execute("""
      INSERT INTO anons (ipv4_addr) VALUES (INET_ATON(%s))
      ON DUPLICATE KEY UPDATE timestamp_posted=CURRENT_TIMESTAMP
    """, (ipv4_addr,))
    # insert thread
    rows_thread = cursor.execute("""
      INSERT INTO posts (board_id, data_message, data_filepath, ipv4_addr)
      VALUES (%s, %s, %s, INET_ATON(%s))
    """, (board_id, thread['message'], file_upload_info['fields']['key'], ipv4_addr,))
    id_inserted = cursor.lastrowid
    # commit if ok
    if rows_anon >= 1 and rows_thread == 1:
      cursor.connection.commit()
      result['data'] = {
        'id': id_inserted,
        'url': file_upload_info['url'],
        'fields': file_upload_info['fields']
      }
  # update result
  if result['data']:
    result['status'] = 201
  return result
