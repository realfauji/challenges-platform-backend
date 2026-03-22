# Challenge Platform Backend (FastAPI + MongoDB)

## Overview

This project is a backend service for a **Challenge Platform** where users can:

* Register and login
* View active challenges
* Join challenges
* Update their progress

The system is built with a focus on:

* Clean API design
* Secure authentication
* Proper data modeling
* Scalable architecture

---

## Tech Stack

* **Backend:** FastAPI
* **Database:** MongoDB (Motor - async driver)
* **Authentication:** JWT (Access + Refresh Token)
* **Validation:** Pydantic

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd challenge-platform
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file:

```env
MONGODB_URL=your_db_url
DB_NAME=challenge_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256

ACCESS_TOKEN=30
REFRESH_TOKEN=7
```

### 5. Run Server

```bash
python main.py
```

---

## Authentication Flow

### 1. Login

* Uses `OAuth2PasswordRequestForm`
* Returns:

  * `access_token`
  * `refresh_token`

### 2. Access Token

* Short-lived
* Used for protected routes
* Passed via:

```
Authorization: Bearer <token>
```

### 3. Refresh Token

* Long-lived
* Used to generate new access tokens

---

## Data Models

### Users (`user_details`)

* email
* password (hashed)
* created_at

---

### Challenges (`challenges`)

* title
* description
* target_value
* duration_days
* is_active
* created_at
* created_by (user_id)

---

### User Challenges (`user_challenges`)

* user_id
* challenge_id
* joined_at
* progress

---

## API Endpoints

### Auth

#### Register

```
POST /auth/register
```

#### Login

```
POST /auth/login
```

#### Refresh Token

```
POST /auth/refresh
```

---

### Challenges

#### Get Active Challenges

```
GET /challenges/get-challenges
```

#### Create Challenge (Protected)

```
POST /challenges/create-challenges
```

---

### Join Challenge

```
POST /challenges/{challenge_id}/join
```

✔ Prevents duplicate joins
✔ Validates challenge existence

---

### Update Progress

```
PUT /challenges/progress
```

✔ Users can only update their own progress

---

## Security Features

* Password hashing using bcrypt
* JWT-based authentication
* Protected routes using dependency injection
* User-specific data access control

---

## Design Decisions

* Used **separate collections** for challenges and user participation for better scalability
* Stored `user_id` as string for easier cross-collection mapping
* Implemented **stateless refresh token flow** (can be extended to DB storage)

---

## Possible Improvements

* Store refresh tokens in DB (for revocation & logout)
* Add role-based access (admin/user)
* Add pagination for challenges
* Add logging & monitoring

---

## Testing

You can test APIs via:

* Swagger UI → `http://127.0.0.1:8000/docs`
* Postman

---

## Author Notes

This project demonstrates:

* Backend fundamentals
* Authentication handling
* Async database operations
* Clean modular architecture

---

