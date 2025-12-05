import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from datetime import datetime
from models import Session, County, User, Restaurant, MenuItem, ReservationReview

def exit_program():
    """Exit the application"""
    print("\n🍽️  Thank you for using DishCovery KE! Goodbye! 🍽️\n")
    exit()

def get_input(prompt, required=True):
    """Helper to get user input"""
    value = input(prompt).strip()
    if required and not value:
        return None
    return value

def safe_int(value):
    """Safely convert to int"""
    try:
        return int(value)
    except ValueError:
        return None

# Restaurant Functions
def list_all_restaurants():
    """List all restaurants"""
    session = Session()
    restaurants = Restaurant.get_all(session)
    
    if not restaurants:
        print("\n❌ No restaurants found.")
        session.close()
        return
    
    print(f"\n🍽️  All Restaurants ({len(restaurants)} found):")
    print("-" * 80)
    for r in restaurants:
        print(f"\n  ID: {r.id} - {r.name} ({r.county.name})")
        print(f"  {r.cuisine} | {r.price_range} | {'⭐' * int(r.rating)} ({r.rating:.1f})")
    session.close()

def search_restaurants_by_county():
    """Search restaurants by county"""
    session = Session()
    county_name = get_input("\nEnter county name: ")
    
    county = County.find_by_name(session, county_name)
    if not county:
        print(f"\n❌ County '{county_name}' not found.")
        session.close()
        return
    
    restaurants = Restaurant.find_by_county(session, county.id)
    if not restaurants:
        print(f"\n❌ No restaurants in {county_name}.")
        session.close()
        return
    
    print(f"\n🍽️  Restaurants in {county_name}:")
    for r in restaurants:
        print(f"  ID: {r.id} - {r.name} | {r.cuisine} | {'⭐' * int(r.rating)}")
    session.close()

def search_restaurants_by_cuisine():
    """Search restaurants by cuisine"""
    session = Session()
    cuisine = get_input("\nEnter cuisine type: ")
    
    restaurants = Restaurant.find_by_cuisine(session, cuisine)
    if not restaurants:
        print(f"\n❌ No {cuisine} restaurants found.")
        session.close()
        return
    
    print(f"\n🍽️  {cuisine} Restaurants:")
    for r in restaurants:
        print(f"  ID: {r.id} - {r.name} ({r.county.name}) | {'⭐' * int(r.rating)}")
    session.close()

def add_restaurant():
    """Add a new restaurant"""
    session = Session()
    print("\n➕ Add New Restaurant")
    
    name = get_input("Restaurant name: ")
    county_name = get_input("County name: ")
    
    county = County.find_by_name(session, county_name)
    if not county:
        print(f"❌ County not found.")
        session.close()
        return
    
    cuisine = get_input("Cuisine: ")
    price_range = get_input("Price range: ")
    phone = get_input("Phone: ")
    hours = get_input("Operating hours: ")
    
    try:
        restaurant = Restaurant.create(session, name, county.id, cuisine=cuisine,
                                      price_range=price_range, phone=phone, operating_hours=hours)
        print(f"✅ Restaurant added! ID: {restaurant.id}")
    except Exception as e:
        print(f"❌ Error: {e}")
    session.close()

def update_restaurant():
    """Update restaurant"""
    session = Session()
    print("\n✏️  Update Restaurant")
    
    rest_id = safe_int(get_input("Restaurant ID: "))
    restaurant = Restaurant.find_by_id(session, rest_id) if rest_id else None
    
    if not restaurant:
        print("❌ Restaurant not found.")
        session.close()
        return
    
    print(f"Updating: {restaurant.name} (leave blank to keep current)")
    restaurant.update(session,
        name=get_input(f"Name [{restaurant.name}]: ", False),
        cuisine=get_input(f"Cuisine [{restaurant.cuisine}]: ", False),
        phone=get_input(f"Phone [{restaurant.phone}]: ", False),
        operating_hours=get_input(f"Hours [{restaurant.operating_hours}]: ", False)
    )
    print("✅ Updated!")
    session.close()

def view_restaurant_details():
    """View restaurant details"""
    session = Session()
    rest_id = safe_int(get_input("\nRestaurant ID: "))
    restaurant = Restaurant.find_by_id(session, rest_id) if rest_id else None
    
    if not restaurant:
        print("❌ Restaurant not found.")
        session.close()
        return
    
    print(f"\n🍽️  {restaurant.name}")
    print("=" * 80)
    print(f"Location: {restaurant.county.name} | Cuisine: {restaurant.cuisine}")
    print(f"Rating: {'⭐' * int(restaurant.rating)} ({restaurant.rating:.1f}/5)")
    print(f"Phone: {restaurant.phone} | Hours: {restaurant.operating_hours}")
    
    menu = MenuItem.find_by_restaurant(session, rest_id)
    if menu:
        print(f"\n🍽️  Menu ({len(menu)} items):")
        for m in menu:
            print(f"  • {m.name} - {m.price} KES")
    
    reservations = ReservationReview.find_reservations_by_restaurant(session, rest_id)
    if reservations:
        print(f"\n📅 Reservations ({len(reservations)}):")
        for res in reservations:
            print(f"  • {res.user.name} - {res.reserved_for} people")
    
    reviews = ReservationReview.find_reviews_by_restaurant(session, rest_id)
    if reviews:
        print(f"\n⭐ Reviews ({len(reviews)}):")
        for rev in reviews:
            print(f"  {rev.rating_stars} - {rev.user.name}: \"{rev.review_text}\"")
    session.close()

# Menu Item Functions
def search_menu_items():
    """Search menu items"""
    session = Session()
    item_name = get_input("\nEnter item name: ")
    
    items = MenuItem.search_by_name(session, item_name)
    if not items:
        print(f"❌ No items found.")
        session.close()
        return
    
    print(f"\n🍽️  Menu Items matching '{item_name}':")
    for m in items:
        print(f"  {m.name} ({m.price} KES) at {m.restaurant.name}")
    session.close()

