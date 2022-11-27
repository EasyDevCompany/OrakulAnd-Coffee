from sqlalchemy.orm import declarative_base
from .session import engine

Base = declarative_base(bind=engine)
