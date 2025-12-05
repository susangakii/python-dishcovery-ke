#!/usr/bin/env python3

from helpers import (
    exit_program,
    list_all_restaurants,
    search_restaurants_by_county,
    search_restaurants_by_cuisine,
    add_restaurant,
    update_restaurant,
    view_restaurant_details,
    search_menu_items,
    add_menu_item,
    update_menu_item,
    make_reservation,
    view_reservations,
    update_reservation,
    add_review,
    view_restaurant_reviews,
    update_review
)

def main_menu():
    """Display main menu"""
    print("\n" + "=" * 80)
    print("🍽️  DISHCOVERY KE - RESTAURANT DISCOVERY SYSTEM  🍽️".center(80))
    print("=" * 80)
    print("\n📋 MAIN MENU:")
    print("-" * 80)
    print("  1. View All Restaurants")
    print("  2. Search Restaurants by County")
    print("  3. Search Restaurants by Cuisine")
    print("  4. View Restaurant Details")
    print("  5. Add New Restaurant")
    print("  6. Update Restaurant")
    print("-" * 80)
    print("  7. Search Menu Items")
    print("  8. Add Menu Item to Restaurant")
    print("  9. Update Menu Item")
    print("-" * 80)
    print("  10. Make Reservation")
    print("  11. View Restaurant Reservations")
    print("  12. Update Reservation")
    print("-" * 80)
    print("  13. Add Review")
    print("  14. View Restaurant Reviews")
    print("  15. Update Review")
    print("-" * 80)
    print("  0. Exit")
    print("=" * 80)

def main():
    """Main CLI loop"""
    print("\n" + "=" * 80)
    print("🍽️  WELCOME TO DISHCOVERY KE!  🍽️".center(80))
    print("Discover Kenya's Best Dining Experiences".center(80))
    print("=" * 80)
    
    while True:
        main_menu()
        choice = input("\n👉 Enter your choice: ").strip()
        
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_all_restaurants()
        elif choice == "2":
            search_restaurants_by_county()
        elif choice == "3":
            search_restaurants_by_cuisine()
        elif choice == "4":
            view_restaurant_details()
        elif choice == "5":
            add_restaurant()
        elif choice == "6":
            update_restaurant()
        elif choice == "7":
            search_menu_items()
        elif choice == "8":
            add_menu_item()
        elif choice == "9":
            update_menu_item()
        elif choice == "10":
            make_reservation()
        elif choice == "11":
            view_reservations()
        elif choice == "12":
            update_reservation()
        elif choice == "13":
            add_review()
        elif choice == "14":
            view_restaurant_reviews()
        elif choice == "15":
            update_review()
        else:
            print("\n❌ Invalid choice. Please enter a number from 0-15.")
        
        input("\n📍 Press Enter to continue...")

if __name__ == "__main__":
    main()