from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base

class MenuItem(Base):
    __tablename__ = 'menu_items'
    
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    # relationships
    restaurant = relationship('Restaurant', back_populates='menu_items')
    
    def __repr__(self):
        return f"<MenuItem(id={self.id}, name='{self.name}', price={self.price})>"
    
    @classmethod
    def create(cls, session, restaurant_id, name, description=None, price=None):
        # create a new menu item
        menu_item = cls(restaurant_id=restaurant_id, name=name, description=description, price=price)
        session.add(menu_item)
        session.commit()
        return menu_item
    
    @classmethod
    def get_all(cls, session):
        # get all menu items
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, menu_item_id):
        # find menu item by ID
        return session.query(cls).filter(cls.id == menu_item_id).first()
    
    @classmethod
    def find_by_restaurant(cls, session, restaurant_id):
        # find menu items by restaurant
        return session.query(cls).filter(cls.restaurant_id == restaurant_id).all()
    
    @classmethod
    def search_by_name(cls, session, name):
        # search menu items by name
        return session.query(cls).filter(cls.name.ilike(f'%{name}%')).all()
    
    def update(self, session, restaurant_id=None, name=None, description=None, price=None):
        # update menu item attributes
        if restaurant_id:
            self.restaurant_id = restaurant_id
        if name:
            self.name = name
        if description:
            self.description = description
        if price:
            self.price = price
        session.commit()
    
    def delete(self, session):
        # delete this menu item
        session.delete(self)
        session.commit()