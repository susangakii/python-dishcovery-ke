from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import Base

class County(Base):
    __tablename__ = 'counties'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    # relationships
    restaurants = relationship('Restaurant', back_populates='county', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<County(id={self.id}, name='{self.name}')>"
    
    @classmethod
    def create(cls, session, name):
        # create a new county
        county = cls(name=name)
        session.add(county)
        session.commit()
        return county
    
    @classmethod
    def get_all(cls, session):
        # get all counties
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, county_id):
        # find county by ID
        return session.query(cls).filter(cls.id == county_id).first()
    
    @classmethod
    def find_by_name(cls, session, name):
        # find county by name
        return session.query(cls).filter(cls.name == name).first()
    
    def delete(self, session):
        # delete this county
        session.delete(self)
        session.commit()