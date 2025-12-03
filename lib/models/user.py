from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # relationships
    reviews = relationship('Review', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    @classmethod
    def create(cls, session, name, email, password):
        # create a new user
        user = cls(name=name, email=email, password=password)
        session.add(user)
        session.commit()
        return user
    
    @classmethod
    def get_all(cls, session):
        # get all users
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, user_id):
        # find user by ID
        return session.query(cls).filter(cls.id == user_id).first()
    
    @classmethod
    def find_by_email(cls, session, email):
        # find user by email
        return session.query(cls).filter(cls.email == email).first()
    
    def update(self, session, name=None, email=None, password=None):
        # update user attributes
        if name:
            self.name = name
        if email:
            self.email = email
        if password:
            self.password = password
        session.commit()
    
    def delete(self, session):
        # delete this user
        session.delete(self)
        session.commit()