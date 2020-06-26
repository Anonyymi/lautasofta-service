import os
import pymysql.cursors
from common.singleton import Singleton

class DbInstance(metaclass=Singleton):
  instance: pymysql.Connection

  def __init__(self):
    self.instance = pymysql.connect(
      host=         os.getenv('DB_HOST'),
      user=         os.getenv('DB_USER'),
      password=     os.getenv('DB_PASSWD'),
      db=           os.getenv('DB_NAME'),
      cursorclass=  pymysql.cursors.DictCursor
    )