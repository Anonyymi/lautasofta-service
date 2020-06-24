import os
from pony.orm import *
from api.singleton import Singleton
from api.dbinstance import DbInstance

db = DbInstance()

class Board(db.db.Entity):
  id = PrimaryKey(int, auto=True)
  name = Required(str)
  description = Required(str)
  flag_hidden = Required(bool)
  flag_nsfw = Required(bool)

class DbModels(metaclass=Singleton):
  def __init__(self):
    db.db.generate_mapping(create_tables=True)
