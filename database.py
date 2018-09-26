import os
from sqlalchemy import create_engine
user='dbc'
pasw='dbc'
host="blue9510.labs.teradata.com"
td_engine = create_engine('teradata://'+ user +':' + pasw + '@'+ host + ':22/')
conn =td_engine.connect()
td_engine.execute('select database;')