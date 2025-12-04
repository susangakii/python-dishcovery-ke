#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import Base, County, User, Restaurant, MenuItem, ReservationReview

if __name__ == '__main__':
    engine = create_engine('sqlite:///dishcovery.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("Clearing existing data...")
    session.query(ReservationReview).delete()
    session.query(MenuItem).delete()
    session.query(Restaurant).delete()
    session.query(User).delete()
    session.query(County).delete()
    session.commit()
    
    print("Seeding counties...")
    counties = [County(name=n) for n in ["Nairobi", "Mombasa", "Kisumu"]]
    session.bulk_save_objects(counties)
    session.commit()
    counties = session.query(County).all()
    county_dict = {c.name: c for c in counties}
    
    print("Seeding users...")
    users = [User(name=n, email=e, password="pass123") for n, e in [
        ("Susan Gakii", "susan@dishcovery.ke"),
        ("John Kamau", "john@email.com")
    ]]
    session.bulk_save_objects(users)
    session.commit()
    users = session.query(User).all()
    
    print("Seeding restaurants...")
    restaurants_data = [
        ("Jiko Restaurant", "Nairobi", "African", "2500-4000 KES", "+254207200601", "Mon-Sun: 6AM-11PM"),
        ("Monsoons Restaurant", "Mombasa", "Seafood", "2500-4500 KES", "+254701897540", "Mon-Sun: 12PM-10PM"),
        ("Tilapia Beach", "Kisumu", "Kenyan", "1500-2500 KES", "+254722111222", "Mon-Sun: 11AM-9PM")
    ]
    restaurants = [Restaurant(
        name=r[0], county_id=county_dict[r[1]].id, cuisine=r[2], 
        price_range=r[3], phone=r[4], operating_hours=r[5]
    ) for r in restaurants_data]
    session.bulk_save_objects(restaurants)
    session.commit()
    restaurants = session.query(Restaurant).all()
    r_dict = {r.name: r for r in restaurants}
    
    print("Seeding menu items...")
    menu_data = [
        ("Jiko Restaurant", "Sukuma Ravioli", "Kale in pasta with African spices", 1200),
        ("Jiko Restaurant", "Tusker Beer", "Kenya's premium lager", 300),
        ("Monsoons Restaurant", "Seafood Platter", "Fresh lobster and prawns", 4500),
        ("Monsoons Restaurant", "Tropical Punch", "Fresh fruit blend", 400),
        ("Tilapia Beach", "Fried Tilapia", "Fresh from Lake Victoria", 1200),
        ("Tilapia Beach", "Passion Juice", "Pure passion fruit", 250)
    ]
    menu_items = [MenuItem(
        restaurant_id=r_dict[m[0]].id, name=m[1], description=m[2], price=m[3]
    ) for m in menu_data]
    session.bulk_save_objects(menu_items)
    session.commit()
    
    print("Seeding reservations...")
    tomorrow = datetime.now() + timedelta(days=1)
    reservations = [
        ReservationReview(restaurant_id=r_dict["Jiko Restaurant"].id, user_id=users[0].id, 
                         reserved_for=4, reservation_time=tomorrow.replace(hour=19)),
        ReservationReview(restaurant_id=r_dict["Monsoons Restaurant"].id, user_id=users[1].id,
                         reserved_for=2, reservation_time=tomorrow.replace(hour=20))
    ]
    session.bulk_save_objects(reservations)
    session.commit()
    
    print("Seeding reviews...")
    reviews_data = [
        ("Jiko Restaurant", 0, 5, "Amazing African fusion!"),
        ("Jiko Restaurant", 1, 4, "Great ambiance and service."),
        ("Monsoons Restaurant", 0, 5, "Fresh seafood with ocean view!"),
        ("Tilapia Beach", 1, 4, "Fresh fish from the lake.")
    ]
    reviews = [ReservationReview(
        restaurant_id=r_dict[r[0]].id, user_id=users[r[1]].id, 
        rating=r[2], review_text=r[3]
    ) for r in reviews_data]
    session.bulk_save_objects(reviews)
    session.commit()
    
    print("Updating restaurant ratings...")
    for restaurant in restaurants:
        reviews = session.query(ReservationReview).filter(
            ReservationReview.restaurant_id == restaurant.id,
            ReservationReview.rating.isnot(None)
        ).all()
        if reviews:
            restaurant.rating = sum(r.rating for r in reviews) / len(reviews)
    session.commit()
    
    print(f"\n✓ Seeding complete!")
    print(f"  {len(counties)} counties | {len(users)} users | {len(restaurants)} restaurants")
    print(f"  {len(menu_items)} menu items | {len(reservations)} reservations | {len(reviews)} reviews")