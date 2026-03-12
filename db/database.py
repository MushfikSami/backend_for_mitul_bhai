from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Format: postgresql://<username>:<password>@<host>/<database_name>
# Change 'localhost' to 'db'
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db:5432/myappdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

  