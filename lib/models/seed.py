#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models import Base, County, User, Restaurant, MenuItem, ReservationReview

if __name__ == '__main__':
    engine = create_engine('sqlite:///db/dishcovery.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # clear existing data
    print("Clearing existing data...")
    session.query(ReservationReview).delete()
    session.query(MenuItem).delete()
    session.query(Restaurant).delete()
    session.query(User).delete()
    session.query(County).delete()
    session.commit()
    
    # Seed Counties
    print("Seeding counties...")
    counties_data = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Malindi"]
    
    counties = [County(name=name) for name in counties_data]
    session.bulk_save_objects(counties)
    session.commit()
    
    # Fetch counties from database to get their IDs
    counties = session.query(County).all()
    county_dict = {c.name: c for c in counties}
    
    # Seed Users
    print("Seeding users...")
    users_data = [
        {"name": "Susan Gakii", "email": "susan@dishcovery.ke", "password": "password123"},
        {"name": "John Kamau", "email": "john@email.com", "password": "password123"},
        {"name": "Mary Wanjiku", "email": "mary@email.com", "password": "password123"},
        {"name": "Peter Omondi", "email": "peter@email.com", "password": "password123"},
    ]
    
    users = [User(name=u["name"], email=u["email"], password=u["password"]) for u in users_data]
    session.bulk_save_objects(users)
    session.commit()
    
    # Fetch users from database to get their IDs
    users = session.query(User).all()
    
    # Seed Restaurants
    print("Seeding restaurants...")
    restaurants_data = [
        {
            "name": "Jiko Restaurant",
            "county": "Nairobi",
            "address": "Tribe Hotel, Village Market, Limuru Road, Nairobi",
            "cuisine": "African",
            "price_range": "2500-4000 KES",
            "phone": "+254207200601",
            "email": "info@tribe-hotel.com",
            "website": "https://www.tribe-hotel.com",
            "special_features": "African fusion cuisine, elegant ambiance",
            "operating_hours": "Mon-Sun: 6:00 AM - 11:00 PM"
        },
        {
            "name": "Hero Restaurant",
            "county": "Nairobi",
            "address": "Trademark Hotel, Village Market, Nairobi",
            "cuisine": "Japanese",
            "price_range": "3000-5000 KES",
            "phone": "+254732186666",
            "email": "info@hero-kenya.com",
            "website": "https://www.hero-kenya.com",
            "special_features": "World-class sushi bar, comic book theme",
            "operating_hours": "Mon-Thu: 5:00 PM - 12:00 AM, Fri-Sat: 5:00 PM - 2:00 AM"
        },
        {
            "name": "Monsoons Restaurant",
            "county": "Mombasa",
            "address": "Jumba Ruins, Mtwapa Beach, Mombasa",
            "cuisine": "Seafood",
            "price_range": "2500-4500 KES",
            "phone": "+254701897540",
            "email": "bandaruins@yahoo.com",
            "website": "https://www.facebook.com/MonsoonsMtwapa",
            "special_features": "Oceanfront location, fresh daily catch",
            "operating_hours": "Mon-Thu: 12:00 PM - 10:00 PM, Fri-Sat: 12:00 PM - 11:00 PM"
        },
        {
            "name": "Roberto's Italian Restaurant",
            "county": "Mombasa",
            "address": "Opposite Premiere Hospital, Links Road, Mombasa",
            "cuisine": "Italian",
            "price_range": "2000-3500 KES",
            "phone": "+254723223399",
            "email": "info@robertoslinksroad.com",
            "website": "https://web.facebook.com/robertoslinksroad",
            "special_features": "Authentic Italian cuisine, central location",
            "operating_hours": "Tue-Sat: 6:00 PM - 10:30 PM"
        },
        {
            "name": "Tilapia Beach Restaurant",
            "county": "Kisumu",
            "address": "Dunga Beach, Kisumu",
            "cuisine": "Kenyan",
            "price_range": "1500-2500 KES",
            "phone": "+254722111222",
            "email": "info@tilapiabeach.com",
            "website": "https://www.tilapiabeach.com",
            "special_features": "Lake Victoria views, fresh tilapia daily",
            "operating_hours": "Mon-Sun: 11:00 AM - 9:00 PM"
        },
        {
            "name": "The Thorn Tree Cafe",
            "county": "Nairobi",
            "address": "Sarova Stanley, Kenyatta Avenue, Nairobi",
            "cuisine": "Continental",
            "price_range": "2000-3500 KES",
            "phone": "+254204222000",
            "email": "info@thorntree.com",
            "website": "https://www.sarovastanley.com",
            "special_features": "Historic meeting point, outdoor seating",
            "operating_hours": "Mon-Sun: 7:00 AM - 10:00 PM"
        }
    ]
    
    restaurants = [
        Restaurant(
            name=r["name"],
            county_id=county_dict[r["county"]].id,
            address=r["address"],
            cuisine=r["cuisine"],
            price_range=r["price_range"],
            phone=r["phone"],
            email=r["email"],
            website=r["website"],
            special_features=r["special_features"],
            operating_hours=r["operating_hours"]
        )
        for r in restaurants_data
    ]
    session.bulk_save_objects(restaurants)
    session.commit()
    
    # Fetch restaurants from database to get their IDs
    restaurants = session.query(Restaurant).all()
    restaurant_dict = {r.name: r for r in restaurants}
    
    # Seed Menu Items (Dishes and Drinks combined)
    print("Seeding menu items...")
    menu_items_data = [
        # Jiko Restaurant - Food
        {"restaurant": "Jiko Restaurant", "name": "Sukuma Ravioli", "description": "Traditional kale wrapped in pasta with African spices", "price": 1200},
        {"restaurant": "Jiko Restaurant", "name": "Kondoo Mchuzi", "description": "Tender lamb stew in rich Swahili sauce", "price": 1800},
        # Jiko Restaurant - Drinks
        {"restaurant": "Jiko Restaurant", "name": "Tusker Beer", "description": "Kenya's premium lager beer", "price": 300},
        {"restaurant": "Jiko Restaurant", "name": "Dawa Cocktail", "description": "Traditional honey and lime vodka cocktail", "price": 600},
        
        # Hero Restaurant - Food
        {"restaurant": "Hero Restaurant", "name": "Octopus and Rhubarb Maki", "description": "Fresh octopus with rhubarb in sushi rice", "price": 1800},
        {"restaurant": "Hero Restaurant", "name": "Salmon Sashimi", "description": "Fresh Atlantic salmon slices with wasabi", "price": 2000},
        # Hero Restaurant - Drinks
        {"restaurant": "Hero Restaurant", "name": "Madafu Sawa", "description": "Coconut water with whisky infusion", "price": 700},
        {"restaurant": "Hero Restaurant", "name": "Sake Flight", "description": "Selection of premium Japanese sake", "price": 1200},
        
        # Monsoons Restaurant - Food
        {"restaurant": "Monsoons Restaurant", "name": "Seafood Platter", "description": "Fresh lobster, prawns, and calamari", "price": 4500},
        {"restaurant": "Monsoons Restaurant", "name": "Pili Pili Lobster", "description": "Grilled lobster with spicy Swahili sauce", "price": 3500},
        # Monsoons Restaurant - Drinks
        {"restaurant": "Monsoons Restaurant", "name": "Tropical Fruit Punch", "description": "Blend of fresh tropical fruits", "price": 400},
        {"restaurant": "Monsoons Restaurant", "name": "White Wine Selection", "description": "Curated international whites", "price": 800},
        
        # Roberto's - Food
        {"restaurant": "Roberto's Italian Restaurant", "name": "Seafood Pizza", "description": "Wood-fired pizza with fresh seafood", "price": 1400},
        {"restaurant": "Roberto's Italian Restaurant", "name": "Beef Cheeks", "description": "Slow-cooked beef cheeks in red wine", "price": 1800},
        # Roberto's - Drinks
        {"restaurant": "Roberto's Italian Restaurant", "name": "Aperol Spritz", "description": "Classic Italian cocktail with prosecco", "price": 600},
        {"restaurant": "Roberto's Italian Restaurant", "name": "Espresso", "description": "Authentic Italian espresso", "price": 200},
        
        # Tilapia Beach - Food
        {"restaurant": "Tilapia Beach Restaurant", "name": "Fried Tilapia", "description": "Fresh tilapia from Lake Victoria", "price": 1200},
        {"restaurant": "Tilapia Beach Restaurant", "name": "Ugali and Fish", "description": "Traditional Kenyan meal", "price": 900},
        # Tilapia Beach - Drinks
        {"restaurant": "Tilapia Beach Restaurant", "name": "Fresh Passion Juice", "description": "Pure passion fruit juice", "price": 250},
        
        # Thorn Tree - Food
        {"restaurant": "The Thorn Tree Cafe", "name": "Club Sandwich", "description": "Classic triple-decker sandwich", "price": 1100},
        {"restaurant": "The Thorn Tree Cafe", "name": "Beef Burger", "description": "Juicy beef patty with fixings", "price": 1300},
        # Thorn Tree - Drinks
        {"restaurant": "The Thorn Tree Cafe", "name": "Kenya Coffee", "description": "Freshly brewed local coffee", "price": 300},
    ]
    
    menu_items = [
        MenuItem(
            restaurant_id=restaurant_dict[m["restaurant"]].id,
            name=m["name"],
            description=m["description"],
            price=m["price"]
        )
        for m in menu_items_data
    ]
    session.bulk_save_objects(menu_items)
    session.commit()
    
    # Seed Reservations
    print("Seeding reservations...")
    tomorrow = datetime.now() + timedelta(days=1)
    next_week = datetime.now() + timedelta(days=7)
    
    reservations_data = [
        {"restaurant": "Jiko Restaurant", "user_idx": 0, "reserved_for": 4, "time": tomorrow.replace(hour=19, minute=0)},
        {"restaurant": "Hero Restaurant", "user_idx": 1, "reserved_for": 2, "time": tomorrow.replace(hour=20, minute=0)},
        {"restaurant": "Monsoons Restaurant", "user_idx": 2, "reserved_for": 6, "time": next_week.replace(hour=18, minute=30)},
        {"restaurant": "Roberto's Italian Restaurant", "user_idx": 3, "reserved_for": 3, "time": next_week.replace(hour=19, minute=30)},
    ]
    
    reservations = [
        ReservationReview(
            restaurant_id=restaurant_dict[r["restaurant"]].id,
            user_id=users[r["user_idx"]].id,
            reserved_for=r["reserved_for"],
            reservation_time=r["time"]
        )
        for r in reservations_data
    ]
    session.bulk_save_objects(reservations)
    session.commit()
    
    # Seed Reviews
    print("Seeding reviews...")
    reviews_data = [
        {"restaurant": "Jiko Restaurant", "user_idx": 0, "rating": 5, "text": "Amazing African fusion! The Sukuma Ravioli was incredible."},
        {"restaurant": "Jiko Restaurant", "user_idx": 1, "rating": 4, "text": "Great ambiance and excellent service. Highly recommend!"},
        {"restaurant": "Hero Restaurant", "user_idx": 2, "rating": 5, "text": "Best sushi in Nairobi! The atmosphere is fantastic."},
        {"restaurant": "Hero Restaurant", "user_idx": 0, "rating": 4, "text": "Creative dishes and great cocktails."},
        {"restaurant": "Monsoons Restaurant", "user_idx": 3, "rating": 4, "text": "Fresh seafood with a beautiful ocean view. Will return!"},
        {"restaurant": "Monsoons Restaurant", "user_idx": 1, "rating": 5, "text": "The Pili Pili Lobster is to die for!"},
        {"restaurant": "Roberto's Italian Restaurant", "user_idx": 0, "rating": 5, "text": "Authentic Italian food that reminds me of Italy!"},
        {"restaurant": "Roberto's Italian Restaurant", "user_idx": 2, "rating": 4, "text": "Great pasta and friendly service."},
        {"restaurant": "Tilapia Beach Restaurant", "user_idx": 3, "rating": 4, "text": "Fresh fish right from the lake. Great local experience."},
        {"restaurant": "The Thorn Tree Cafe", "user_idx": 1, "rating": 4, "text": "Historic spot with good food."},
    ]
    
    reviews = [
        ReservationReview(
            restaurant_id=restaurant_dict[r["restaurant"]].id,
            user_id=users[r["user_idx"]].id,
            rating=r["rating"],
            review_text=r["text"]
        )
        for r in reviews_data
    ]
    session.bulk_save_objects(reviews)
    session.commit()
    
    # Update restaurant ratings based on reviews
    print("Updating restaurant ratings...")
    for restaurant in restaurants:
        reviews = session.query(ReservationReview).filter(
            ReservationReview.restaurant_id == restaurant.id,
            ReservationReview.rating.isnot(None)
        ).all()
        if reviews:
            avg_rating = sum(rev.rating for rev in reviews) / len(reviews)
            restaurant.rating = avg_rating
    session.commit()
    
    print("Seeding complete!")
    print(f"Created {len(counties)} counties")
    print(f"Created {len(users)} users")
    print(f"Created {len(restaurants)} restaurants")
    print(f"Created {len(menu_items)} menu items")
    print(f"Created {len(reservations)} reservations")
    print(f"Created {len(reviews)} reviews")