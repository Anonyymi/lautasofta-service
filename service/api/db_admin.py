import os
import uuid
from common.dbinstance import DbInstance
from common.s3client import S3Client

def select_admin_posts(deleted, limit, offset):
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
        DATE_FORMAT(p.timestamp_bumped, '%%m/%%d/%%y(%%a)%%T') AS timestamp_bumped,
        CONCAT(SUBSTRING_INDEX(INET_NTOA(p.ipv4_addr), '.', 2), '.x.x') AS ipv4_addr,
        p.deleted AS deleted
      FROM posts AS p
      WHERE p.deleted = %s
      ORDER BY p.datetime_created DESC
      LIMIT %s OFFSET %s
    """, (deleted, limit, offset,))
    result['data'] = cursor.fetchall()
  
  # update result
  if result['data']:
    result['status'] = 200
  
  return result
