from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user", "postgres")
PASSWORD = os.getenv("password", "password")
HOST = os.getenv("host", "localhost")
PORT = os.getenv("port", "5432")
DBNAME = os.getenv("dbname", "test_db")


# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


 # Configuration de JWT
SECRET_KEY = os.getenv("SECRET_KEY")