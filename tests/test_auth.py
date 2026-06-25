def test_register_returns_success(client, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201
    assert response.json()["first_name"] == test_user["first_name"]
    assert response.json()["last_name"] == test_user["last_name"]
    assert response.json()["email"] == test_user["email"]

def test_register_duplicate_email_returns_400(client, test_user):
    response1 = client.post("/auth/register", json=test_user)
    assert response1.status_code == 201

    response2 = client.post("/auth/register", json=test_user)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "User with this email already exists"

def test_register_missing_fields_returns_422(client, test_user):
    response = client.post("/auth/register", json={
        "first_name": test_user["first_name"],
        "email": test_user["email"]
    })
    assert response.status_code == 422

def test_login_returns_success(client, test_user):
    client.post("/auth/register", json=test_user)
    response = client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200

def test_login_wrong_email_returns_401(client, test_user):
    response = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": test_user["password"]
    })
    assert response.status_code == 401

def test_login_wrong_password_returns_401(client, test_user):
    client.post("/auth/register", json=test_user)
    response = client.post("/auth/login", json={
        "email": test_user["email"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_logout_returns_success(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200

def test_logout_clears_cookie(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert "token" not in response.cookies

def test_register_and_login_flow(client, test_user):
    register_response = client.post("/auth/register", json=test_user)
    assert register_response.status_code == 201

    login_response = client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert login_response.status_code == 200

def test_register_and_login_and_logout_flow(client, test_user):
    register_response = client.post("/auth/register", json=test_user)
    assert register_response.status_code == 201

    login_response = client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert login_response.status_code == 200

    logout_response = client.post("/auth/logout")
    assert logout_response.status_code == 200

def test_login_sets_cookie(client, test_user):
    client.post("/auth/register", json=test_user)
    login_response = client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert login_response.status_code == 200
    assert "token" in login_response.cookies

def test_logout_clears_cookie_after_login(client, test_user):
    client.post("/auth/register", json=test_user)
    login_response = client.post("/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert login_response.status_code == 200
    assert "token" in login_response.cookies

    logout_response = client.post("/auth/logout")
    assert logout_response.status_code == 200
    assert "token" not in logout_response.cookies
