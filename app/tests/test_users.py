# The 'client' argument is automatically injected by conftest.py!

def test_health_check(client):
    """Test that the server is alive"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"health": "ok"}


def test_register_user(client):
    """Test that a new user can register successfully"""
    # 1. Simulate a frontend sending JSON to your endpoint
    response = client.post(
        "/auth/register", # Update this if your route is different!
        json={"email": "test@example.com", "username": "testuser", "password": "securepassword123"}
    )
    
    # 2. Check the results
    assert response.status_code == 201
    
    # 3. Verify the database returned the correct schema (without the password!)
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password" not in data


def test_login_user(client):
    """Test that the registered user can log in and receive a JWT"""
    # 1. Use 'data' instead of 'json' for OAuth2 Form Data
    response = client.post(
        "/auth/login", 
        data={"username": "testuser", "password": "securepassword123"}
    )
    
    # 2. Verify the login was successful
    assert response.status_code == 200
    
    # 3. Verify the server gave us a perfectly formatted Token schema
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_access_protected_route(client):
    """Test that a valid JWT token unlocks protected endpoints"""
    
    # 1. Log in first to grab a fresh token
    login_response = client.post(
        "/auth/login", 
        data={"username": "testuser", "password": "securepassword123"}
    )
    token = login_response.json()["access_token"]
    
    # 2. Attach the token to the Authorization header
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Request the protected route (Change '/auth/me' to your actual route!)
    response = client.get("/auth/me", headers=headers)
    
    # 4. Verify the server accepted the token and returned the user data
    assert response.status_code == 200
    
    data = response.json()
    assert data["username"] == "testuser"
    assert "email" in data