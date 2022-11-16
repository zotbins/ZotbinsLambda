from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = create_engine("postgresql://postgres:password@localhost:5432/postgres")
Session = sessionmaker(db)
#session = Session()
session = "test"
