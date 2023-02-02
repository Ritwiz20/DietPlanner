from os import environ, getcwd, path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
load_dotenv(path.join(getcwd(), '.env'))

SECRET_KEY = environ.get("SECRET_KEY")

db = SQLAlchemy()
db_string = "postgresql+psycopg2://postgres:password@localhost:5432/dietPlanner"

my_db = create_engine(db_string)

Session = sessionmaker(db)
sess =  Session()

