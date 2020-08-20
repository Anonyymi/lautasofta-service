import os
import pymysql.cursors

class DbInstance():
  instance: pymysql.Connection

  def __init__(self):
    self.instance = pymysql.connect(
      host=         os.getenv('DB_HOST'),
      user=         os.getenv('DB_USER'),
      password=     os.getenv('DB_PASSWD'),
      db=           os.getenv('DB_NAME'),
      cursorclass=  pymysql.cursors.DictCursor
    )
  
  def get_instance(self):
    return self.instance
