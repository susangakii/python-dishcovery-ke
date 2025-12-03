#!/usr/bin/env python3

import sys
sys.path.append('models')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import County, User, Restaurant, MenuItem, ReservationReview

if __name__ == '__main__':
    engine = create_engine('sqlite:///dishcovery.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    counties = session.query(County).all()
    users = session.query(User).all()
    restaurants = session.query(Restaurant).all()
    menu_items = session.query(MenuItem).all()
    reservations = session.query(ReservationReview).filter(ReservationReview.reserved_for.isnot(None)).all()
    reviews = session.query(ReservationReview).filter(ReservationReview.rating.isnot(None)).all()
    
    print("\n" + "=" * 60)
    print("TESTING DISHCOVERY KE")
    print("=" * 60)
    
    # Test County methods
    print("\n COUNTY TESTS")
    print("-" * 60)
    county = counties[0]
    print(f"County: {county.name}")
    print(f"  Restaurants: {len(county.restaurants)}")
    print(f"  Find by name: {County.find_by_name(session, county.name).name}")
    print(f"  Find by ID: {County.find_by_id(session, county.id).name}")
    
    # Test User methods
    print("\n USER TESTS")
    print("-" * 60)
    user = users[0]
    print(f"User: {user.name}")
    print(f"  Email: {user.email}")
    user_reservations = ReservationReview.find_reservations_by_user(session, user.id)
    user_reviews = ReservationReview.find_reviews_by_user(session, user.id)
    print(f"  Reservations made: {len(user_reservations)}")
    print(f"  Reviews written: {len(user_reviews)}")
    print(f"  Find by email: {User.find_by_email(session, user.email).name}")
    
    # Test Restaurant methods
    print("\n RESTAURANT TESTS")
    print("-" * 60)
    restaurant = restaurants[0]
    print(f"Restaurant: {restaurant.name}")
    print(f"  County: {restaurant.county.name}")
    print(f"  Cuisine: {restaurant.cuisine}")
    print(f"  Operating Hours: {restaurant.operating_hours}")
    print(f"  Rating: {restaurant.rating:.1f}⭐")
    print(f"  Average rating: {restaurant.average_rating:.1f}")
    print(f"  Menu items: {len(restaurant.menu_items)}")
    rest_reservations = ReservationReview.find_reservations_by_restaurant(session, restaurant.id)
    rest_reviews = ReservationReview.find_reviews_by_restaurant(session, restaurant.id)
    print(f"  Reservations: {len(rest_reservations)}")
    print(f"  Reviews: {len(rest_reviews)}")
    print(f"  Find by county: {len(Restaurant.find_by_county(session, restaurant.county_id))} restaurants")
    print(f"  Find by cuisine: {len(Restaurant.find_by_cuisine(session, restaurant.cuisine))} restaurants")
    
    # Test MenuItem methods
    print("\n MENU ITEM TESTS")
    print("-" * 60)
    menu_item = menu_items[0]
    print(f"Menu Item: {menu_item.name}")
    print(f"  Restaurant: {menu_item.restaurant.name}")
    print(f"  Price: {menu_item.price} KES")
    print(f"  Description: {menu_item.description}")
    print(f"  Search 'Ravioli': {len(MenuItem.search_by_name(session, 'Ravioli'))} items")
    print(f"  Find by restaurant: {len(MenuItem.find_by_restaurant(session, menu_item.restaurant_id))} items")
    
    # Test Reservation methods
    print("\n RESERVATION TESTS")
    print("-" * 60)
    if reservations:
        reservation = reservations[0]
        print(f"Reservation by: {reservation.user.name}")
        print(f"  Restaurant: {reservation.restaurant.name}")
        print(f"  Reserved for: {reservation.reserved_for} people")
        print(f"  Time: {reservation.reservation_time}")
        print(f"  Is reservation: {reservation.is_reservation}")
        print(f"  Is review: {reservation.is_review}")
    print(f"  Total reservations: {len(ReservationReview.get_all_reservations(session))}")
    
    # Test Review methods
    print("\n REVIEW TESTS")
    print("-" * 60)
    if reviews:
        review = reviews[0]
        print(f"Review by: {review.user.name}")
        print(f"  Restaurant: {review.restaurant.name}")
        print(f"  Rating: {review.rating_stars}")
        print(f"  Text: {review.review_text}")
        print(f"  Is reservation: {review.is_reservation}")
        print(f"  Is review: {review.is_review}")
    print(f"  Total reviews: {len(ReservationReview.get_all_reviews(session))}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS COMPLETED")
    print("=" * 60 + "\n")
    
    import ipdb; ipdb.set_trace()