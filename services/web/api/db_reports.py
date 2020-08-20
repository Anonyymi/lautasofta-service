import os
import uuid
from common.dbinstance import DbInstance

def insert_report(report, ipv4_addr):
  # prepare result
  result = {
    'status': 400,
    'data': None
  }

  # check if user has permission to create report
  permitted = False
  with DbInstance().get_instance().cursor() as cursor:
    cursor.execute("""
      SELECT
        a.timestamp_created_report < DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 15 SECOND) AS permission
      FROM anons AS a
      WHERE a.ipv4_addr = INET_ATON(%s)
    """, (ipv4_addr,))
    permitted = cursor.fetchone()
    permitted = True if permitted is None else permitted['permission'] == 1
  
    # create report if permitted
    if permitted:
      # insert/update ipv4_addr row
      rows_anon = cursor.execute("""
        INSERT INTO anons (ipv4_addr, timestamp_created_report) VALUES (INET_ATON(%s), CURRENT_TIMESTAMP)
        ON DUPLICATE KEY UPDATE timestamp_created_report=CURRENT_TIMESTAMP
      """, (ipv4_addr,))

      # insert report
      rows_thread = cursor.execute("""
        INSERT INTO reports (post_id, data_reason, ipv4_addr)
        VALUES (%s, %s, INET_ATON(%s))
      """, (report['post_id'], report['reason'], ipv4_addr,))
      id_inserted = cursor.lastrowid

      # commit if ok
      if rows_anon >= 1 and rows_thread == 1:
        cursor.connection.commit()
        result['status'] = 201
        result['data'] = {
          'id': id_inserted
        }
    else:
      result['status'] = 429
      result['data'] = {
        'message': 'too many requests'
      }

  return result
