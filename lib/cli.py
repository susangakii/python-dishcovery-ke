#!/usr/bin/env python3

from helpers import (
    exit_program,
    list_all_restaurants,
    search_restaurants_by_county,
    search_restaurants_by_cuisine,
    add_restaurant,
    update_restaurant,
    view_restaurant_details,
    delete_restaurant,
    search_menu_items,
    add_menu_item,
    update_menu_item,
    view_menu_item_details,
    delete_menu_item,
    list_all_users,
    view_user_details,
    add_user,
    update_user,
    delete_user,
    make_reservation,
    view_reservations,
    update_reservation,
    view_reservation_details,
    delete_reservation,
    add_review,
    view_restaurant_reviews,
    update_review,
    view_review_details,
    delete_review
)

def main_menu():
    """Display main menu"""
    print("\n" + "=" * 80)
    print("🍽️  DISHCOVERY KE - RESTAURANT DISCOVERY SYSTEM  🍽️".center(80))
    print("=" * 80)
    print("\n📋 MAIN MENU:")
    print("-" * 80)
    print("    RESTAURANTS")
    print("  1. View All Restaurants")
    print("  2. Search Restaurants by County")
    print("  3. Search Restaurants by Cuisine")
    print("  4. View Restaurant Details (by ID)")
    print("  5. Add New Restaurant")
    print("  6. Update Restaurant")
    print("  7. Delete Restaurant")
    print("-" * 80)
    print("   MENU ITEMS")
    print("  8. Search Menu Items")
    print("  9. View Menu Item Details (by ID)")
    print("  10. Add Menu Item")
    print("  11. Update Menu Item")
    print("  12. Delete Menu Item")
    print("-" * 80)
    print("   USERS")
    print("  13. View All Users")
    print("  14. View User Details (by ID)")
    print("  15. Add New User")
    print("  16. Update User")
    print("  17. Delete User")
    print("-" * 80)
    print("   RESERVATIONS")
    print("  18. Make Reservation")
    print("  19. View Restaurant Reservations")
    print("  20. View Reservation Details (by ID)")
    print("  21. Update Reservation")
    print("  22. Delete Reservation")
    print("-" * 80)
    print("   REVIEWS")
    print("  23. Add Review")
    print("  24. View Restaurant Reviews")
    print("  25. View Review Details (by ID)")
    print("  26. Update Review")
    print("  27. Delete Review")
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
            delete_restaurant()
        elif choice == "8":
            search_menu_items()
        elif choice == "9":
            view_menu_item_details()
        elif choice == "10":
            add_menu_item()
        elif choice == "11":
            update_menu_item()
        elif choice == "12":
            delete_menu_item()
        elif choice == "13":
            list_all_users()
        elif choice == "14":
            view_user_details()
        elif choice == "15":
            add_user()
        elif choice == "16":
            update_user()
        elif choice == "17":
            delete_user()
        elif choice == "18":
            make_reservation()
        elif choice == "19":
            view_reservations()
        elif choice == "20":
            view_reservation_details()
        elif choice == "21":
            update_reservation()
        elif choice == "22":
            delete_reservation()
        elif choice == "23":
            add_review()
        elif choice == "24":
            view_restaurant_reviews()
        elif choice == "25":
            view_review_details()
        elif choice == "26":
            update_review()
        elif choice == "27":
            delete_review()
        else:
            print("\n❌ Invalid choice. Please enter a number from 0-27.")
        
        input("\n📍 Press Enter to continue...")

if __name__ == "__main__":
    main()