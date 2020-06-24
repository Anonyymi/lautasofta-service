import os
from pony.orm import *
from api.singleton import Singleton

class DbInstance(metaclass=Singleton):
  def __init__(self):
    self.db = Database()
    self.db.bind(
      provider= 'mysql',
      host=     os.getenv('DB_HOST'),
      user=     os.getenv('DB_USER'),
      passwd=   os.getenv('DB_PASSWD'),
      db=       os.getenv('DB_NAME'),
    )
