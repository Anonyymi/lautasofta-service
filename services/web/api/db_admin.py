import os
import uuid
from common.dbinstance import DbInstance

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

def select_admin_reports(limit, offset):
  # prepare result
  result = {
    'status': 404,
    'data': None
  }

  # fetch rows from db
  with DbInstance().get_instance().cursor() as cursor:
    cursor.execute("""
      SELECT
        r.id AS id,
        r.post_id AS post_id,
        r.data_reason AS data_reason,
        DATE_FORMAT(r.datetime_created, '%%m/%%d/%%y(%%a)%%T') AS datetime_created,
        DATE_FORMAT(r.timestamp_processed, '%%m/%%d/%%y(%%a)%%T') AS timestamp_processed,
        CONCAT(SUBSTRING_INDEX(INET_NTOA(r.ipv4_addr), '.', 2), '.x.x') AS ipv4_addr,
        r.processed AS processed,
        r.admin_notes AS admin_notes
      FROM reports AS r
      ORDER BY r.datetime_created DESC
      LIMIT %s OFFSET %s
    """, (limit, offset,))
    result['data'] = cursor.fetchall()
  
  # update result
  if result['data']:
    result['status'] = 200
  
  return result

def update_admin_report(report_id, report, ipv4_addr):
  # prepare result
  result = {
    'status': 400,
    'data': None
  }

  # update row in db
  with DbInstance().get_instance().cursor() as cursor:
    rows_updated = cursor.execute("""
      UPDATE reports SET
        processed=%s,
        admin_notes=%s
      WHERE
        id = %s
    """, (report['processed'], report['admin_notes'], report_id,))

    if rows_updated == 1:
      cursor.connection.commit()
      result['status'] = 204
      result['data'] = {
        'affected': rows_updated
      }

  return result

def select_admin_bans(limit, offset):
  # prepare result
  result = {
    'status': 404,
    'data': None
  }

  # fetch rows from db
  with DbInstance().get_instance().cursor() as cursor:
    cursor.execute("""
      SELECT
        b.id AS id,
        b.report_id AS report_id,
        b.post_id AS post_id,
        b.data_reason AS data_reason,
        DATE_FORMAT(b.datetime_created, '%%m/%%d/%%y(%%a)%%T') AS datetime_created,
        DATE_FORMAT(b.datetime_starts, '%%m/%%d/%%y(%%a)%%T') AS datetime_starts,
        DATE_FORMAT(b.datetime_ends, '%%m/%%d/%%y(%%a)%%T') AS datetime_ends,
        CONCAT(SUBSTRING_INDEX(INET_NTOA(b.ipv4_addr), '.', 2), '.x.x') AS ipv4_addr,
        CONCAT(SUBSTRING_INDEX(INET_NTOA(b.banned_ipv4_addr), '.', 2), '.x.x') AS banned_ipv4_addr
      FROM bans AS b
      ORDER BY b.datetime_created DESC
      LIMIT %s OFFSET %s
    """, (limit, offset,))
    result['data'] = cursor.fetchall()
  
  # update result
  if result['data']:
    result['status'] = 200
  
  return result

def insert_admin_ban(ban, ipv4_addr):
  # prepare result
  result = {
    'status': 400,
    'data': None
  }

  # insert row to db
  with DbInstance().get_instance().cursor() as cursor:
    rows_inserted = 0
    if 'report_id' in ban and ban['report_id'] is not None:
      rows_inserted = cursor.execute("""
        INSERT INTO bans (report_id, data_reason, datetime_ends, ipv4_addr, banned_ipv4_addr)
        VALUES (%s, %s, %s, INET_ATON(%s), (
          SELECT
            p.ipv4_addr
          FROM reports r
          JOIN posts p ON p.id = r.post_id
          WHERE
            r.id = %s
        ))
      """, (ban['report_id'], ban['reason'], ban['datetime_ends'], ipv4_addr, ban['report_id'],))
    else:
      rows_inserted = cursor.execute("""
        INSERT INTO bans (post_id, data_reason, datetime_ends, ipv4_addr, banned_ipv4_addr)
        VALUES (%s, %s, %s, INET_ATON(%s), (
          SELECT
            p.ipv4_addr
          FROM posts p
          WHERE
            p.id = %s
        ))
      """, (ban['post_id'], ban['reason'], ban['datetime_ends'], ipv4_addr, ban['post_id'],))
    id_inserted = cursor.lastrowid

    if rows_inserted == 1:
      cursor.connection.commit()
      result['status'] = 201
      result['data'] = {
        'id': id_inserted
      }

  return result

