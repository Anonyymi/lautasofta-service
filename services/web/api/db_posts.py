import os
import uuid
from common.dbinstance import DbInstance
from common.s3client import S3Client

def select_post(post_id):
  # prepare result
  result = {
    'status': 404,
    'data': None
  }

  # fetch rows from db
  with DbInstance().get_instance().cursor() as cursor:
    cursor.execute("""
      SELECT
        p.id AS id,
        p.board_id AS board_id,
        p.thread_id AS thread_id,
        p.data_message AS data_message,
        p.data_filepath AS data_filepath,
        p.data_thumbpath AS data_thumbpath,
        DATE_FORMAT(p.datetime_created, '%%m/%%d/%%y(%%a)%%T') AS datetime_created,
        DATE_FORMAT(p.timestamp_edited, '%%m/%%d/%%y(%%a)%%T') AS timestamp_edited,
        (
          SELECT
            b.data_reason
          FROM bans AS b
          WHERE
            b.post_id = p.id
          ORDER BY b.datetime_ends IS NULL DESC, b.datetime_ends DESC
          LIMIT 1
        ) AS ban_reason
      FROM posts AS p
      WHERE p.id = %s AND p.deleted = false
    """, (post_id,))
    result['data'] = cursor.fetchone()
  
  # update result
  if result['data']:
    result['status'] = 200
  
  return result

def select_posts(board_id, thread_id, limit, offset):
  # prepare result
  result = {
    'status': 404,
    'data': None
  }

  # fetch rows from db
  with DbInstance().get_instance().cursor() as cursor:
    cursor.execute("""
      SELECT
        p.id AS id,
        p.board_id AS board_id,
        p.thread_id AS thread_id,
        p.data_message AS data_message,
        p.data_filepath AS data_filepath,
        p.data_thumbpath AS data_thumbpath,
        DATE_FORMAT(p.datetime_created, '%%m/%%d/%%y(%%a)%%T') AS datetime_created,
        DATE_FORMAT(p.timestamp_edited, '%%m/%%d/%%y(%%a)%%T') AS timestamp_edited,
        (
          SELECT
            b.data_reason
          FROM bans AS b
          WHERE
            b.post_id = p.id
          ORDER BY b.datetime_ends IS NULL DESC, b.datetime_ends DESC
          LIMIT 1
        ) AS ban_reason
      FROM posts AS p
      WHERE (p.board_id = %s AND p.thread_id = %s OR p.id = %s) AND p.deleted = false
      ORDER BY p.datetime_created ASC
      LIMIT %s OFFSET %s
    """, (board_id, thread_id, thread_id, limit, offset,))
    result['data'] = cursor.fetchall()
  
  # update result
  if result['data']:
    result['status'] = 200
  
  return result

def insert_post(board_id, thread_id, post, ipv4_addr):
  # prepare result
  result = {
    'status': 400,
    'data': None
  }

  # check if user has permission to create post
  with DbInstance().get_instance().cursor() as cursor:
    # check 403 (banned)
    cursor.execute("""
      SELECT
        CASE
          WHEN b.datetime_ends IS NOT NULL THEN (
            b.datetime_ends < CURRENT_TIMESTAMP
          )
          ELSE (
            false
          )
        END AS permission
      FROM bans AS b
      WHERE b.banned_ipv4_addr = INET_ATON(%s)
      ORDER BY b.datetime_ends IS NULL DESC, b.datetime_ends DESC
      LIMIT 1
    """, (ipv4_addr,))
    permitted_403 = cursor.fetchone()
    permitted_403 = True if permitted_403 is None else permitted_403['permission'] == 1

    # check 429 (too many requests)
    cursor.execute("""
      SELECT
        a.timestamp_created_post < DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 5 SECOND) AS permission
      FROM anons AS a
      WHERE a.ipv4_addr = INET_ATON(%s)
    """, (ipv4_addr,))
    permitted_429 = cursor.fetchone()
    permitted_429 = True if permitted_429 is None else permitted_429['permission'] == 1

    # create post if permitted
    if permitted_403 and permitted_429:
      # if requested, generate presigned s3 POST url for the file
      file_upload_info = {
        'url': None,
        'fields': {
          'key': None
        },
      }

      if 'extension' in post and post['extension'] is not None:
        file_upload_info = S3Client().instance.generate_presigned_post(
          os.getenv('MEDIA_BUCKET'),
          str(uuid.uuid4()) + '.' + post['extension'],
          Fields={
            'acl': 'public-read',
            'Content-Type': 'image/' + post['extension']
          },
          Conditions=[
            {'acl': 'public-read'},
            {'Content-Type': 'image/' + post['extension']},
            ['content-length-range', 128, 4096000]
          ],
          ExpiresIn=60
        )
      
      # insert/update ipv4_addr row
      rows_anon = cursor.execute("""
        INSERT INTO anons (ipv4_addr, timestamp_created_post) VALUES (INET_ATON(%s), CURRENT_TIMESTAMP)
        ON DUPLICATE KEY UPDATE timestamp_created_post=CURRENT_TIMESTAMP
      """, (ipv4_addr,))

      # insert post
      rows_post = cursor.execute("""
        INSERT INTO posts (board_id, thread_id, data_message, data_filepath, ipv4_addr)
        VALUES (%s, %s, %s, %s, INET_ATON(%s))
      """, (board_id, thread_id, post['message'], file_upload_info['fields']['key'], ipv4_addr,))
      id_inserted = cursor.lastrowid

      # update thread
      rows_thread = cursor.execute("""
        UPDATE posts
        SET timestamp_bumped = CURRENT_TIMESTAMP
        WHERE board_id = %s AND id = %s;
      """, (board_id, thread_id,))
      
      # commit if ok
      if rows_anon >= 1 and rows_post == 1 and rows_thread == 1:
        cursor.connection.commit()
        result['status'] = 201
        result['data'] = {
          'id': id_inserted,
          'url': file_upload_info['url'],
          'fields': file_upload_info['fields']
        }
    else:
      if not permitted_403:
        result['status'] = 403
        result['data'] = {
          'message': 'you are banned'
        }
      else:
        result['status'] = 429
        result['data'] = {
          'message': 'too many requests'
        }
  
  return result

def delete_post(post_id, ipv4_addr):
  # prepare result
  result = {
    'status': 403,
    'data': None
  }

  # delete row from db
  with DbInstance().get_instance().cursor() as cursor:
    # delete post (admin)
    if ipv4_addr in os.getenv('ADMIN_IPS'):
      rows_deleted = cursor.execute("""
        UPDATE posts SET
          deleted = true,
          delete_reason = 'DELETED_BY_ADMIN'
        WHERE
          id = %s
      """, (post_id,))
      
      # commit if ok
      if rows_deleted >= 1:
        cursor.connection.commit()
        result['data'] = {
          'affected': rows_deleted
        }
    # delete post (normal)
    else:
      rows_deleted = cursor.execute("""
        UPDATE posts SET
          deleted = true,
          delete_reason = 'DELETED_BY_USER'
        WHERE
          id = %s
        AND
          ipv4_addr = INET_ATON(%s)
        AND
          datetime_created > DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 HOUR)
      """, (post_id, ipv4_addr,))
      
      # commit if ok
      if rows_deleted >= 1:
        cursor.connection.commit()
        result['data'] = {
          'affected': rows_deleted
        }

  # update result
  if result['data']:
    result['status'] = 200
  
  return result
