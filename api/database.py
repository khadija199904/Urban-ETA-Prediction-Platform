from sqlalchemy import create_engine 
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker,declarative_base
from api.core.config import DATABASE_URL



engine = create_engine(DATABASE_URL, poolclass=NullPool)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# Test the connection
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("Connection successful!")
    except Exception as e:
        print(f"Failed to connect: {e}")
