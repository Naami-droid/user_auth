from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials
from main import app, supabase, AuthCredentials, security

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def sign_up(creds: AuthCredentials):
    if not creds.email or not creds.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        response = supabase.auth.sign_up({"email": creds.email, "password": creds.password})
        return {"message": "User registered successfully", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", status_code=status.HTTP_200_OK)
def log_in(creds: AuthCredentials):
    if not creds.email or not creds.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    try:
        response = supabase.auth.sign_in_with_password({"email": creds.email, "password": creds.password})
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.get("/public/info", status_code=status.HTTP_200_OK)
def public_info():
    return {"message": "Welcome stranger! This info is public."}

@app.get("/protected/profile", status_code=status.HTTP_200_OK)
def protected_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return {
            "id": user_response.user.id,
            "email": user_response.user.email,
            "created_at": user_response.user.created_at
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def verify_access_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return user_response.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/protected/dashboard", status_code=status.HTTP_200_OK)
def protected_dashboard(user = Depends(verify_access_token)):
    return {"message": f"Welcome to your dashboard, {user.email}"}

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def log_out(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Note: Depending on your supabase-py version, sign_out may not take a token argument.
        # But we will use the user's provided code as requested.
        supabase.auth.sign_out(token)
        return
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