def add_menu_item():
    """Add menu item"""
    session = Session()
    print("\n➕ Add Menu Item")
    
    rest_id = safe_int(get_input("Restaurant ID: "))
    if not Restaurant.find_by_id(session, rest_id):
        print("❌ Restaurant not found.")
        session.close()
        return
    
    name = get_input("Item name: ")
    description = get_input("Description: ")
    price = float(get_input("Price (KES): "))
    
    try:
        MenuItem.create(session, rest_id, name, description, price)
        print("✅ Menu item added!")
    except Exception as e:
        print(f"❌ Error: {e}")
    session.close()

def update_menu_item():
    """Update menu item"""
    session = Session()
    print("\n✏️  Update Menu Item")
    
    item_id = safe_int(get_input("Menu Item ID: "))
    item = MenuItem.find_by_id(session, item_id) if item_id else None
    
    if not item:
        print("❌ Item not found.")
        session.close()
        return
    
    print(f"Updating: {item.name} (leave blank to keep current)")
    price_str = get_input(f"Price [{item.price}]: ", False)
    
    item.update(session,
        name=get_input(f"Name [{item.name}]: ", False),
        description=get_input(f"Description [{item.description}]: ", False),
        price=float(price_str) if price_str else None
    )
    print("✅ Updated!")
    session.close()

# Reservation Functions
def make_reservation():
    """Make reservation"""
    session = Session()
    print("\n➕ Make Reservation")
    
    rest_id = safe_int(get_input("Restaurant ID: "))
    user_id = safe_int(get_input("User ID: "))
    reserved_for = safe_int(get_input("Number of people: "))
    datetime_str = get_input("Date & time (YYYY-MM-DD HH:MM): ")
    
    try:
        res_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        ReservationReview.create_reservation(session, rest_id, user_id, reserved_for, res_time)
        print("✅ Reservation made!")
    except Exception as e:
        print(f"❌ Error: {e}")
    session.close()

def view_reservations():
    """View reservations"""
    session = Session()
    rest_id = safe_int(get_input("\nRestaurant ID: "))
    restaurant = Restaurant.find_by_id(session, rest_id) if rest_id else None
    
    if not restaurant:
        print("❌ Restaurant not found.")
        session.close()
        return
    
    reservations = ReservationReview.find_reservations_by_restaurant(session, rest_id)
    if not reservations:
        print("❌ No reservations.")
        session.close()
        return
    
    print(f"\n📅 Reservations for {restaurant.name}:")
    for res in reservations:
        print(f"  ID: {res.id} | {res.user.name} - {res.reserved_for} people at {res.reservation_time}")
    session.close()

def update_reservation():
    """Update reservation"""
    session = Session()
    print("\n✏️  Update Reservation")
    
    res_id = safe_int(get_input("Reservation ID: "))
    reservation = ReservationReview.find_by_id(session, res_id) if res_id else None
    
    if not reservation or not reservation.is_reservation:
        print("❌ Reservation not found.")
        session.close()
        return
    
    print(f"Updating reservation for {reservation.user.name}")
    people_str = get_input(f"People [{reservation.reserved_for}]: ", False)
    time_str = get_input(f"New time (YYYY-MM-DD HH:MM): ", False)
    
    try:
        reservation.update(session,
            reserved_for=int(people_str) if people_str else None,
            reservation_time=datetime.strptime(time_str, "%Y-%m-%d %H:%M") if time_str else None
        )
        print("✅ Updated!")
    except Exception as e:
        print(f"❌ Error: {e}")
    session.close()

# Review Functions
def add_review():
    """Add review"""
    session = Session()
    print("\n➕ Add Review")
    
    rest_id = safe_int(get_input("Restaurant ID: "))
    user_id = safe_int(get_input("User ID: "))
    rating = safe_int(get_input("Rating (1-5): "))
    text = get_input("Review text: ")
    
    try:
        ReservationReview.create_review(session, rest_id, user_id, rating, text)
        print("✅ Review added!")
    except Exception as e:
        print(f"❌ Error: {e}")
    session.close()

def view_restaurant_reviews():
    """View reviews"""
    session = Session()
    rest_id = safe_int(get_input("\nRestaurant ID: "))
    restaurant = Restaurant.find_by_id(session, rest_id) if rest_id else None
    
    if not restaurant:
        print("❌ Restaurant not found.")
        session.close()
        return
    
    reviews = ReservationReview.find_reviews_by_restaurant(session, rest_id)
    if not reviews:
        print("❌ No reviews.")
        session.close()
        return
    
    print(f"\n⭐ Reviews for {restaurant.name}:")
    print(f"Average: {'⭐' * int(restaurant.rating)} ({restaurant.rating:.1f}/5)")
    for rev in reviews:
        print(f"  {rev.rating_stars} - {rev.user.name}: \"{rev.review_text}\"")
    session.close()

def update_review():
    """Update review"""
    session = Session()
    print("\n✏️  Update Review")
    
    rev_id = safe_int(get_input("Review ID: "))
    review = ReservationReview.find_by_id(session, rev_id) if rev_id else None
    
    if not review or not review.is_review:
        print("❌ Review not found.")
        session.close()
        return
    
    print(f"Updating review by {review.user.name}")
    rating_str = get_input(f"Rating [{review.rating}]: ", False)
    
    try:
        review.update(session,
            rating=int(rating_str) if rating_str else None,
            review_text=get_input(f"Text [{review.review_text}]: ", False)
        )
        print("✅ Updated!")
    except Exception as e:
        print(f"❌ Error: {e}")
    session.close()