import os
from sqlalchemy import create_engine

USER_DB= os.getenv('USER_DB', 'postgres')
PASS_DB= os.getenv('PASS_DB')
POSTGRES = f'postgresql+psycopg2://{USER_DB}:{PASS_DB}@127.0.0.1:5432/data_books'
engine = create_engine(POSTGRES)
db = engine.connect()