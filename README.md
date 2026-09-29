# Auth Login & Protect API

A secure REST API built with **Python, FastAPI, and Supabase Auth**.

This project demonstrates user registration, login, JWT-based authentication, protected API routes, reusable authentication dependencies, logout, and Swagger UI documentation.

## Features

* User Sign Up
* User Log In
* JWT access-token authentication
* Protected API endpoints
* Reusable FastAPI authentication dependency
* Public API endpoint
* User profile endpoint
* Protected dashboard endpoint
* Logout endpoint
* Interactive Swagger UI
* Environment variables for Supabase credentials

## Tech Stack

* Python 3.10+
* FastAPI
* Supabase Auth
* Uvicorn
* Pydantic
* python-dotenv
* Git & GitHub

## Project Structure

```text
auth-login-protect/
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd auth-login-protect
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv myenv
myenv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Supabase

Create a project on Supabase.

Get your:

* Project URL
* Anon Key

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
```

**Never commit your `.env` file to GitHub.**

### 5. Start the server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint               | Authentication | Description                       |
| ------ | ---------------------- | -------------- | --------------------------------- |
| POST   | `/auth/signup`         | No             | Create a new user                 |
| POST   | `/auth/login`          | No             | Authenticate user and receive JWT |
| POST   | `/auth/logout`         | Yes            | Log out authenticated user        |
| GET    | `/public/info`         | No             | Access public information         |
| GET    | `/protected/profile`   | Yes            | Get authenticated user's profile  |
| GET    | `/protected/dashboard` | Yes            | Access protected dashboard        |

## Authentication Flow

The authentication process works as follows:

```text
Client
   │
   │ Email + Password
   ▼
Supabase Auth
   │
   │ Access Token (JWT)
   ▼
Client
   │
   │ Authorization: Bearer <JWT>
   ▼
FastAPI
   │
   │ Extract JWT
   ▼
Authentication Dependency
   │
   │ Verify token
   ▼
Supabase
   │
   ├── Valid → Protected Route
   │
   └── Invalid → 401 Unauthorized
```

## Sign Up

Endpoint:

```text
POST /auth/signup
```
