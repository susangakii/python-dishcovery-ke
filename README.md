# DishCovery KE - CLI & ORM

A Python CLI application that helps users discover restaurants across Kenya by searching for dishes and filtering by location and preferences.

## Description

DishCovery KE is a command-line restaurant discovery system built with Python and SQLAlchemy ORM. Users can search for menu items, browse restaurants by county, make reservations, leave reviews, and view detailed restaurant information.

## Features

- County-based restaurant search
- Cuisine, rating, and price range filtering
- Menu item search (dishes and drinks combined)
- Restaurant management (create, view, update)
- Reservation system
- Review and rating system
- Price range filtering

## Technologies Used

- Python 3.8+
- SQLAlchemy (ORM)
- Alembic (Database migrations)
- SQLite (Database)
- Pipenv (Dependency management)

## Database Schema

The application uses 5 related database models:

- **County**: Kenya's counties
- **User**: User accounts
- **Restaurant**: Restaurant details
- **MenuItem**: Menu items (dishes and drinks)
- **ReservationReview**: Combined model for reservations and reviews

### Relationships:
- One County → Many Restaurants
- One Restaurant → Many MenuItems, ReservationsReviews
- One User → Many ReservationsReviews
- ReservationsReviews connects Users to Restaurants with either reservation data OR review data

## Installation

### 1. Clone and Setup

```bash
# Clone repository
git clone <your-repo-url>
cd python-dishcovery-ke

# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell
```

### 2. Initialize Database

```bash
# Navigate to models directory
cd lib/models

# Run migrations
alembic upgrade head

# Seed database
python seed.py
```

## Usage

### Running the Application

From the project root:
```bash
python lib/cli.py
```

Or make it executable:
```bash
chmod +x lib/cli.py
./lib/cli.py
```

### Debugging

```bash
python lib/debug.py
```

## Project Structure

```
python-dishcovery-ke/
├── .venv/
├── lib/
│   ├── cli.py
│   ├── debug.py
│   ├── helpers.py
│   └── models/
│       ├── __init__.py
│       ├── county.py
│       ├── user.py
│       ├── restaurant.py
│       ├── menu_item.py
│       ├── reservation_review.py
│       ├── seed.py
│       ├── alembic.ini
│       └── migrations/
│           ├── env.py
│           ├── script.py.mako
│           └── versions/
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Contributing

This is a Phase 3 educational project. Fork and modify for your own learning.

## License

MIT License

## Author

Susan Gakii - DishCovery KE