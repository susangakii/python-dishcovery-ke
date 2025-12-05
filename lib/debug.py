#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import County, User, Restaurant, MenuItem, ReservationReview

if __name__ == '__main__':
    engine = create_engine('sqlite:///models/db/dishcovery.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    counties = session.query(County).all()
    users = session.query(User).all()
    restaurants = session.query(Restaurant).all()
    menu_items = session.query(MenuItem).all()
    reservations = ReservationReview.get_all_reservations(session)
    reviews = ReservationReview.get_all_reviews(session)
    
    print("\n" + "=" * 60)
    print("TESTING DISHCOVERY KE")
    print("=" * 60)
    
    # County tests
    print("\n COUNTY TESTS")
    print("-" * 60)
    c = counties[0]
    print(f"County: {c.name} | Restaurants: {len(c.restaurants)}")
    print(f"Find by name: {County.find_by_name(session, c.name).name}")
    
    # User tests
    print("\n USER TESTS")
    print("-" * 60)
    u = users[0]
    print(f"User: {u.name} ({u.email})")
    print(f"Reservations: {len(ReservationReview.find_reservations_by_user(session, u.id))}")
    print(f"Reviews: {len(ReservationReview.find_reviews_by_user(session, u.id))}")
    
    # Restaurant tests
    print("\n RESTAURANT TESTS")
    print("-" * 60)
    r = restaurants[0]
    print(f"Restaurant: {r.name} | {r.county.name}")
    print(f"Cuisine: {r.cuisine} | Rating: {r.rating:.1f}⭐")
    print(f"Menu: {len(r.menu_items)} items | Hours: {r.operating_hours}")
    print(f"Find by county: {len(Restaurant.find_by_county(session, r.county_id))}")
    
    # MenuItem tests
    print("\n MENU ITEM TESTS")
    print("-" * 60)
    m = menu_items[0]
    print(f"Item: {m.name} ({m.price} KES) at {m.restaurant.name}")
    print(f"Search 'Ravioli': {len(MenuItem.search_by_name(session, 'Ravioli'))} found")
    
    # Reservation tests
    print("\n RESERVATION TESTS")
    print("-" * 60)
    if reservations:
        res = reservations[0]
        print(f"Reservation: {res.user.name} at {res.restaurant.name}")
        print(f"For {res.reserved_for} people at {res.reservation_time}")
        print(f"Is reservation: {res.is_reservation} | Is review: {res.is_review}")
    
    # Review tests
    print("\n REVIEW TESTS")
    print("-" * 60)
    if reviews:
        rev = reviews[0]
        print(f"Review: {rev.rating_stars} by {rev.user.name}")
        print(f"Restaurant: {rev.restaurant.name}")
        print(f"Is reservation: {rev.is_reservation} | Is review: {rev.is_review}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS COMPLETED")
    print("=" * 60 + "\n")
    
    import ipdb; ipdb.set_trace()