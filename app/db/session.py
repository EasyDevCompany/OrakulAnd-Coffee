from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# engine = create_engine("sqlite:///orakul.db")
engine = create_engine(settings.SYNC_SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
