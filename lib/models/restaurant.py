from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base

class Restaurant(Base):
    __tablename__ = 'restaurants'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)
    county_id = Column(Integer, ForeignKey('counties.id'), nullable=False)
    cuisine = Column(String)
    price_range = Column(String)
    phone = Column(String)
    email = Column(String)
    website = Column(String)
    rating = Column(Float, default=0.0)
    special_features = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    
    # relationships
    county = relationship('County', back_populates='restaurants')
    dishes = relationship('Dish', back_populates='restaurant', cascade='all, delete-orphan')
    drinks = relationship('Drink', back_populates='restaurant', cascade='all, delete-orphan')
    reviews = relationship('Review', back_populates='restaurant', cascade='all, delete-orphan')
    operating_hours = relationship('OperatingHour', back_populates='restaurant', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Restaurant(id={self.id}, name='{self.name}', cuisine='{self.cuisine}')>"
    
    @property
    def average_rating(self):
        # calculate average rating from reviews
        if not self.reviews:
            return 0.0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    @classmethod
    def create(cls, session, name, county_id, address=None, cuisine=None, 
            price_range=None, phone=None, email=None, website=None, 
            special_features=None):
        # create a new restaurant
        restaurant = cls(
            name=name,
            county_id=county_id,
            address=address,
            cuisine=cuisine,
            price_range=price_range,
            phone=phone,
            email=email,
            website=website,
            special_features=special_features
        )
        session.add(restaurant)
        session.commit()
        return restaurant
    
    @classmethod
    def get_all(cls, session):
        # get all restaurants
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, restaurant_id):
        # find restaurant by ID
        return session.query(cls).filter(cls.id == restaurant_id).first()
    
    @classmethod
    def find_by_county(cls, session, county_id):
        # find restaurants by county
        return session.query(cls).filter(cls.county_id == county_id).all()
    
    @classmethod
    def find_by_cuisine(cls, session, cuisine):
        # find restaurants by cuisine type
        return session.query(cls).filter(cls.cuisine == cuisine).all()
    
    @classmethod
    def search_by_name(cls, session, name):
        # search restaurants by name
        return session.query(cls).filter(cls.name.ilike(f'%{name}%')).all()
    
    def update(self, session, name=None, address=None, cuisine=None, 
           price_range=None, phone=None, email=None, website=None, 
           special_features=None):
        # update restaurant attributes
        if name:
            self.name = name
        if address:
            self.address = address
        if cuisine:
            self.cuisine = cuisine
        if price_range:
            self.price_range = price_range
        if phone:
            self.phone = phone
        if email:
            self.email = email
        if website:
            self.website = website
        if special_features:
            self.special_features = special_features
        session.commit()
    
    def delete(self, session):
        # delete this restaurant
        session.delete(self)
        session.commit()
    
    def update_rating(self, session):
        # update rating based on reviews
        self.rating = self.average_rating
        session.commit()