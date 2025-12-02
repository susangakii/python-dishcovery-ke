from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///dishcovery.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# import models
from models.county import County
from models.user import User
from models.restaurant import Restaurant
from models.dish import Dish
from models.drink import Drink
from models.review import Review
from models.operating_hour import OperatingHour