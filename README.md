# User Auth Backend

A secure authentication API built with FastAPI and Supabase.

## Features
* **Sign Up / Login**: User registration and JWT-based authentication via Supabase.
* **Public & Protected Routes**: Examples of both open endpoints and secure endpoints protected by HTTPBearer.
* **Dashboard & Profile**: Secure endpoints that verify user identity dynamically.
* **Swagger UI**: Built-in, interactive documentation (`/docs`) with Bearer token authentication support.

## Running Locally

1. Create a `.env` file with your `SUPABASE_URL` and `SUPABASE_KEY`.
2. Install requirements.
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
4. Access the API at `http://localhost:8000/docs`.
