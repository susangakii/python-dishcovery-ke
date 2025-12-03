from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base

class ReservationReview(Base):
    __tablename__ = 'reservations_reviews'
    
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # reservation fields (nullable - only for reservations)
    reserved_for = Column(Integer)  # number of people
    reservation_time = Column(DateTime)
    # review fields (nullable - only for reviews)
    rating = Column(Integer)  # 1-5 stars
    review_text = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now)
    
    # relationships
    restaurant = relationship('Restaurant', back_populates='reservations_reviews')
    user = relationship('User', back_populates='reservations_reviews')
    
    def __repr__(self):
        if self.rating is not None:
            return f"<Review(id={self.id}, rating={self.rating}, restaurant_id={self.restaurant_id})>"
        else:
            return f"<Reservation(id={self.id}, for={self.reserved_for}, restaurant_id={self.restaurant_id})>"
    
    @property
    def is_reservation(self):
        # check if this is a reservation
        return self.reserved_for is not None
    
    @property
    def is_review(self):
        # check if this is a review
        return self.rating is not None
    
    @property
    def rating_stars(self):
        # return rating as stars
        if self.rating:
            return '⭐' * self.rating
        return ''
    
    @classmethod
    def create_reservation(cls, session, restaurant_id, user_id, reserved_for, reservation_time):
        # create a new reservation
        reservation = cls(
            restaurant_id=restaurant_id,
            user_id=user_id,
            reserved_for=reserved_for,
            reservation_time=reservation_time
        )
        session.add(reservation)
        session.commit()
        return reservation
    
    @classmethod
    def create_review(cls, session, restaurant_id, user_id, rating, review_text=None):
        # create a new review
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        review = cls(
            restaurant_id=restaurant_id,
            user_id=user_id,
            rating=rating,
            review_text=review_text
        )
        session.add(review)
        session.commit()
        
        # update restaurant rating
        from models.restaurant import Restaurant
        restaurant = Restaurant.find_by_id(session, restaurant_id)
        if restaurant:
            restaurant.update_rating(session)
        
        return review
    
    @classmethod
    def get_all(cls, session):
        # get all reservations and reviews
        return session.query(cls).all()
    
    @classmethod
    def get_all_reservations(cls, session):
        # get all reservations only
        return session.query(cls).filter(cls.reserved_for.isnot(None)).all()
    
    @classmethod
    def get_all_reviews(cls, session):
        # get all reviews only
        return session.query(cls).filter(cls.rating.isnot(None)).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        # find reservation/review by ID"""
        return session.query(cls).filter(cls.id == id).first()
    
    @classmethod
    def find_reservations_by_restaurant(cls, session, restaurant_id):
        # find reservations by restaurant
        return session.query(cls).filter(
            cls.restaurant_id == restaurant_id,
            cls.reserved_for.isnot(None)
        ).all()
    
    @classmethod
    def find_reviews_by_restaurant(cls, session, restaurant_id):
        # find reviews by restaurant
        return session.query(cls).filter(
            cls.restaurant_id == restaurant_id,
            cls.rating.isnot(None)
        ).all()
    
    @classmethod
    def find_reservations_by_user(cls, session, user_id):
        # find reservations by user
        return session.query(cls).filter(
            cls.user_id == user_id,
            cls.reserved_for.isnot(None)
        ).all()
    
    @classmethod
    def find_reviews_by_user(cls, session, user_id):
        # find reviews by user
        return session.query(cls).filter(
            cls.user_id == user_id,
            cls.rating.isnot(None)
        ).all()
    
    def update(self, session, reserved_for=None, reservation_time=None, 
               rating=None, review_text=None):
        # update reservation or review attributes
        # update reservation fields
        if reserved_for is not None:
            if not self.is_reservation:
                raise ValueError("This is not a reservation")
            self.reserved_for = reserved_for
        
        if reservation_time is not None:
            if not self.is_reservation:
                raise ValueError("This is not a reservation")
            self.reservation_time = reservation_time
        
        # update review fields
        if rating is not None:
            if not self.is_review:
                raise ValueError("This is not a review")
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
            self.rating = rating
            
            # update restaurant rating
            from models.restaurant import Restaurant
            restaurant = Restaurant.find_by_id(session, self.restaurant_id)
            if restaurant:
                restaurant.update_rating(session)
        
        if review_text is not None:
            if not self.is_review:
                raise ValueError("This is not a review")
            self.review_text = review_text
        
        session.commit()

    def delete(self, session):
        # delete this reservation/review
        restaurant_id = self.restaurant_id
        is_review = self.is_review
        
        session.delete(self)
        session.commit()
        
        # update restaurant rating if this was a review
        if is_review:
            from models.restaurant import Restaurant
            restaurant = Restaurant.find_by_id(session, restaurant_id)
            if restaurant:
                restaurant.update_rating(session)