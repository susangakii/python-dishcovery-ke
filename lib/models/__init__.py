import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_path = os.path.join(os.path.dirname(__file__), 'db', 'dishcovery.db')
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# import models
from models.county import County
from models.user import User
from models.restaurant import Restaurant
from models.menu_item import MenuItem
from models.reservation_review import ReservationReview

__all__ = ['Base', 'County', 'User', 'Restaurant', 'MenuItem', 'ReservationReview']