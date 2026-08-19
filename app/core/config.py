from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_url = "postgresql://postgres:Ritishreddy@localhost:5432/mybookmyshow"

engine = create_engine(db_url)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()