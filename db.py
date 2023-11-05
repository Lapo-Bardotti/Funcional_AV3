from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = 'user'
password = 'pass'
host = '127.0.0.1'
port = 3306
database = 'my_database'

engine = create_engine(
    url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        user, password, host, port, database
    )
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
