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


def test_register_and_login_long_password(client):
    long_password = "a" * 100

    register_response = client.post(
        "/auth/register",
        json={"email": "long@example.com", "username": "longuser", "password": long_password},
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={"username": "longuser", "password": long_password},
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_verify_legacy_bcrypt_hash():
    from app.auth import get_password_hash, verify_password, pwd_context

    password = "legacy-password-123"
    legacy_hash = pwd_context.hash(password)

    assert verify_password(password, legacy_hash) is True
    assert verify_password(password, get_password_hash(password)) is True