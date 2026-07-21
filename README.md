# Hotel Management System
**Version:** Beta 0.1

## About The Project
This project was created as a junior developer initiative for educational purposes. The main goal was to deeply understand how RESTful APIs work, what databases are really used for in a "production-like" environment, and how to securely connect user inputs with backend logic. 

*Note: Currently, there is no frontend implemented. The focus is strictly on building a robust, secure, and efficient backend architecture.*

## Project Structure & Architecture

The application is divided into four main modules, separating the database configuration, data validation, business logic, and API endpoints:

### 1. `database.py` (Database Setup & ORM)
Handles the SQLite3 database connection and structure.
* Contains 3 main tables (classes): `Hotel` (for rooms), `Reservations`, and `CancelReservations`.
* Utilizes Foreign Keys referencing `Hotel.ID` to maintain relational data integrity.
* Implements the `get_db()` generator function for secure connection management (Dependency Injection). It opens a database session for each endpoint and guarantees safe closure after the function ends, preventing connection leaks.

### 2. `models.py` (Data Validation / Schemas)
Powered by **Pydantic** to strictly control and validate user inputs before they reach the database.
* Contains 4 validation classes (3 referring to the database operations and 1 for checking room availability).
* Defines required data types, sets default values, and uses Regex patterns (e.g., for user names) to counteract invalid or malicious inputs.

### 3. `crud.py` (Business Logic)
The core engine of the application holding functions controlled by Pydantic validators. 
Contains 4 clearly named functions:
* `add_hotel_room`
* `make_reservation`
* `cancel_reservation`
* `show_available_rooms`

**Security & Error Handling:** `try/except` blocks are used extensively to prevent unsecure or unwanted database changes. If a function succeeds, it returns a simple message to the user. If it fails, the exception is caught, the database transaction is rolled back, and a controlled `HTTPException` is raised to the API layer.

### 4. `main.py` (API Endpoints)
The main entry point where the FastAPI application connects with the backend logic.
* Exposes 4 endpoints: `3x POST` (creating data) and `1x GET` (querying data).
* Leverages FastAPI's `Depends(get_db)` to automatically open and close sessions. Even if a connection breaks or an error occurs mid-request, this guarantees that the database session will be securely closed and the database will not be "infected" or locked.

## How to Run

1. Clone the repository to your local machine.
2. Install the required dependencies (FastAPI, Uvicorn, SQLAlchemy, Pydantic).
3. Run the development server using Uvicorn:
   ```bash
   uvicorn main:app --reload
