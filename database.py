from config import POSTGRES
from sqlalchemy import create_engine

engine = create_engine(POSTGRES)
db = engine.connect()